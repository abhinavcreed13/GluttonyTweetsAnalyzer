//
// Team 13, Melbourne
// Abhinav Sharma, 1009225
// Benjamin Frengley, 1050642
// Kabir Manandhar Shrestha, 1059431
// Rohit Kumar Gupta, 1023418
// Jan Knížek, 1052305
//
class SdsMap {
    constructor(containerId) {
        this._container = containerId;
        this._tweetLayer = 'sds-tweets';
        this._aurinAlcoholLayer = 'sds-aurin-alcohol';
        this._layers = new Set();

        /** @type {import('mapbox-gl').Map)} */
        this._map = null;
    }

    initialize() {
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmZyZW5nbGV5dGVsb2dpcyIsImEiOiJjajNvejhnYnIwMGh5MnFxdHYyem9naHVwIn0.FGvU1_a4IDBABe_WCO9hpQ';

        if (this._map) {
            this._map.remove();
        }

        this._map = new mapboxgl.Map({
            container: this._container,
            center: [144.9587, -37.8197],
            zoom: 10,
            hash: true,
            style: 'mapbox://styles/mapbox/light-v10',
        });
        this._map.on('load', () => {
            this._map.addControl(new mapboxgl.NavigationControl());
        })
    }

    /**
     * @param {string} name 
     * @param {import('mapbox-gl').Layer} layer 
     * @param {string} before
     */
    _addLayer(name, layer, before) {
        this._layers.add(name);
        this._map.addLayer(Object.assign({ id: name }, layer), before);
    }

    /**
     * 
     * @param {any[]} tweets
     * @param {boolean} append
     */
    displayTweets(tweets, append) {
        const map = this._map;
        const tweetGeojson = {
            type: 'FeatureCollection',
            features: tweets.map(({ doc }) => ({
                type: 'Feature',
                geometry: doc.coordinates || doc.geo,
                id: doc.id,
                properties: {
                    text: doc.full_text || doc.text,
                    author: doc.user.screen_name,
                    authorId: doc.user.id,
                    time: doc.created_at,
                },
            })),
        };

        if (map.getSource(this._tweetLayer)) {
            if (append) {
                tweetGeojson.features = tweetGeojson.features.concat(
                    map.getSource(this._tweetLayer).serialize().data.features
                );
            }
            map.getSource(this._tweetLayer).setData(tweetGeojson);
        } else {
            this._addLayer(this._tweetLayer, {
                source: {
                    type: 'geojson',
                    data: tweetGeojson,
                },
                minzoom: 13,
                type: 'circle',
                paint: {
                    'circle-color': 'blue',
                    'circle-radius': [
                        'interpolate',
                        ['linear'], ['zoom'],
                        0, 4,
                        10, 5,
                        15, 7,
                    ],
                    'circle-opacity': 0.7,
                },
            });
            this._addLayer(`${this._tweetLayer}-heatmap`, {
                type: 'heatmap',
                source: this._tweetLayer,
                maxzoom: 13,
                paint: {
                    'heatmap-radius': [
                        'interpolate',
                        ['linear'], ['zoom'],
                        0, 2,
                        8, 5,
                        13, 15,
                    ],
                },
            }, 'road-label');

            let popup = new mapboxgl.Popup();
            map.on('mousemove', this._tweetLayer, ev => {
                let tweet = ev.features[0].properties;
                popup
                    .setLngLat(ev.features[0].geometry.coordinates)
                    .setHTML(`
<div class="tweet-text">
  ${tweet.text}
</div>
<div class="tweet-author">
  &mdash; <a href="https://twitter.com/${tweet.author}">@${tweet.author}</a>
</div>`)
                    .addTo(map);
            });
            map.on('mouseleave', this._tweetLayer, () => {
                popup.remove();
            });
        }
    }

    displayAurinAlcoholData(data) {
        const geojson = {
            type: 'FeatureCollection',
            features: data.filter(item => item.properties.alcohol_related === 'Yes'),
        };

        if (!this._map.getSource(this._aurinAlcoholLayer)) {
            this._addLayer(this._aurinAlcoholLayer, {
                source: {
                    type: 'geojson',
                    data: geojson
                },
                type: 'circle',
                paint: {
                    'circle-opacity': 0.7,
                    'circle-radius': [
                        'interpolate',
                        ['linear'], ['zoom'],
                        0, 5,
                        10, 6,
                        15, 8,
                    ],
                    'circle-color': 'red',
                }
            }, this._map.getLayer(this._tweetLayer) ? this._tweetLayer : undefined);
        } else {
            this._map.getSource(this._aurinAlcoholLayer).setData(geojson);
        }
    }

    displayHealthData(data, key) {
        const geojson = {
            type: 'FeatureCollection',
            features: data.map(item => {
                let xMin = item.bounding_box[0],
                    yMin = item.bounding_box[1],
                    xMax = item.bounding_box[2],
                    yMax = item.bounding_box[3];
                return {
                    geometry: {
                        type: 'Polygon',
                        coordinates: [[
                            [xMin, yMin],
                            [xMax, yMin],
                            [xMax, yMax],
                            [xMin, yMax],
                            [xMin, yMin],
                        ]],
                    },
                    properties: Object.keys(item).reduce((acc, key) => {
                        acc[key.toLowerCase()] = item[key];
                        return acc;
                    }, {}),
                };
            }),
        };

        const colour = [
            'interpolate',
            ['linear'], ['get', `${key}_count`],
            0, 'rgba(0, 0, 255, 0)',
            10, 'royalblue',
            30, 'cyan',
            50, 'lime',
            70, 'yellow',
            100, 'red',
        ];
        const height = [
            'interpolate',
            ['exponential', 1.05], ['get', `${key}_count`],
            0, 1,
            100, 10000,
        ];

        if (this._map.getSource('sds-aurin_gluttony-3d')) {
            this._map.getSource('sds-aurin_gluttony-3d').setData(geojson);
            this._map.setPaintProperty('sds-aurin_gluttony-3d', 'fill-extrusion-height', height);
            this._map.setPaintProperty('sds-aurin_gluttony-3d', 'fill-extrusion-color', colour);
        } else {
            this._addLayer('sds-aurin_gluttony-3d', {
                'type': 'fill-extrusion',
                source: {
                    type: 'geojson',
                    data: geojson,
                },
                'paint': {
                    'fill-extrusion-color': colour,
                    'fill-extrusion-opacity': 0.4,
                    'fill-extrusion-height': height,
                },
            }, this._tweetLayer);

            let popup = new mapboxgl.Popup();
            this._map.on('mousemove', 'sds-aurin_gluttony-3d', ev => {
                let obj = ev.features[0].properties;
                let ui_text = null;

                if (key === 'obesity') ui_text = 'Obesity: ' + obj.obesity_count + '%';
                else if (key === 'heart_disease') ui_text = 'Heart Disease: ' + obj.heart_disease_count + '%';
                else if (key === 'hbp') ui_text = 'High Blood Pressure: ' + obj.HBP_count + '%';
                else if (key === 'diabetes') ui_text = 'Diabetes: ' + obj.diabetes_count + '%';

                popup
                    .setLngLat(ev.lngLat)
                    .setHTML(`
<div class="tweet-text">
  ${ui_text}
</div>`)
                    .addTo(this._map);
            });
            this._map.on('mouseleave', 'sds-aurin_gluttony-3d', () => {
                popup.remove();
            });
        }
    };

    fitBoundingBox(bbox) {
        this._map.fitBounds(
            [[bbox.xmin, bbox.ymin], [bbox.xmax, bbox.ymax]],
            { padding: 20 }
        );
    }

    reset() {
        const sources = new Set();
        for (const layer of this._map.getStyle().layers.filter(l => l.id.startsWith('sds-'))) {
            sources.add(layer.source);
            this._map.removeLayer(layer.id);
        }
        for (const source of sources) {
            this._map.removeSource(source);
        }
    }
}

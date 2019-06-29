//
// Team 13, Melbourne
// Abhinav Sharma, 1009225
// Benjamin Frengley, 1050642
// Kabir Manandhar Shrestha, 1059431
// Rohit Kumar Gupta, 1023418
// Jan Knížek, 1052305
//
class ComponentsManager {
    constructor(apiManagerInstance) {
        console.log('Initilizing ComponentsManager')

        this._apiManager = null;
        this._coordinatesManager = null;

        this._state = {
            _selectedRegionKey: null,
            _selectedRegionBbox: {},
            _selectedSinKey: null,
            _selectedAurinKey: null,
            _tweet_buffer_count: 0
        };

        this._dataState = {
            _sinApiData: [],
            _aurinApiData: [],
            _aurinSelectedKey: null
        };

        this.regions = [
            {id: 'melbourne', text: 'Melbourne'},
            {id: 'melbourne_1', text: 'Melbourne - Part 1'},
            {id: 'melbourne_2', text: 'Melbourne - Part 2'},
            {id: 'melbourne_3', text: 'Melbourne - Part 3'},
            {id: 'melbourne_4', text: 'Melbourne - Part 4'},
        ];

        this.sins = [
            {id: 'alcohol', text: 'Alcohol'},
            {id: 'wrath', text: 'Wrath'},
            {id: 'gluttony', text: 'Gluttony'}
        ];

        this.aurin_dataset = [
            //{id: 'data01', text: 'Perception of Safety - Feeling unsafe during night'},
            {
                id: 'data03',
                search_key: 'obesity',
                text: 'VIC Health - Obesity',
                apiFunction: apiManagerInstance.get_customized_data_from_aurin_gluttony
            },
            {
                id: 'data04',
                search_key: 'heart_disease',
                text: 'VIC Health - Heart Disease',
                apiFunction: apiManagerInstance.get_customized_data_from_aurin_gluttony
            },
            {
                id: 'data05',
                search_key: 'hbp',
                text: 'VIC Health - High Blood Pressure',
                apiFunction: apiManagerInstance.get_customized_data_from_aurin_gluttony
            },
            {
                id: 'data06',
                search_key: 'diabetes',
                text: 'VIC Health - Diabetes',
                apiFunction: apiManagerInstance.get_customized_data_from_aurin_gluttony
            },
            {id: 'data02', text: 'VIC Health - Alcohol'}
        ];

        this._map = new SdsMap('map_view');

        this._apiManager = apiManagerInstance;
        this._coordinatesManager = new CoordinatesManager();
    }

    initializeComponents() {
        this.create_define_region_component();
        this.create_plot_sins_component();
        this.create_aurin_dataset_component();
        this._map.initialize();

        //Reset Action
        $("#reset_action").click((e) => {
            this.reset_event_triggered();
        });

        //Get More Tweets
        $("#get_more_tweets_action").click((e) => {
            this.get_more_tweets_triggered();
        });

        $("#explore_action").click((e) => {
            this.explore_event_triggered();
        });

        $(".explore .close").click((e) => {
            $(".explore").toggleClass('sidebar-open');
        });

        $(".charts").height($(window).height() - 90);
    };

    //************** COMPONENTS **************
    create_define_region_component() {
        //destroy component if exists
        if ($('.data-control-define-region').data('select2')) {
            $('.data-control-define-region').data('select2').destroy();
            $('.data-control-define-region').remove();
            $("#region_section").append('<select class="data-control-define-region" name="state"></select>');
        }

        //add data
        $('.data-control-define-region').append('<option></option>');
        _.each(this.regions, function (regObj) {
            let $ele = '<option value="' + regObj.id + '">' + regObj.text + '</option>';
            $('.data-control-define-region').append($ele);
        });

        //create component
        $('.data-control-define-region').select2({
            closeOnSelect: true,
            placeholder: 'Select Region...',
            allowClear: true,
        });

        // $('.data-control-define-region').on('select2:open', function (e) {
        //     $('.data-control-define-region .select2-search input').prop('focus', false);
        // });

        // add events
        $('.data-control-define-region').on('select2:select', (e) => {
            //console.log(e.params.data);
            $('.data-control-plot-sins').prop('disabled', false);
            $(".data-control-define-region").select2().trigger("select2:close");
            this.region_event_triggered(e.params.data.id, e.params.data.text)
        });
    };

    create_plot_sins_component() {
        //destroy component if exists
        if ($('.data-control-plot-sins').data('select2')) {
            $('.data-control-plot-sins').data('select2').destroy();
            $('.data-control-plot-sins').remove();
            $("#sins_section").append('<select class="data-control-plot-sins" name="state2"></select>');
        }

        //add data
        $('.data-control-plot-sins').append('<option></option>');
        _.each(this.sins, function (regObj) {
            let $ele = '<option value="' + regObj.id + '">' + regObj.text + '</option>';
            $('.data-control-plot-sins').append($ele);
        });

        //create component
        $('.data-control-plot-sins').select2({
            minimumResultsForSearch: -1,
            placeholder: 'Choose sin to plot...',
            allowClear: true,
            disabled: true
        });

        // add events
        $('.data-control-plot-sins').on('select2:select', (e) => {
            //console.log(e.params.data);
            $('.data-control-aurin-dataset').prop('disabled', false);
            $(".data-control-plot-sins").select2().trigger("select2:close");
            this.sins_event_triggered(e.params.data.id)
        });
    };

    create_aurin_dataset_component() {
        //destroy component if exists
        if ($('.data-control-aurin-dataset').data('select2')) {
            $('.data-control-aurin-dataset').data('select2').destroy();
            $('.data-control-aurin-dataset').remove();
            $("#aurin_section").append('<select class="data-control-aurin-dataset" name="state3"></select>');
        }

        //add data
        $('.data-control-aurin-dataset').append('<option></option>');
        _.each(this.aurin_dataset, function (regObj) {
            let $ele = '<option value="' + regObj.id + '">' + regObj.text + '</option>';
            $('.data-control-aurin-dataset').append($ele);
        });

        //create component
        $('.data-control-aurin-dataset').select2({
            minimumResultsForSearch: -1,
            placeholder: 'Choose AURIN dataset...',
            allowClear: true,
            disabled: true
        });

        //add events
        $('.data-control-aurin-dataset').on('select2:select', (e) => {
            console.log(e.params.data);
            $(".data-control-aurin-dataset").select2().trigger("select2:close");
            this.aurin_event_triggered(e.params.data.id, e.params.data.text)
        });
    };

    //*******************************************


    //************* EVENTS HANDLERS *****************

    region_event_triggered(selectedId, selectedText) {
        console.log(selectedId);
        var region_bbox = this._coordinatesManager.get_region_bbox(selectedId);

        //set state
        this._state._selectedRegionKey = selectedId;
        this._state._selectedRegionBbox = region_bbox;

        console.log('region_bbox->' + JSON.stringify(region_bbox));
        $(".output-1").empty();
        $(".output-1").append(JSON.stringify(region_bbox, null, 2));

        //TODO:map can be refined here using region_bbox
        this._map.fitBoundingBox(region_bbox);
    };

    sins_event_triggered(selectedId, map_key) {
        console.log(selectedId);
        this._state._selectedSinKey = selectedId;
        let dataObj = {
            'region_key': this._state._selectedRegionKey,
            'region_bbox': this._state._selectedRegionBbox,
            'sin_key': this._state._selectedSinKey,
            'buffer_mode': false, //TRUE/FALSE
            'minimum_tweets': 100,
            'buffer_count': this._state._tweet_buffer_count
        };
        $(".output-2").empty();
        $(".output-2").append("Fetching from API.......");
        //fetch filtered tweets of *selected sin* (Still in dev mode) from couchdb
        this._apiManager.get_tweets_by_bbox(dataObj, (dataFromApi) => {
            console.log(dataFromApi);
            $(".output-2").empty();
            $(".output-2").append('Showing top 100...Check console.log for more..<br/>');
            var items = dataFromApi.data.slice(0, 100);
            $(".output-2").append(JSON.stringify(items, undefined, 4));

            this._map.displayTweets(dataFromApi.data, map_key);
            this._state._tweet_buffer_count += dataFromApi.data.length;
            $(".tweet_count").empty();
            $(".tweet_count").append(this._state._tweet_buffer_count + " tweets");

            this._dataState._sinApiData = this._dataState._sinApiData.concat(dataFromApi.data);
        });
    };

    aurin_event_triggered(selectedId, selectedText) {
        console.log(selectedId);
        this._state._selectedAurinKey = selectedId;
        let dataObj = {
            'region_key': this._state._selectedRegionKey,
            'region_bbox': this._state._selectedRegionBbox,
            'dataset_name': this._state._selectedAurinKey
        };
        $(".output-3").empty();
        $(".output-3").append("Fetching from API.......");
        var dataset_obj = _.findWhere(this.aurin_dataset, {id: selectedId})
        if (dataset_obj && dataset_obj.apiFunction) {
            dataset_obj.apiFunction(dataObj, (dataFromApi) => {
                console.log(dataFromApi);
                $(".output-3").empty();
                $(".output-3").append('Showing top 100...Check console.log for more..<br/>');
                var items = dataFromApi.data.slice(0, 100);

                if (['data03', 'data04', 'data05', 'data06'].indexOf(selectedId) != -1) {
                    this._map.displayHealthData(dataFromApi.data, dataset_obj.search_key);
                }

                $(".output-3").append(JSON.stringify(items, undefined, 4));

                this._dataState._aurinApiData = dataFromApi.data;
                this._dataState._aurinSelectedKey = dataset_obj.search_key;
            });
        }
        else {
            //fetch filtered data from downloaded aurin json file as per selected dataset
            this._apiManager.get_data_from_aurin_by_bbox(dataObj, (dataFromApi) => {
                console.log(dataFromApi);
                $(".output-3").empty();
                $(".output-3").append('Showing top 100...Check console.log for more..<br/>');
                var items = dataFromApi.data.slice(0, 100);

                if (selectedId === 'data02') {
                    this._map.displayAurinAlcoholData(dataFromApi.data);
                }
                if (selectedId === 'data03') {
                    this._map.displayHealthData(dataFromApi.data);
                }

                $(".output-3").append(JSON.stringify(items, undefined, 4));

                this._dataState._aurinApiData = dataFromApi.data;
            });
        }
    };

    get_more_tweets_triggered() {
        this.sins_event_triggered(this._state._selectedSinKey, true);
    }

    explore_event_triggered() {
        $(".explore").toggleClass('sidebar-open');

        let _sinData, _aurinData, allData, totalTweets,
            _firstDataKey, _secondDataKey;

        //analyze data - Chart #1
        setTimeout(() => {
            _sinData = this._dataState._sinApiData;
            _aurinData = this._dataState._aurinApiData;
            let finalData = [];
            _.each(_aurinData, function (aurinObj) {
                let arrAurin = {
                    key: aurinObj.name,
                    count: 0
                };
                let aurinCoords = aurinObj.bounding_box;
                _.each(_sinData, function (sinObj) {
                    let coords = sinObj.doc.coordinates.coordinates;
                    if ((coords[0] >= aurinCoords[0]) && (coords[0] <= aurinCoords[2])) {
                        if ((coords[1] >= aurinCoords[1]) && (coords[1] <= aurinCoords[3])) {
                            arrAurin.count = arrAurin.count + 1;
                        }
                    }
                });
                finalData.push(arrAurin);
            });
            totalTweets = _sinData.length;
            allData = _.clone(finalData);
            finalData = _.sortBy(finalData, 'count');
            finalData = _.last(finalData, 5);
            _firstDataKey = finalData[finalData.length - 1].key;
            _secondDataKey = finalData[finalData.length - 2].key;
            let seriesData = [];
            _.each(finalData, function (data) {
                seriesData.push([data.key, Number(((data.count / _sinData.length) * 100).toFixed(2))]);
            });
            Highcharts.chart('chart_container_01', {
                chart: {
                    type: 'pie',
                    options3d: {
                        enabled: true,
                        alpha: 45
                    },
                    backgroundColor: '#f9f7f7',
                    style: {
                        fontFamily: 'Lato',
                        fontSize: '9px'
                    }
                },
                exporting: {
                    enabled: false
                },
                title: {
                    text: ''
                },
                plotOptions: {
                    pie: {
                        innerSize: 60,
                        depth: 30,
                        size: 200,
                        dataLabels: {
                            enabled: false
                        },
                        showInLegend: true
                    }
                },
                credits: {
                    enabled: false
                },
                tooltip: {
                    formatter: function () {
                        return 'Tweets: <b>' + this.y + '%</b>';
                    }
                },
                legend: {
                    enabled: true
                },
                yAxis: {
                    reversedStacks: true
                },
                series: [{
                    name: 'Tweets',
                    data: seriesData
                }]
            });
        }, 700);

        //Chart #2 - Aurin Data Analysis
        setTimeout(() => {
            let _aurinKey = this._dataState._aurinSelectedKey;
            let chart2data = [];
            let xFactor = [['obesity', 'Obesity'], ['heart_disease', 'Heart Disease'], ['hbp', 'High-Blood Pressure'], ['diabetes', 'Diabetes']];
            let xVal = _.sample(xFactor);
            let self = this;
            let yText = '';
            while (xVal[0] == _aurinKey) {
                xVal = _.sample(xFactor);
            }
            _.each(_aurinData, function (aurinObj) {
                let val = 0;
                if (_aurinKey === 'obesity') {
                    val = aurinObj.obesity_count;
                    yText = 'Obesity';
                }
                else if (_aurinKey === 'heart_disease') {
                    val = aurinObj.heart_disease_count;
                    yText = 'Heart Disease';
                }
                else if (_aurinKey === 'hbp') {
                    val = aurinObj.HBP_count;
                    yText = 'High Blood Pressure';

                }
                else if (_aurinKey === 'diabetes') {
                    val = aurinObj.diabetes_count;
                    yText = 'Diabetes';

                }
                $("#chart_02 .chart_header").empty();
                $("#chart_02 .chart_header").append(yText + ' vs ' + xVal[1]);

                // chart2data.push({
                //     name: aurinObj.name,
                //     value: val
                // });
                chart2data.push({
                    name: aurinObj.name,
                    data: [[val, self.get_aurin_data(xVal[0], aurinObj),]]
                });
            });
            //chart2data = _.sortBy(chart2data, 'value');
            //chart2data = _.last(chart2data, 5);

            Highcharts.chart('chart_container_02', {
                    chart: {
                        type: 'scatter',
                        zoomType: 'xy',
                        backgroundColor: '#f9f7f7',
                        style: {
                            fontFamily: 'Lato',
                            fontSize: '10px'
                        }
                    },
                    title: {
                        text: ''
                    },
                    exporting: {
                        enabled: false
                    },
                    xAxis: {
                        title: {
                            enabled: true,
                            text: yText + ' % '
                        },
                        startOnTick: true,
                        endOnTick: true,
                        showLastLabel: true
                    },
                    yAxis: {
                        title: {
                            text: xVal[1] + ' % '
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    credits: {
                        enabled: false
                    },
                    plotOptions: {
                        scatter: {
                            marker: {
                                radius: 7,
                                states: {
                                    hover: {
                                        enabled: true,
                                        lineColor: 'rgb(100,100,100)'
                                    }
                                }
                            },
                            states: {
                                hover: {
                                    marker: {
                                        enabled: false
                                    }
                                }
                            },
                            tooltip: {
                                headerFormat: '<b>{series.name}</b><br>',
                                pointFormat: yText + ':{point.x} % <br>' + xVal[1] + ': {point.y} %'
                            }
                        }
                    },
                    // series: [{
                    //     name: 'Region',
                    //     color: 'rgba(223, 83, 83, .5)',
                    //     data: chart2data
                    // }]
                    series: chart2data
                },
                function (chart) {
                    _.each(chart.series, function (serObj) {
                        if (serObj.name == _firstDataKey || serObj.name == _secondDataKey) {
                            serObj.data[0].setState('hover');
                        }
                    });
                });
        }, 1500);

        // Chart #3
        setTimeout(() => {
            let dataObj = {
                'region_key': this._state._selectedRegionKey,
                'region_bbox': this._state._selectedRegionBbox
            };
            this._apiManager.get_restaurants_data(dataObj, (dataFromApi) => {
                let resDataWithAurin = [];
                _.each(_aurinData, function (aurinObj) {
                    let arrAurin = {
                        key: aurinObj.name,
                        count: 0
                    };
                    let aurinCoords = aurinObj.bounding_box;
                    _.each(Object.keys(dataFromApi.data), function (key) {
                        let coords = dataFromApi.data[key];
                        if ((Number(coords[0]) >= aurinCoords[0]) && (Number(coords[0]) <= aurinCoords[2])) {
                            if ((Number(coords[1]) >= aurinCoords[1]) && (Number(coords[1]) <= aurinCoords[3])) {
                                arrAurin.count = arrAurin.count + 1;
                            }
                        }
                    });
                    resDataWithAurin.push(arrAurin);
                });
                resDataWithAurin = _.filter(resDataWithAurin, function (r) {
                    return r.count > 0
                });
                let categories = _.pluck(resDataWithAurin, 'key');
                let data1 = _.pluck(resDataWithAurin, 'count');
                let totalres = resDataWithAurin.reduce((s, f) => {
                    return s + f.count;               // return the sum of the accumulator and the current time, as the the new accumulator
                }, 0);
                let data1percent = [];
                _.each(data1, function (d) {
                    data1percent.push(-100 * Number((d / totalres).toFixed(4)));
                });
                let data2 = [];
                _.each(categories, function (category) {
                    let c = _.findWhere(allData, {key: category}).count;
                    c = Number((c / totalTweets).toFixed(4));
                    data2.push(c * 100);
                });

                Highcharts.chart('chart_container_03', {
                    chart: {
                        type: 'bar',
                        backgroundColor: '#f9f7f7',
                        style: {
                            fontFamily: 'Lato',
                            fontSize: '10px'
                        }
                    },
                    exporting: {
                        enabled: false
                    },
                    title: {
                        text: ''
                    },
                    credits: {
                        enabled: false
                    },
                    xAxis: [{
                        categories: categories,
                        reversed: false,
                        labels: {
                            step: 1
                        }
                    }, { // mirror axis on right side
                        opposite: true,
                        reversed: false,
                        categories: categories,
                        linkedTo: 0,
                        labels: {
                            step: 1
                        }
                    }],
                    yAxis: {
                        title: {
                            text: null
                        },
                        labels: {
                            formatter: function () {
                                return Math.abs(this.value) + '%';
                            }
                        }
                    },

                    plotOptions: {
                        series: {
                            stacking: 'normal'
                        }
                    },

                    tooltip: {
                        formatter: function () {
                            return '<b>' + this.series.name + '<br/>' +
                                this.point.category + ':' + Highcharts.numberFormat(Math.abs(this.point.y), 0) + ' % ';
                        }
                    },

                    series: [{
                        name: 'Restaurants',
                        data: data1percent
                    }, {
                        name: 'Tweets',
                        data: data2
                    }]
                });

            });
        }, 2000);
    }

    get_aurin_data(key, aurinObj) {
        if (key === 'obesity') {
            return aurinObj.obesity_count;
        }
        else if (key === 'heart_disease') {
            return aurinObj.heart_disease_count;
        }
        else if (key === 'hbp') {
            return aurinObj.HBP_count;
        }
        else if (key === 'diabetes') {
            return aurinObj.diabetes_count;
        }
    }

    reset_event_triggered() {
        console.log('reset triggered');
        //reset state
        this._state = {
            _selectedRegionKey: null,
            _selectedRegionBbox: {},
            _selectedSinKey: null,
            _selectedAurinKey: null,
            _tweet_buffer_count: 0
        };
        //reset select2
        this.create_define_region_component();
        this.create_plot_sins_component();
        this.create_aurin_dataset_component();

        //clean pre
        $(".output-1").empty();
        $(".output-2").empty();
        $(".output-3").empty();

        $(".tweet_count").empty().append("0 tweets");

        this._map.fitBoundingBox(this._coordinatesManager.get_region_bbox('melbourne'));
        this._map.reset();
    }

    //*******************************************
}

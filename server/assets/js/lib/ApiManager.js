//
// Team 13, Melbourne
// Abhinav Sharma, 1009225
// Benjamin Frengley, 1050642
// Kabir Manandhar Shrestha, 1059431
// Rohit Kumar Gupta, 1023418
// Jan Knížek, 1052305
//
class ApiManager {
    constructor() {
        console.log('Initilizing ApiManager');

        this.URLs = {
            GET_TWEETS_BY_BBOX: '/api/get_tweets_by_bbox',
            GET_DATA_FROM_AURIN_BY_BBOX: '/api/get_data_from_aurin_by_bbox',
            GET_CUSTOMIZED_DATA_AURIN_GLUTTONY: '/api/get_customized_aurin_data_by_bbox_gluttony',
            GET_RESTAURANTS_DATA: '/api/get_restaurants_data'
        };

        this.get_tweets_by_bbox = this._post.bind(this, this.URLs.GET_TWEETS_BY_BBOX);
        this.get_data_from_aurin_by_bbox = this._post.bind(this, this.URLs.GET_DATA_FROM_AURIN_BY_BBOX);
        this.get_customized_data_from_aurin_gluttony = this._post.bind(this, this.URLs.GET_CUSTOMIZED_DATA_AURIN_GLUTTONY);
        this.get_restaurants_data = this._post.bind(this, this.URLs.GET_RESTAURANTS_DATA);
    };

    _post(url, data, callback) {
        $.ajax({
            url,
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            success: callback,
        });
    }
}

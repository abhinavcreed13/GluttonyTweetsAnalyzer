//
// Team 13, Melbourne
// Abhinav Sharma, 1009225
// Benjamin Frengley, 1050642
// Kabir Manandhar Shrestha, 1059431
// Rohit Kumar Gupta, 1023418
// Jan Knížek, 1052305
//
class CoordinatesManager {
    constructor() {
        console.log('Initilizing CoordinatesManager');

        this.region_coords = {
            "melbourne": {
                "xmin": 144.5869,
                "xmax": 145.3477,
                "ymin": -38.299,
                "ymax": -37.5581
            },
            //144.962302,-38.397737 145.569297,-37.822896
            "melbourne_1": {
                "xmin": 144.962302,
                "xmax": 145.569297,
                "ymin": -38.397737,
                "ymax": -37.822896
            },
            //144.962302,-37.822896 145.569297,-37.495657
            "melbourne_2": {
                "xmin": 144.962302,
                "xmax": 145.569297,
                "ymin": -37.822896,
                "ymax": -37.495657
            },
            //144.345695,-37.822896 144.962302,-37.495657
            "melbourne_3": {
                "xmin": 144.345695,
                "xmax": 144.962302,
                "ymin": -37.822896,
                "ymax": -37.495657
            },
            //144.17678,-38.271704 144.962302,-37.495657
            "melbourne_4": {
                "xmin": 144.17678,
                "xmax": 144.962302,
                "ymin": -38.271704,
                "ymax": -37.822896
            }
        };
    }

    get_region_bbox(region_key) {
        return this.region_coords[region_key];
    }
}

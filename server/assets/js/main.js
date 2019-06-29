//
// Team 13, Melbourne
// Abhinav Sharma, 1009225
// Benjamin Frengley, 1050642
// Kabir Manandhar Shrestha, 1059431
// Rohit Kumar Gupta, 1023418
// Jan Knížek, 1052305
//
'use strict';

class SDS {
    constructor() {
        console.log('Initilizing SDS')
        this._apiManager = new ApiManager();
        this._componentsManager = new ComponentsManager(this._apiManager);
    }

    init() {
        this._componentsManager.initializeComponents();
    }
}

'use strict';

var Motor = function (params){
    var _this = this;
	console.log('Motor Initalized', params);
};

Motor.prototype.forward = function(num){
    console.log('Forward', num);
};

Motor.prototype.backward = function(num){
    console.log('Backward', num);
};

Motor.prototype.stop = function(key){
    console.log('Stop');
};

module.exports = Motor;

'use strict';

angular.module('8wizards.components.subtabs.filters', ['ngRoute'])
    .filter('makeRange', function() {
        return function(input) {

            var low = input[0],
                high = input[1],
                step = input[2];

            var result = [];
            for (var i = low; i < high; i=i+step)
                if (i > low)
                    result.push(i);
            if (result[result.length - 1] != high) {
                result.push(high);
            }
            return result;
        };
    });
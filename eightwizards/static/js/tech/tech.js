'use strict';

angular.module('8wizards.tech', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/tech', {
    templateUrl: '/static/ngtpls/tech.html',
    controller: 'TechCtrl'
  });
}])

.controller('TechCtrl', [function() {
<<<<<<< HEAD
  console.info('TechCtrl')
=======
  console.info('Tech')
>>>>>>> master
}]);
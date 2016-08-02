'use strict';

angular.module('8wizards.index', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: '/static/ngtpls/index.html',
    controller: 'IndexCtrl'
  }).when('/index', {
    templateUrl: '/static/ngtpls/index.html',
    controller: 'IndexCtrl'
  });
  console.info($routeProvider)
}])

.controller('IndexCtrl', ['$scope', '$location', function() {
  console.info('IndexCTrl');
}]);
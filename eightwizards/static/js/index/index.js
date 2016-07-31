'use strict';

angular.module('8wizards.index', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: '/static/ngtpls/index.html',
    controller: 'IndexCtrl'
  });
}])

.controller('IndexCtrl', [function() {

}]);
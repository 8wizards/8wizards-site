'use strict';

angular.module('8wizards.team', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: '/static/ngtpls/team.html',
    controller: 'TeamCtrl'
  });
}])

.controller('TeamCtrl', [function() {

}]);
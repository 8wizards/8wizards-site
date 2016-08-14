'use strict';

angular.module('8wizards.projects', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider
      .when('/projects', {
        templateUrl: '/static/ngtpls/projects.html',
        controller: 'ProjectsCtrl'
      })
}])

.controller('ProjectsCtrl', ['$scope', function($scope) {

}]);
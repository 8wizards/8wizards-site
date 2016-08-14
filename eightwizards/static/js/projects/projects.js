'use strict';

angular.module('8wizards.projects', ['ngRoute', '8wizards.projects.services'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider
      .when('/projects', {
        templateUrl: '/static/ngtpls/projects.html',
        controller: 'ProjectsCtrl'
      })
}])

.controller('ProjectsCtrl', ['$scope', 'Projects', function($scope, Projects) {
  $scope.tabs = [
    {name: 'web', publicName: 'Web'},
    {name: 'mob', publicName: 'Mobile'},
    {name: 'games', publicName: 'Games'}
  ];
  Projects.query(function(projects) {
    $scope.projects = projects;
  });
}]);
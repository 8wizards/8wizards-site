'use strict';

angular.module('8wizards.tech', ['ngRoute', '8wizards.tech.services'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/tech', {
    templateUrl: '/static/ngtpls/technologies.html',
    controller: 'TechCtrl'
  });
  $routeProvider.when('/skills', {
    templateUrl: '/static/ngtpls/skills.html',
    controller: 'SkillsCtrl'
  });
  $routeProvider.when('/certificates', {
    templateUrl: '/static/ngtpls/certificates.html',
    controller: 'CertsCtrl'
  });
}])

.controller('TechCtrl', ['$scope', 'Technology', function($scope, Technology) {
  console.info('Tech');
  Technology.query(function(technologies) {
    $scope.technologies = technologies;
  });
}])
.controller('SkillsCtrl', ['$scope', 'Skill', function($scope, Skill) {
  console.info('Skills');
  Skill.query(function(skills) {
    $scope.skills = skills;
  });
}])
.controller('CertsCtrl', ['$scope', 'Certification', function($scope, Certification) {
  console.info('Certificates');
  Certification.query(function(certificates) {
    $scope.certificates = certificates;
  });
}]);
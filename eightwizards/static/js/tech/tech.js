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
.controller('TechTabsCtrl', function($scope) {
  $scope.tabs = [
        {name: 'tech', publicName: 'Technologies'},
        {name: 'skills', publicName: 'Skills'},
        {name: 'certificates', publicName: 'Certificates'}
  ]
})
.controller('TechCtrl', ['$scope', '$controller', 'Technology', function($scope, $controller, Technology) {
  $controller('TechTabsCtrl', {$scope: $scope});
  Technology.query(function(technologies) {
    $scope.technologies = technologies;
  });

}])
.controller('SkillsCtrl', ['$scope', '$controller', 'Skill', function($scope, $controller, Skill) {
  $controller('TechTabsCtrl', {$scope: $scope});
  Skill.query(function(skills) {
    $scope.skills = skills;
  });
}])
.controller('CertsCtrl', ['$scope', '$controller', 'Certification', function($scope, $controller, Certification) {
  $controller('TechTabsCtrl', {$scope: $scope});
  Certification.query(function(certificates) {
    $scope.certificates = certificates;
  });
}]);
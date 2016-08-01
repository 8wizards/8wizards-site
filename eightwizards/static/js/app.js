'use strict';

// Declare app level module which depends on views, and components
angular.module('8wizards', [
    'ngRoute',
    'ngResource',
    '8wizards.index',
    '8wizards.projects',
    '8wizards.contacts',
    '8wizards.team',
    '8wizards.components.generic'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  //$locationProvider.hashPrefix('!');
  $routeProvider.otherwise({redirectTo: '/index'});
}]).
config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
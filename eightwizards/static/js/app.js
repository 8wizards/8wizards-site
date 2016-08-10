'use strict';

// Declare app level module which depends on views, and components
angular.module('8wizards', [
    'ngRoute',
    'ngResource',
    'ngAnimate',
    'angular-blocks',
    '8wizards.index',
    '8wizards.projects',
    '8wizards.contacts',
    '8wizards.team',
    '8wizards.tech',
    '8wizards.components.frame',
    '8wizards.components.subtabs',
    '8wizards.components.mobileNav'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  //$locationProvider.hashPrefix('!');
  $routeProvider.otherwise({redirectTo: '/index'});
}]).
config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
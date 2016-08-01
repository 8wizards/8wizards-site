'use strict';

angular.module('8wizards.contacts', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/contacts', {
    templateUrl: '/static/ngtpls/contacts.html',
    controller: 'ContactsCtrl'
  });
}])

.controller('ContactsCtrl', [function() {
  console.info('ContactsCtrl')
}]);
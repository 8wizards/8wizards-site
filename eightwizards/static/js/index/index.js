'use strict';

angular.module('8wizards.index', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: '/static/ngtpls/index.html',
    controller: 'IndexCtrl'
  });
  console.info($routeProvider)
}])

.controller('IndexCtrl', ['$scope', '$location', function($scope, $location) {
  console.info('IndexCTrl');
  $scope.out = function($event) {
    var redirectTarget = $event.delegateTarget.rel;
    $location.redirectTo('/'+redirectTarget)
  }
}]);
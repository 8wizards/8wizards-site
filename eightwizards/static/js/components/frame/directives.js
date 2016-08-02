'use strict';

angular.module('8wizards.components.frame.directives', ['ngRoute'])


.directive('navigationFrame', ['$location', function($location) {
  return {
    restrict: 'E',
    transclude: true,
    templateUrl: 'static/ngtpls/frame/component.html',
    scope: {
      navigation: '='
    },
    link: function (scope) {
      scope.out = function($event) {
        var redirectTarget = $event.delegateTarget.rel;
        $location.url('/'+redirectTarget);
      }
    }
  };
}]);
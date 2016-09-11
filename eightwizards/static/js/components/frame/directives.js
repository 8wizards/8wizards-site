'use strict';

angular.module('8wizards.components.frame.directives', ['ngRoute', 'ngAnimate'])


.directive('navigationFrame', ['$location', '$animate', '$document', '$timeout', '$rootScope', function($location, $animate, $document, $timeout, $rootScope) {
  return {
    restrict: 'E',
    transclude: true,
    templateUrl: 'static/ngtpls/frame/component.html',
    scope: {
      navigation: '='
    },
    link: function (scope) {
      scope.out = function($event, pageAnimationClass) {
        $rootScope.pageAnimationClass = pageAnimationClass;
        $location.url('/'+$event.delegateTarget.rel);
      }
    }
  };
}]);
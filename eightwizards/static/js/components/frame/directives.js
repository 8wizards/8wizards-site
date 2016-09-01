'use strict';

angular.module('8wizards.components.frame.directives', ['ngRoute', 'ngAnimate'])


.directive('navigationFrame', ['$location', '$animate', '$document', '$timeout', function($location, $animate, $document, $timeout) {
  return {
    restrict: 'E',
    transclude: true,
    templateUrl: 'static/ngtpls/frame/component.html',
    scope: {
      navigation: '='
    },
    link: function (scope) {
      scope.out = function($event) {
        var el = $document.find('.frame-overlay .'+$event.delegateTarget.dataset.position);
        $animate.addClass(el, 'transition').done(function() {
          $timeout(function() {
            $location.url('/'+$event.delegateTarget.rel);
          }, 0)
        })
      }
    }
  };
}]);
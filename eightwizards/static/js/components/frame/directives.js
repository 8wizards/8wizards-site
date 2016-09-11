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
      /*scope.out = function($event) {
        var el = $document.find('.frame-overlay .'+$event.delegateTarget.dataset.position)
        $animate.addClass(el, 'transition').done(function() {
          $timeout(function() {
            $location.url('/'+$event.delegateTarget.rel);
          }, 0)
        })
      }*/
      scope.out = function($event, pageAnimationClass) {
        $rootScope.pageAnimationClass = pageAnimationClass;
        $location.url('/'+$event.delegateTarget.rel);
 /*       if (path === 'back') {debugger // Allow a 'back' keyword to go to previous page
            $window.history.back();
        }*/
        
        //else { debugger// Go to the specified path

        //}
      }
    }
  };
}]);
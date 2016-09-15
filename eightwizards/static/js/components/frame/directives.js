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

        //debugger;
        //$rootScope.pageAnimationClass = pageAnimationClass;
         if (typeof(pageAnimationClass) === 'undefined') { // Use a default, your choice
            $rootScope.pageAnimationClass = 'crossFade';
        }
        /*else if(pageAnimationClass == 'standartTab') {
          
        }*/
        else { // Use the specified animation
            $rootScope.pageAnimationClass = pageAnimationClass;
        }


 /*       if (path === 'back') {debugger // Allow a 'back' keyword to go to previous page
            $window.history.back();
        }*/
        
        //else { debugger// Go to the specified path
            $location.url('/'+$event.delegateTarget.rel);
        //}

        $rootScope.pageAnimationClass = pageAnimationClass;
        $location.url('/'+$event.delegateTarget.rel);

      }
    }
  };
}]);
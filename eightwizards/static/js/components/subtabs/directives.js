'use strict';

angular.module('8wizards.components.subtabs.directives', ['ngRoute', 'ngAnimate'])


.directive('subTabs', ['$location', '$animate', '$document', '$timeout', function($location, $animate, $document, $timeout) {
  return {
    link: function (scope, element) {
      console.info(scope);
      console.info(element);
      scope.activate = function($event) {
        var el = $event.target
        console.info(el);
        console.info($event.delegateTarget.rel)
        $animate.addClass(el, 'active').done(function() {
          $timeout(function() {
            $location.url('/'+$event.delegateTarget.rel);
          }, 0)
        })
      }
    }
  };
}]).directive('eLastInserted', function () {
        return function (scope, element) {
            if (scope.$last) {
                window.setTimeout(function () {
                    scope.$apply(function () {
                        scope.$emit('LastElem');
                        $(document).foundation();
                        element.closest('.hidden').removeClass('hidden')
                    })
                }, 500);
            }
        }
    });;
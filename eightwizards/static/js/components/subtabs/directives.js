'use strict';

angular.module('8wizards.components.subtabs.directives', ['ngRoute', 'ngAnimate'])


.directive('subTabs', ['$location', '$animate', '$document', '$timeout', function($location, $animate, $document, $timeout) {
  return {
    link: function (scope, element) {
      scope.activate = function($event) {
        var el = $event.target;
        $animate.addClass(el, 'active').done(function() {
          $timeout(function() {
            $location.url('/'+$event.delegateTarget.attributes.id.value);
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
    }).directive('dynamicHeight', function(){
        return function(scope, element) {
            console.info($(window).height());
            element.height(($(window).height() - $(window).height()*0.15));
        }
});
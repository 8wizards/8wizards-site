'use strict';

angular.module('8wizards.components.mobileNav.directives', ['ngRoute', 'ngAnimate'])


.directive('navigationMobile', ['$location', '$animate', '$document', '$timeout', function($location, $animate, $document, $timeout) {
  return {
    restrict: 'E',
    template: '<button>Menu</button>'

  };
}]);
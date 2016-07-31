'use strict';

angular.module('8wizards.components.generic.directives', [])

.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]);
'use strict';

angular.module('8wizards.components.mobileNav.directives', ['ngRoute', 'ngAnimate'])


.directive('navigationMobile', ['$location', '$animate', '$document', '$timeout', function($location, $animate, $document, $timeout) {
  return {
    restrict: 'E',
    templateUrl: 'static/ngtpls/mobileNav.html',
    scope: {
      'navOptions': '=',
      'toggleId': '='
    },
    link: function(scope) {
      scope.addStyle = function() {
        var tabMenu = $( '#' + scope.toggleId );
        if (tabMenu.hasClass( 'hide-for-small-only')) {
          tabMenu.removeClass('hide-for-small-only');
        }
        else {
          tabMenu.addClass('hide-for-small-only');
        }
      }

    }

  };
}]);
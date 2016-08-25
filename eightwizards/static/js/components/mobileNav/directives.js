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
      $(".toggle-mnu").click(function() {
    $(this).toggleClass("on");
    $(".sub-tabs").slideToggle();
    return false;
  });
     /* $(document).foundation();
      //console.log(scope.navOptions)
      scope.addStyle = function() {
        $(document).foundation();

      }*/

    }

  };
}]);
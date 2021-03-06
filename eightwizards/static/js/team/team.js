'use strict';

angular.module('8wizards.team', ['ngRoute', 'ngAnimate', '8wizards.team.services'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/team', {
    templateUrl: '/static/ngtpls/team.html',
    controller: 'TeamCtrl'
  });
    $routeProvider.when('/approach', {
    templateUrl: '/static/ngtpls/approach.html',
    controller: 'ApproachCtrl'
  });
    $routeProvider.when('/hiring', {
    templateUrl: '/static/ngtpls/hiring.html',
    controller: 'HiringCtrl'
  });
}])

.controller('TeamTabsCtrl', function($scope) {
  $scope.tabs = [
        {name: 'team', publicName: 'Team'},
        {name: 'approach', publicName: 'Approach'},
        /*{name: 'hiring', publicName: 'Hiring'}*/
  ];

})
.controller('TeamCtrl', ['$scope', '$controller', 'Team', function($scope, $controller, Team) {
  $controller('TeamTabsCtrl', {$scope: $scope});
  $scope.selected = 0;
    $scope.breakpoints = [{
      breakpoint: 1000,
      settings: {
        slidesToShow: 6,
        slidesToScroll: 6
      }
    },  {
      breakpoint: 768,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 2
      }
    }, {
      breakpoint: 760,
      settings: {
        slidesToShow: 2,
        dots: false,
        slidesToScroll: 1,
        draggable: true
      }
    }, {
      breakpoint: 480,
      settings: {
        slidesToShow: 2,
        dots: false,
        vertical: true,
        verticalSwiping: true,
        slidesToScroll: 1,
        draggable: true,
      }
    }];

    $scope.slickConfig = {
    enabled: true,
    autoplay: true,
    verticalSwiping: false,
    dots: true,
    slidesToShow: 8,
    slidesToScroll: 8,
    arrows: false,
    draggable: true,
    autoplaySpeed: 5000,
    method: {},
    event: {
        beforeChange: function (event, slick, currentSlide, nextSlide) {
        },
        afterChange: function (event, slick, currentSlide, nextSlide) {
        }
    }
  };

  Team.query(function(team) {
    $scope.team = team;
  });

}])
.controller('ApproachCtrl', ['$scope', '$controller', 'Skill', function($scope, $controller, Approach) {
  $controller('TeamTabsCtrl', {$scope: $scope});
  $scope.selected = 1;
   $scope.breakpoints = [{
      breakpoint: 480,
      settings: {
        dots: false
      }
    }];
     $scope.slickConfig = {
      adaptiveHeight: false,
    enabled: true,
    autoplay: true,
    slidesToScroll: 1,
    dots: true,
    arrows: false,
    draggable: true,
    autoplaySpeed: 6000,
    method: {},
    event: {
        beforeChange: function (event, slick, currentSlide, nextSlide) {
        },
        afterChange: function (event, slick, currentSlide, nextSlide) {
        }
    }
};

  Approach.query(function(approach) {
    $scope.approach = approach;
  });
}])
.controller('HiringCtrl', ['$scope', '$controller', 'Certification', function($scope, $controller, Hiring) {
  $controller('TeamTabsCtrl', {$scope: $scope});
  $scope.selected = 2;
  Hiring.query(function(hiring) {
    $scope.hiring = hiring;
  });
}]);








'use strict';

angular.module('8wizards.team', ['ngRoute'])

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
        {name: 'hiring', publicName: 'Hiring'}
  ]
})
.controller('TeamCtrl', ['$scope', '$controller', 'Technology', function($scope, $controller, Technology) {
  $controller('TeamTabsCtrl', {$scope: $scope});
    $scope.breakpoints = [{
      breakpoint: 1000,
      settings: {
        slidesToShow: 6,
        slidesToScroll: 6
      }
    },  {
      breakpoint: 740,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 4
      }
    }, {
      breakpoint: 500,
      settings: {
        slidesToShow: 2,
        dots: false,
        vertical: true,
        verticalSwiping: true,
        slidesToScroll: 1
      }
    }];

    $scope.slickConfig = {
    enabled: true,
    autoplay: true,
    dots: true,
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

  Technology.query(function(technologies) {
    $scope.technologies = technologies;
  });

}])
.controller('ApproachCtrl', ['$scope', '$controller', 'Skill', function($scope, $controller, Skill) {
  $controller('TeamTabsCtrl', {$scope: $scope});
  Approach.query(function(approach) {
    $scope.approach = approach;
  });
}])
.controller('HiringCtrl', ['$scope', '$controller', 'Certification', function($scope, $controller, Certification) {
  $controller('TeamTabsCtrl', {$scope: $scope});
  Hiring.query(function(hiring) {
    $scope.hiring = hiring;
  });
}]);








'use strict';

angular
    .module('8wizards.projects', ['ngRoute', '8wizards.projects.services'])
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider
          .when('/projects', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'ProjectsCtrl'
          });
      $routeProvider
          .when('/mobile', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'MobileCtrl'
          });
      $routeProvider
          .when('/projects/games', {
            templateUrl: '/static/ngtpls/games.html',
            controller: 'GamesCtrl'
          });

    }])
    .controller('ProjectsTabsCtrl', function($scope) {
      $scope.tabs = [
        {name: 'projects', publicName: 'Web'},
        {name: 'mobile', publicName: 'Mobile'},
        //{name: 'games', publicName: 'Games'}
      ];
      $scope.breakpoints = [{
          breakpoint: 740,
          settings: {
            dots: false
          }
        },{
          breakpoint: 480,
          settings: {
            dots: false
           }
        }];
       $scope.slickConfig = {
        enabled: true,
        autoplay: true,
        slidesToScroll: 1,
        dots: true,
        arrows: false,
        draggable: true,
        autoplaySpeed: 3000,
        method: {},
        event: {
            beforeChange: function (event, slick, currentSlide, nextSlide) {
            },
            afterChange: function (event, slick, currentSlide, nextSlide) {
            }
        }
    };
    })

    .controller('ProjectsCtrl', ['$scope', '$controller', 'Projects', function($scope, $controller, webProjects) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 0;
      $scope.projects = [];
      webProjects.query(function(projects) {
        $scope.projects = projects;
      });
    }])
    .controller('MobileCtrl', ['$scope', '$controller', 'mobileProjects', function($scope, $controller, mobileProjects) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 1;
      mobileProjects.query(function(mobiles) {
        $scope.projects = mobiles;
      });
    }])
    .controller('GamesCtrl', ['$scope', '$controller', 'Game', function($scope, $controller, Game) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 2;
      Game.query(function(games) {
        $scope.games = games;
  });
}]);
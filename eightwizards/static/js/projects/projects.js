'use strict';

angular
    .module('8wizards.projects', ['ngRoute', '8wizards.projects.services'])
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider
          .when('/projects', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'ProjectsCtrl'
          })
          .when('/projects/:id', {
            templateUrl: '/static/ngtpls/project-detail.html',
            controller: 'ProjectDetailCtrl'
          });
      $routeProvider
          .when('/mobile', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'MobileCtrl'
          })
          .when('/mobile/:id', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'ProjectDetailCtrl'
          });
      $routeProvider
          .when('/games', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'GamesCtrl'
          })
          .when('/games/:id', {
            templateUrl: '/static/ngtpls/projects.html',
            controller: 'ProjectDetailCtrl'
          });

    }])
    .controller('ProjectDetailCtrl', ['$scope','Projects', '$routeParams', function($scope, Projects, $routeParams) {
      $scope.tabs = [
        /*{name: 'projects', publicName: 'Web'},
        {name: 'mobile', publicName: 'Mobile'},
        {name: 'games', publicName: 'Games'}*/
      ];
      $scope.projectDetail = {};
      Projects.get(
        {id: $routeParams.id},
        function(res) {
          $scope.projectDetail = res;
        }
      )
    }]) 
    .controller('ProjectsTabsCtrl', function($scope) {
      $scope.tabs = [
        {name: 'projects', publicName: 'Web'},
        {name: 'mobile', publicName: 'Mobile'}
        /*{name: 'games', publicName: 'Games'}*/
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
        slidesToShow: 1,
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

    })

    .controller('ProjectsCtrl', ['$timeout', '$scope', '$controller', 'webProjects', function($timeout, $scope, $controller, webProjects) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 0;
      $scope.projects = [];
      $scope.showSlider = false;
      webProjects.query(function(projects) {
        $scope.projects = projects;

      });
      $scope.getLastElement = function (el) {
          console.log(el);
      }
    }])
    .controller('MobileCtrl', ['$scope', '$controller', 'mobileProjects', function($scope, $controller, mobileProjects) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 1;
      mobileProjects.query(function(mobiles) {
        $scope.projects = mobiles;
      });
    }])
    .controller('GamesCtrl', ['$scope', '$controller', 'mobileProjects', function($scope, $controller, mobileProjects) {
      $controller('ProjectsTabsCtrl', {$scope: $scope});
      $scope.selected = 2;
      mobileProjects.query(function(games) {
        $scope.projects = games;
  });
}]);
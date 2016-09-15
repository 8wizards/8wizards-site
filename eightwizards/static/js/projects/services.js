'use strict';

angular
    .module('8wizards.projects.services', ['ngResource'])
    .factory('Projects', function ($resource) {
        return $resource('/api/v1/projects/:id', {id: '@id'} 
        /*{
            get: {method: 'GET', params: {}}
        }*/
        );
    })
    .factory('webProjects', function ($resource) {
        return $resource('/api/v1/categories/web-development/projects/', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    })
    .factory('mobileProjects', function ($resource) {
        return $resource('/api/v1/categories/mobile-development/projects/', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    })
    .factory('gameProjects', function ($resource) {
        return $resource('/api/v1/categories/game-development/projects/', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    });

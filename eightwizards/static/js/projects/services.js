'use strict';

angular
    .module('8wizards.projects.services', ['ngResource'])
    .factory('Projects', function ($resource) {
        return $resource('/api/v1/projects/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
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
    });

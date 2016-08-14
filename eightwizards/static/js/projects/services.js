'use strict';

angular
    .module('8wizards.projects.services', ['ngResource'])
    .factory('Projects', function ($resource) {
        return $resource('/api/v1/projects/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    });


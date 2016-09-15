'use strict';

angular
    .module('8wizards.team.services', ['ngResource'])
    .factory('Team', function ($resource) {
        return $resource('/api/v1/members/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    });

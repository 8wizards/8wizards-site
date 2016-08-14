'use strict';


angular.module('8wizards.projects.services', ['ngResource']).
    factory('Technology', function ($resource) {
        return $resource('/api/v1/technologies/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    })
    .factory('Skill', function($resource) {
        return $resource('/api/v1/skills/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    })
    .factory('Certification', function($resource) {
        return $resource('/api/v1/certification/:id', {}, {
            query: {method: 'GET', params: {}, isArray: true}
        });
    });
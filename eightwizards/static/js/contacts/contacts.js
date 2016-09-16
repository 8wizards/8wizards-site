'use strict';

angular
  .module('8wizards.contacts', ['ngRoute'])
  .config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/contacts', {
      templateUrl: '/static/ngtpls/contacts.html',
      controller: 'ContactsCtrl'
    });
  }])

  .factory('contactUs', ['$resource', function($resource) {
    return $resource('/api/v1/email/')
  }])

  .controller('ContactsCtrl', ['$scope', 'contactUs', '$document', '$http', function($scope, contactUs, $document, $http) {
     $scope.tabs = [
          {name: 'contacts', publicName: 'Contacts US'}
    ];
    $scope.form = {
      name: '',
      email: '',
      message: ''
    };

    $http.defaults.headers.common['X-CSRFToken'] = $document.context.cookie.split('csrftoken=')[1];

    var errorStyle = {'border-color': 'red'},
        okStyle = {'border-color': 'inherit'};

    $scope.fieldValidate = function(value, field) {
      _validateField(value, field);
    };

    $scope.sendFromData = function(){
      var errorFields = [];
      for (var input in $scope.form) {
        if (_validateField($scope.form[input], input)) {
          errorFields.push(input)
        }
      }
      if (!errorFields.length) {
        contactUs.save($scope.form,
          function () {
            $scope.form = {};
            $scope.successMessage = 'Your message was successfully sent, thanks.'
          },
          function (error) {
            $scope.errorMessage = 'Something went wrong. We are so sorry.';
          }
        );
      }
    };
    function _validateField(value, fieldName) {
      var error = false;
      if (value=='') {
        error = true;
        $scope[fieldName] = errorStyle;
      }
      else {
        $scope[fieldName] = okStyle;
      }
      return error;
    }
}]);
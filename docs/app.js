var app = angular.module('StarterApp', ['ngMaterial', 'ngMdIcons']);

app.controller('AppCtrl', ['$scope', '$http', '$mdBottomSheet','$mdSidenav', '$mdDialog', function($scope, $http, $mdBottomSheet, $mdSidenav, $mdDialog){
    
    console.log('hello')
   
   $scope.edtype = {
        isDisabled: false,
        noCache: true,
        selectedItem: 0,
        searchTextChange: function(text) {
            console.log($scope.searchText)
            return ['hello', 'world']
        },
        searchText: '',

   };   
}]);

app.config(function() {

});

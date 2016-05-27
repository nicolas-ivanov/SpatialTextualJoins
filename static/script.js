angular
    .module('app', [
        'ngSanitize',
        'ngtweet',
        'ngMap'
    ])
    .controller('MainCtrl', function($http, $scope, NgMap) {
        var test = [
            '617749885933232128', '617749885933232128'
        ];

        $scope.tweetPairs = [];

        $scope.formSubmit = function() {
            $http
                .get('/ppjoin')
                .then(function(response) {
                    $scope.tweetPairs = [test];
                    // $scope.tweetPairs = response.data || [];
                })
                .catch(function(response) {
                    alert('Something went wrong');
                    console.log(response);
                });
        }


    });

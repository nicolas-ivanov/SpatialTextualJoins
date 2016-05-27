angular
    .module('app', [
        'ngSanitize',
        'ngtweet',
        'ngMap'
    ])
    .controller('MainCtrl', function($http, $scope, NgMap) {
        $scope.data = {};

        var test = [
            '617749885933232128', '617749885933232128'
        ];

        $scope.tweetPairs = [];


        $scope.search = function() {
            request({
                q: $scope.data.theta
            });
        }

        $scope.feelingLucky = function() {
            request();
        }


        function request(params) {
            return $http
                .get('/ppjoin', {
                    params: params
                })
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

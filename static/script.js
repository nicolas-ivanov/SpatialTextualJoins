angular
    .module('app', [
        'ngSanitize',
        'ngtweet',
        'ngMap'
    ])
    .controller('MainCtrl', function($http, $scope, NgMap) {
        $scope.data = {};

        var test = [
            [{
                "id": "617749885933232128",
                "long": "40.74",
                "lat": "-74.21",
                "text": "Test 1"
            }, {
                "id": "733450573018632192",
                "long": "40.71",
                "lat": "-74.20",
                "text": "Test 2"
            }],
            [{
                "id": "617749885933232128",
                "long": "40.72",
                "lat": "-74.22",
                "text": "Test 3"
            }, {
                "id": "733450573018632192",
                "long": "40.74",
                "lat": "-74.21",
                "text": "Test 4"
            }]
        ];

        $scope.tweetPairs = [];


        $scope.search = function() {
            request({
                q: $scope.data.theta
            });
        };

        $scope.feelingLucky = function() {
            request();
        };


        function request(params) {
            return $http
                .get('/ppjoin', {
                    params: params
                })
                .then(function(response) {
                    $scope.tweetPairs = test;
                    // $scope.tweetPairs = response.data || [];
                })
                .catch(function(response) {
                    alert('Something went wrong');
                    console.log(response);
                });
        }

    });

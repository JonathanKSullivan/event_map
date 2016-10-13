var app = angular.module('EventSite', []);

app.controller('homeCtrl', function($scope, $http) {
    $scope.mapListView = "list";
    $scope.zipCode = new Number();
    $scope.distance = 50;
    $scope.sort = "time";
    
    $scope.getEventData = function() {
        $http({
			method: 'GET',
			url: Flask.url_for("json_events")
		}).then(function successCallback(response) {
			var status = response.status;
			data = response.data.json_list
			deleteMarkers();
			deleteList();
			$scope.loadNewData(data)
			// this callback will be called asynchronously
			// when the response is available
		}, function errorCallback(response) {
			console.log(response);
			console.log('error could not get event data check getEventData');
			// called asynchronously if an error occurs
			// or server returns response with an error status.
		});
    };

    

    $scope.toggleMapListView = function() {
        if ($scope.mapListView == "list") {
            $scope.mapListView = "map";
            setTimeout(function() {
                console.log($scope.zipCode)
                console.log($scope.distance)
                console.log($scope.sort)
                google.maps.event.trigger(map, 'resize');
            }, 1);
        } else {
            $scope.mapListView = "list";
        }
    };

    $scope.findEvents = function() {
        $scope.centerMapAtZip();
        $scope.getEventData();
    };

    $scope.centerMapAtZip = function() {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({
            'address': $scope.zipCode.toString()
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //Got result, center the map and put it out there
                map.setCenter(results[0].geometry.location);
                if ($scope.distance == 100) {
                    map.setZoom(8)
                } else if ($scope.distance == 50) {
                    map.setZoom(9)
                } else if ($scope.distance == 20) {
                    map.setZoom(10)
                } else if ($scope.distance == 5) {
                    map.setZoom(12)
                }
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
    };

    $scope.loadNewData = function(eventData) {
        getLatLon($scope.zipCode, 'compare', 'fakeinfo', eventData, $scope.distance);
    };
});
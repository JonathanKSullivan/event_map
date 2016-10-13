var map;
markers = [];
ibArray = [];


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 31.1352,
            lng: -99.3351
        },
        zoom: 6
    });
    map.setOptions({draggable: true});
    google.maps.event.addListener(map, "click", function(event) {
	    for (var i = 0; i < ibArray.length; i++ ) {  //I assume you have your infoboxes in some array
	         ibArray[i].close();
	    }
	});
};

var toggleBounce = function(marker) {
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
    }
};


var getLatLon = function(address,  operation, info="", eventData, distanceThreshold = 0) {
    destinationArray = [];
    originArray = [];
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({
            'address': address.toString()
        },
        function(results, status) {
            if (status == 'OK') {
                if (operation == 'compare') {
                    origin = results[0].geometry.location;
                    for(event in eventData){
                        destination = new google.maps.LatLng({lat: eventData[event].lat, lng: eventData[event].lng});
                        destinationArray.push(destination);
                }
                getDistance(origin, destinationArray, distanceThreshold, eventData);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        }
    });
};

var codeAddress = function(lat, lng, contentString) {
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
    ibArray.push(infowindow)
    myLatLng = new google.maps.LatLng({lat: lat, lng: lng}); 
    addMarker(myLatLng, infowindow);
};

var addMarker = function(location, information) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP
    });
    marker.addListener('click', function() {
    	for (var i = 0; i < ibArray.length; i++ ) {  //I assume you have your infoboxes in some array
	         ibArray[i].close();
	    }
        information.open(map, marker);
        toggleBounce(marker);
        setTimeout(function() {
            toggleBounce(marker);
        }, 3000);
    });
    markers.push(marker);
};

var addList = function(eventData, distance) {
	listItem = '<div class="col-xs-12 listItem">'+
				'<hr/>'+
				'<span class="listItem_distance">'+ distance +' mi</span> '+
				'| '+
				"<span>"+formatDate(new Date(eventData.event_time.substring(0, eventData.event_time.length-4)))
                +"</span>" +
				'<a href="Flask.url_for("readEvent", event_id = ' + eventData.id + ')><h3 class="listItem_title">'+ eventData.title+'</h3>'+
				'<span class="listItem_subtitle">'+eventData.event_type+'</span></a>'+
				'<p id="event" class="listItem_description">'+ eventData.description +'</p>'+
				'<button class="listItem_rsvp pull-right">rsvp</button>'+
				'</div>';

    $('#right_list').append(listItem);
};

// Sets the map on all markers in the array.
var setMapOnAll = function(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
};

// Removes the markers from the map, but keeps them in the array.
var clearMarkers = function() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
var showMarkers = function() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
var deleteMarkers = function() {
    clearMarkers();
    markers = [];
}
var deleteList = function() {
    $('#right_list').text(''); 
}

getDistance = function(origin, destination, distanceThreshold, eventData) {
    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix({
        origins: [origin],
        destinations: destination,
        travelMode: 'DRIVING',
        unitSystem: google.maps.UnitSystem.IMPERIAL
    }, function(responses, status) {
        for(response in responses.rows[0].elements){
            distance = parseFloat(responses.rows[0].elements[response].distance.text.split(' ')[0])
            if (distance < distanceThreshold){
                contentString = "<span>"+eventData[response].zipCode+"</span>" +
                " | "+
                "<span>"+formatDate(new Date(eventData[response].event_time.substring(0, eventData[response].event_time.length-4)))
                +"</span>" +
                "<br/>" +
                "<a href = 'Flask.url_for('''readEvent''', event_id = 'eventData.id')'><h1>"+eventData[response].event_type+"</h1>" +
                "<h2>"+eventData[response].title+"</h2></a>" +
                "<button class='infoWindow_rsvp' style='margin:0px;'>rsvp</button>"
                var infowindow = new google.maps.InfoWindow({
                    content: contentString
                });
                ibArray.push(infowindow)
                addMarker(destination[response], infowindow);
                addList(eventData[response], distance);
            }
        
        }
    });
}

function formatDate(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var day = date.getDate();
  var month = date.getMonth() + 1;
  var year = date.getFullYear();
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return year + "-" + ('0' + month).slice(-2) +  "-" + day + " | " + strTime;
}



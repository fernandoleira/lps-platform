let map;
const initMarkersDelay = 1500;

const redMarkerIcon = "http://127.0.0.1:5000/img/red_marker.png";
const userIcon = "http://127.0.0.1:5000/img/user.png";

// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 42.487770, lng: -83.144608 };

    // The map, centered at Uluru
    map = new google.maps.Map(document.getElementById("map"), {
        center: uluru,
        zoom: 8,
        mapId: 'cb30c336b498ec72'
    });

    findCurrentLocation();

    /* The marker, positioned at Uluru
    const marker = new google.maps.Marker({
        position: uluru,
        map: map,
    });*/

    // Delay the request of markers
    setTimeout(() => {
        getData('http://127.0.0.1:5000/locators')
        .then(res => {
            for (var i = 0; i < res.length; i++)
            {
                // Convert to coordinates
                var latLng = new google.maps.LatLng(res[i].lat, res[i].lon);

                // Add Marker
                new google.maps.Marker({
                    position: latLng,
                    icon: redMarkerIcon,
                    map: map,
                    animation: google.maps.Animation.DROP
                });
            }
        });
    }, initMarkersDelay);
}

function findCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
                };
                new google.maps.Marker({
                    position: pos,
                    icon: userIcon,
                    map: map
                });
                //map.setCenter(pos);
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

async function getData(url = '') {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      headers: {
        'Content-Type': 'application/json' // 'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
    
    return await response.json(); // parses JSON response into native JavaScript objects
  }
let map;
const initMarkersDelay = 1500;

const redMarkerIcon = "http://127.0.0.1:5000/img/red_marker.png";
const blueMarkerIcon = "http://127.0.0.1:5000/img/blue_marker.png";
const greenMarkerIcon = "http://127.0.0.1:5000/img/green_marker.png";
const yellowMarkerIcon = "http://127.0.0.1:5000/img/yellow_marker.png";
const purpleMarkerIcon = "http://127.0.0.1:5000/img/purple_marker.png";
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

    // Delay the request of markers
    setTimeout(() => {
        getData('http://127.0.0.1:5000/locators')
        .then(res => {
            for (var i = 0; i < res.length; i++)
            {
                // Convert to coordinates
                const latLng = new google.maps.LatLng(res[i].lat, res[i].lon);

                // Add Marker
                const marker = new google.maps.Marker({
                    position: latLng,
                    icon: redMarkerIcon,
                    map: map,
                    animation: google.maps.Animation.DROP
                });

                const infoContent = `
                <div class="infoWindow">
                <h5>${res[i].title}</h5>
                <span>${res[i].point_type}</span>
                <p><b>Description:</b> ${res[i].description}</p>
                <span>${res[i].created_at}</span>
                </div>
                `;

                // Add InfoWindow
                const infoWindow = new google.maps.InfoWindow({
                    content: infoContent
                });

                // Open popup window when mouse is over marker
                marker.addListener("mouseover", () => {
                    infoWindow.open({
                        anchor: marker,
                        map,
                        shouldFocus: false,
                    });
                });
                
                // Close popup window when mouse is notover marker
                marker.addListener("mouseout", () => {
                    infoWindow.close();
                });
            }
        });
    }, initMarkersDelay);

    // Finc current user location
    findCurrentLocation();
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
        'Content-Type': 'application/jsonp' // 'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
    
    return await response.json(); // parses JSON response into native JavaScript objects
  }

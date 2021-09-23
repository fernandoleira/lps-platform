const appURL = `http://${window.location.hostname}:${window.location.port}`;
const redMarkerIcon = appURL + "/img/red_marker.png";
const blueMarkerIcon = appURL + "/img/blue_marker.png";
const greenMarkerIcon = appURL + "/img/green_marker.png";
const yellowMarkerIcon = appURL + "/img/yellow_marker.png";
const purpleMarkerIcon = appURL + "/img/purple_marker.png";
const userIcon = appURL + "/img/user.png";
const initMarkersDelay = 1500;

let map;
let markers = [];
let markersUnits = [];
let infoWindows = [];

let attrIdActive = "unit-btn-active";
let activeUnitId = "";

// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 42.487770, lng: -83.144608 };

    // The map, centered at Uluru
    map = new google.maps.Map(document.getElementById("map"), {
        center: uluru,
        zoom: 8,
        mapId: "cb30c336b498ec72"
    });

    // Delay the request of markers
    setTimeout(() => {
        getData(appURL + "/map/locators")
        .then(res => {
            for (var i = 0; i < res.length; i++) {
                // Convert to coordinates
                const latLng = new google.maps.LatLng(res[i].lat, res[i].lon);

                // Add Marker
                const marker = new google.maps.Marker({
                    position: latLng,
                    icon: getMarkerColor(res[i].point_type),
                    map: map,
                    animation: google.maps.Animation.DROP
                });
                markers.push(marker);
                markersUnits.push(res[i].unit_id);

                // Add InfoWindow
                const infoWindow = new google.maps.InfoWindow({
                    content: infoWindowContents(res[i])
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

async function getData(url = "") {
    // Default options are marked with *
    const response = await fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/jsonp", // 'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    return await response.json(); // parses JSON response into native JavaScript objects
}

function findCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
                };

                const current_location_info = new google.maps.InfoWindow({
                    content: '<div class="infoWindow"><h5>You are here!</h5></div>'
                });

                const current_location_marker = new google.maps.Marker({
                    position: pos,
                    icon: userIcon,
                    map: map
                });

                current_location_marker.addListener("mouseover", () => {
                    current_location_info.open({
                        anchor: current_location_marker,
                        map,
                        shouldFocus: false,
                    });
                })

                current_location_marker.addListener("mouseout", () => {
                    current_location_info.close();
                })

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

// Return the image of the marker type for the map
function getMarkerColor(markerType) {
    switch (markerType) {
        case "Info":
            return blueMarkerIcon;
        case "Warning":
            return yellowMarkerIcon;
        case "Alert":
            return redMarkerIcon;
        case "Ping":
            return purpleMarkerIcon;
        default:
            return greenMarkerIcon;
    }
}

// Return the infoWindow content for a specific marker
function infoWindowContents(obj) {
    const infoContent = `
    <div class="infoWindow">
    <h5>${obj.title}</h5>
    <span>${obj.point_type}</span>
    <p><b>Description:</b> ${obj.description}</p>
    <span>${obj.created_at}</span>
    </div>`;

    return infoContent;
}


// Filter through markers to only show the ones having the active unbit id
function unitFilter() {
    for (var i = 0; i < markersUnits.length; i++) {
        if (markersUnits[i] != activeUnitId) markers[i].setMap(null);
    }
}

// Show all markers
function clearUnitFilter() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// When button selector press, create new marker filter
function setUnitFilter(elm) {
// Check if element is currently selected
    if (elm.id == attrIdActive) {
        elm.id = "";
        activeUnitId = "";
        clearUnitFilter();
    } 
    else {
    // Clear other elements selected
        var current_elm = document.getElementById(attrIdActive);

        // Clear selected element
        if (current_elm != null) {
            current_elm.id = "";
            clearUnitFilter();
        }

        // Assign selected button with id
        activeUnitId = elm.getElementsByTagName("p")[0].innerHTML;
        elm.id = attrIdActive;
        unitFilter();
    }
}

function initMap() {
    var uluru = {lat: 41.8735599, lng: -87.6293282};
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12.5,
      center: uluru
    });
    var marker = new google.maps.Marker({
      position: uluru,
      map: map
    });

    // draw many lines http://jsfiddle.net/7UpQZ/7/
    var line = new google.maps.Polyline({
        path: [
            new google.maps.LatLng(41.7930671862, -87.7231602513),
            new google.maps.LatLng(41.793140551, -87.7136071496)
        ],
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 10,
        map: map
    });

}

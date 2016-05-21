
// set up the basic map window
var mymap = L.map('mapid').setView([38, -96], 5);
//var inside = require('point-in-polygon');
        
// add map background from openstreetmap
L.tileLayer("https://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: ["otile1-s", "otile2-s", "otile3-s", "otile4-s"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="https://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
}).addTo(mymap);

// keep a list of the markers to delete old ones
var mymarkers = [];

function updateMarkers(newMarker) {
    mymarkers.push(newMarker);
    newMarker.addTo(mymap);

    if (mymarkers.length > 100) {
        oldMarker = mymarkers.shift();
        mymap.removeLayer(oldMarker);
    }
}


// create icons for different sentiments
// OLD PATH var image_path = 'http://paillot.info:5000/static/assets/img/';
image_path = 'http://0.0.0.0:5000/static/assets/img/' 

var veryHappyIcon = L.icon({
    iconUrl: image_path + 'very_happy2.png',
    iconSize: [10, 10],
    iconAnchor: [15, 15],
    popupAnchor: [-3, -76]
});
var happyIcon = L.icon({
    iconUrl: image_path + 'happy2.png',
    iconSize: [10, 10],
    iconAnchor: [15, 15],
    popupAnchor: [-3, -76]
});
var neutralIcon = L.icon({
    iconUrl: image_path + 'neutral.png',
    iconSize: [10, 10],
    iconAnchor: [15, 15],
    popupAnchor: [-3, -76]
});
var sadIcon = L.icon({
    iconUrl: image_path + 'sad2.png',
    iconSize: [10, 10],
    iconAnchor: [15, 15],
    popupAnchor: [-3, -76]
})
var verySadIcon = L.icon({
    iconUrl: image_path + 'very_sad.png',
    iconSize: [10, 10],
    iconAnchor: [15, 15],
    popupAnchor: [-3, -76]
});


// wait for page fully loaded
window.addEventListener("load", pageFullyLoaded, false);

function pageFullyLoaded(e) {
    // now fully loaded

    // first create invisible markers so the images are loaded
    L.marker([0, 90], {icon: happyIcon, opacity: 0}).addTo(mymap);
    L.marker([0, 90], {icon: veryHappyIcon, opacity: 0}).addTo(mymap);
    L.marker([0, 90], {icon: neutralIcon, opacity: 0}).addTo(mymap);
    L.marker([0, 90], {icon: sadIcon, opacity: 0}).addTo(mymap);
    L.marker([0, 90], {icon: verySadIcon, opacity: 0}).addTo(mymap);

    // load state layer
    statesData.setStyle({stroke: false, fillOpacity: 0.5});
    statesData.addTo(mymap);

    //alabama.setStyle({fillColor: '#FF0000'});

    // only get tweets if everything else is loaded
    if (!!window.EventSource) {
      // this is requesting a datastream for the tweets
      var source = new EventSource('http://0.0.0.0:5000/tweets');
      source.onmessage = function(e) {
        // this is exectued for every new incoming tweet

        // oparse the json string
        var response = JSON.parse(e.data);

        $("#data").text(response.state);
        // inside([response.coordinates[1],response.coordinates[0]],alabama.geometry)
        alabama.geometry
        
        
        var params = {icon: neutralIcon};
        if (response.sentiment < 2) {
          params = {icon: verySadIcon};
          //curstate=response.state
          //curstate.setStyle({fillColor: '#FF1111'})
          //curstate.addTo(mymap);

        } else if (response.sentiment < 4) {
          params = {icon: sadIcon};
          //curstate=response.state
          //curstate.setStyle({fillColor: '#FF3111'})
          //curstate.addTo(mymap);
          
        } else if (response.sentiment > 7.5) {
          params = {icon: veryHappyIcon};
          //curstate=response.state
        //  curstate.setStyle({fillColor: '#FF6111'})
      //    curstate.addTo(mymap);
          
        } else if (response.sentiment > 6) {
          params = {icon: happyIcon};
    //      curstate=response.state
  //        curstate.setStyle({fillColor: '#FF9111'})
//          curstate.addTo(mymap);
          
        }
        var marker = L.marker([response.coordinates[1],
                               response.coordinates[0]],
                               params);

        updateMarkers(marker);
      }
    }
}

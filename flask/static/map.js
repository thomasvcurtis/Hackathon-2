var geojson;
fetch('{{ geojson }}')
  .then(response => response.json())
  .then(json => geojson = json);
mapboxgl.accessToken =
  "pk.eyJ1IjoidGN1cnRpczIwMDEiLCJhIjoiY2xmNGIxbnZ3MDB4NjN5bzl5dXFheHhsbSJ9.tYigyctoEj13PPZwSQfGig";
const map = new mapboxgl.Map({
  container: "map", // container ID
  // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
  style: "mapbox://styles/mapbox/streets-v12", // style URL
  center: [-74.5, 40], // starting position [lng, lat]
  zoom: 9, // starting zoom
  projection: "mercator",
});

for (const feature of geojson.features) {
  const el = document.createElement('div');
  el.className = 'marker';

  new mapboxgl.Marker(el).setLngLat(feature.geometry.coordinates).addTo(map);
}

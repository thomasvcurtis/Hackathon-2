// Create map
function CreateMap() {
  mapboxgl.accessToken =
  "pk.eyJ1IjoiY3JsaWxseSIsImEiOiJjbGY0YWZ4N2gwcGdwM3FxbWt1dGcxMXh5In0.OrBtfHlPZ09hQHmne6ZFJA";
  const map = new mapboxgl.Map({
    container: "map", // container ID
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: "mapbox://styles/crlilly/clo1lfhpj00ba01oyhvtt20xp",
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 9, // starting zoom
    projection: "mercator",
  });
}
// Add controls to map
map.addControl(new mapboxgl.NavigationControl());


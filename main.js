// Your Mapbox access token (replace this with your actual token)
mapboxgl.accessToken =
  "pk.eyJ1Ijoic3RyaWlkZSIsImEiOiJjbHN1dml6em0wM3E0MmxzMWVwMjNvNDBsIn0.aWXVdLx6iq3ZSSavUicsZA";

// Initialize the map
const map = new mapboxgl.Map({
  container: "map", // container id
  style: "mapbox://styles/mapbox/streets-v11", // style URL
  center: [-74.4464, 40.4883], // starting position [lng, lat]
  zoom: 13, // starting zoom
});

// Function to fetch the path data from Flask API and render it on Mapbox
function getPathData(source, destination) {
  const url = `http://127.0.0.1:5000/calculate?pntdata=${source},${destination}`;

  // Fetch the path from the Flask backend
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const coordinates = data.map((coord) => [coord.lng, coord.lat]); // Format the data for Mapbox

      // Remove the previous route if it exists
      if (map.getSource("path")) {
        map.removeLayer("route");
        map.removeSource("path");
      }

      // Add the new path to the map
      map.addSource("path", {
        type: "geojson",
        data: {
          type: "Feature",
          geometry: {
            type: "LineString",
            coordinates: coordinates,
          },
        },
      });

      map.addLayer({
        id: "route",
        type: "line",
        source: "path",
        layout: {
          "line-join": "round",
          "line-cap": "round",
        },
        paint: {
          "line-color": "#3887be",
          "line-width": 5,
          "line-opacity": 0.75,
        },
      });

      // Fit the map to the bounds of the path
      const bounds = coordinates.reduce((bounds, coord) => {
        return bounds.extend(coord);
      }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));

      map.fitBounds(bounds, { padding: 20 });
    })
    .catch((err) => console.error(err));
}

// Event listener for the "Get Path" button
document.getElementById("getPathBtn").addEventListener("click", () => {
  const source = document.getElementById("source").value;
  const destination = document.getElementById("destination").value;

  getPathData(source, destination);
});

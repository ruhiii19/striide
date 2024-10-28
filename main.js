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

function getPathData(source, destination) {
  console.log(
    `Fetching path data for source: ${source}, destination: ${destination}`
  );
  const url = `http://127.0.0.1:5000/calculate?pntdata=${source},${destination}`;

  console.log(`Sending request to: ${url}`);
  fetch(url)
    .then((response) => {
      console.log("Received response from server");
      return response.json();
    })
    .then((data) => {
      console.log("Parsed JSON data:", data);
      const shortestPath = data.shortest_path;
      const safestPath = data.safest_path;

      const shortestCoordinates = shortestPath.map((coord) => [
        coord.lng,
        coord.lat,
      ]); // Format the data for Mapbox
      const safeCoordinates = safestPath.map((coord) => [coord.lng, coord.lat]); // Format the data for Mapbox

      // Remove the previous routes if they exist
      if (map.getSource("path")) {
        map.removeLayer("route");
        map.removeSource("path");
      }

      if (map.getSource("safePath")) {
        map.removeLayer("safeRoute");
        map.removeSource("safePath");
      }

      // Add the new shortest path to the map
      map.addSource("path", {
        type: "geojson",
        data: {
          type: "Feature",
          geometry: {
            type: "LineString",
            coordinates: shortestCoordinates,
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
          "line-color": "#3887be", // Color for shortest path
          "line-width": 5,
          "line-opacity": 0.75,
        },
      });

      // Add the new safest path to the map
      map.addSource("safePath", {
        type: "geojson",
        data: {
          type: "Feature",
          geometry: {
            type: "LineString",
            coordinates: safeCoordinates,
          },
        },
      });

      map.addLayer({
        id: "safeRoute",
        type: "line",
        source: "safePath",
        layout: {
          "line-join": "round",
          "line-cap": "round",
        },
        paint: {
          "line-color": "#ff0000", // Color for safest path
          "line-width": 5,
          "line-opacity": 0.75,
        },
      });

      // Fit the map to the bounds of both paths
      const bounds = new mapboxgl.LngLatBounds();
      shortestCoordinates.forEach((coord) => bounds.extend(coord));
      safeCoordinates.forEach((coord) => bounds.extend(coord));

      map.fitBounds(bounds, { padding: 20 });
    })
    .catch((err) => {
      console.error("Error fetching or processing data:", err);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded");

  const getPathBtn = document.getElementById("getPathBtn");
  getPathBtn.addEventListener("click", () => {
    const source = document.getElementById("source").value;
    const destination = document.getElementById("destination").value;
    console.log(
      `Button clicked: Source: ${source}, Destination: ${destination}`
    );
    getPathData(source, destination);
  });
});

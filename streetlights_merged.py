"""from pyproj import CRS, Transformer

# Define the CRS
crs_wgs84 = CRS.from_epsg(4326)  # WGS 84 (lat/lon)
crs_utm = CRS.from_epsg(32619)   # UTM zone 19N for Boston

# Create a Transformer object
transformer = Transformer.from_crs(crs_wgs84, crs_utm, always_xy=True)

def latlon_to_utm(lon, lat):
    return transformer.transform(lon, lat)

####################################################################################################

#PARSING OSM FILE

import xml.etree.ElementTree as ET

# Parse the OSM file
tree = ET.parse('data/boston_sidewalks.osm')
root = tree.getroot()

# Extract nodes with their coordinates
sidewalk_nodes = {}
for node in root.findall('node'):
    node_id = node.attrib['id']
    lat = float(node.attrib['lat'])
    lon = float(node.attrib['lon'])
    # Convert to UTM
    x, y = latlon_to_utm(lon, lat)
    sidewalk_nodes[node_id] = (x, y)





####################################################################################################
import json

# PARSING STREETLIGHT DATA

# Load streetlight data
with open('data/lights_merged.json') as f:
    streetlight_data = json.load(f)

# Extract streetlight coordinates and properties
streetlights = []


# Loop through features in the JSON file
for feature in streetlight_data['features']:
    geometry = feature.get('geometry', None)
    
    # Check if geometry and coordinates exist
    if geometry is not None and geometry.get('coordinates') is not None:
        coordinates = geometry['coordinates']
        
        # Check if coordinates has the expected length
        if len(coordinates) >= 2:
            x, y = coordinates[:2]  # Only extract x and y, ignoring any extra values
            pole_id = feature['properties']['pole_id']
            height = feature['properties']['height']

            # Append valid streetlight data
            streetlights.append({
                'id': pole_id,
                'coordinates': (x, y),
                'height': height
            })
        else:
            print(f"Invalid coordinates for feature with pole_id {feature['properties']['pole_id']}: {coordinates}")
    else:
        print(f"Missing geometry or coordinates for feature with pole_id {feature['properties']['pole_id']}")



####################################################################################################

#mapping streetlights to nearest sidewalk

from shapely.geometry import Point, LineString

# Function to find the nearest sidewalk segment for a given streetlight
def nearest_sidewalk(light_point, G):
    nearest_edge = None
    min_distance = float('inf')
    
    for edge in G.edges(data=True):
        node1 = G.nodes[edge[0]]['pos']  # Assuming 'pos' holds the (x, y) coordinates
        node2 = G.nodes[edge[1]]['pos']
        sidewalk_segment = LineString([node1, node2])

        distance = light_point.distance(sidewalk_segment)
        if distance < min_distance:
            min_distance = distance
            nearest_edge = edge
    
    return nearest_edge, min_distance"""





import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import convertJSON as cj
import astar as algo
import json

app = Flask(__name__)
CORS(app)

# Set up logging to log only to file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('astar_log.txt')
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Load streetlight data at startup
streetlights = []
try:
    with open('data/lights_merged.json') as f:
        streetlight_data = json.load(f)
        streetlights = streetlight_data['features']  # Ensure the correct format of the GeoJSON file
    logger.info("Streetlight data loaded successfully")
except Exception as e:
    logger.error(f"Failed to load streetlight data: {str(e)}")

@app.route('/calculate', methods=['GET'])
def home():
    logging.info("Received request for /calculate")
    raw_input = request.args.get('pntdata')
    
    if not raw_input:
        logging.error("No input data provided.")
        return jsonify({"error": "No input data provided."}), 400
    
    logging.info(f"Input data: {raw_input}")
    
    try:
        raw_input = raw_input.split(',')
        if len(raw_input) != 4:
            raise ValueError("Input must contain exactly four values.")
        
        inputSourceLoc = (float(raw_input[0]), float(raw_input[1]))  # (lat, lon)
        inputDestLoc = (float(raw_input[2]), float(raw_input[3]))  # (lat, lon)
        
        logging.info(f"Source: {inputSourceLoc}, Destination: {inputDestLoc}")

        mappedSourceLoc = cj.getKNN(inputSourceLoc)
        mappedDestLoc = cj.getKNN(inputDestLoc)
        
        logging.info(f"Mapped Source: {mappedSourceLoc}, Mapped Destination: {mappedDestLoc}")

        # Convert streetlight coordinates (if needed, if they are already in UTM format, skip this)
        logging.info("Using existing streetlight coordinates (already in UTM)")

        # Calculate shortest path
        logging.info("Calculating shortest path")
        shortest_path = algo.aStar(mappedSourceLoc, mappedDestLoc)
        shortest_finalPath, shortest_cost = cj.getResponsePathDict(shortest_path, mappedSourceLoc, mappedDestLoc)
        
        # Calculate safest path using converted streetlight data
        logging.info("Calculating safest path")
        safest_path = algo.aStar_safe(mappedSourceLoc, mappedDestLoc, streetlights)
        safest_finalPath, safest_cost = cj.getResponsePathDict(safest_path, mappedSourceLoc, mappedDestLoc)
        
        logging.info(f"Shortest path cost: {shortest_cost}, Safest path cost: {safest_cost}")
        
        response = {
            'shortest_path': shortest_finalPath,
            'shortest_cost': shortest_cost,
            'safest_path': safest_finalPath,
            'safest_cost': safest_cost
        }
        logging.info("Sending response")
        return jsonify(response)
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("Starting Flask server")
    app.run(host='0.0.0.0', debug=True)

import logging
import heapq as heap
import time
import convertJSON as cj
import math
import pyproj

# Set up logging
logging.basicConfig(filename='astar_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def aStar(source, destination):
    logging.info(f"Starting A* algorithm for source: {source}, destination: {destination}")
    
    if source == destination:
        logging.info("Source and destination are the same. Returning empty path.")
        return {}
    
    open_list = []
    g_values = {}
    path = {}
    closed_list = {}
    
    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])
    
    logging.info(f"Source ID: {sourceID}, Destination ID: {destID}")
    
    g_values[sourceID] = 0
    h_source = cj.calculateHeuristic(source, destination)
    heap.heappush(open_list, (h_source, sourceID))
    
    start_time = time.time()
    iterations = 0
    while open_list:
        iterations += 1
        if iterations % 1000 == 0:
            logging.info(f"A* iteration: {iterations}")
        
        f_value, curr_state = heap.heappop(open_list)
        closed_list[curr_state] = ""

        if curr_state == destID:
            logging.info("A* reached the goal")
            break 
        
        nbrs = cj.getNeighbours(curr_state, destination)
        for eachNeighbour in nbrs.get(curr_state, []):
            neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon = cj.getNeighbourInfo(eachNeighbour)
            current_inherited_cost = g_values[curr_state] + neighbourCost

            if neighbourId in closed_list:
                continue
            
            if neighbourId not in g_values or current_inherited_cost < g_values[neighbourId]:
                g_values[neighbourId] = current_inherited_cost
                f_value = neighbourHeuristic + current_inherited_cost
                heap.heappush(open_list, (f_value, neighbourId))
                
                path[str(neighbourLatLon)] = {"parent": str(cj.getLatLon(curr_state)), "cost": neighbourCost}
    
    logging.info(f"A* completed in {time.time() - start_time} seconds")
    return path

def aStar_safe(source, destination, streetlights, streetlight_radius=50, safety_weight=0.5):
    open_list = []
    g_values = {}
    path = {}
    closed_list = {}

    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])
    
    g_values[sourceID] = 0
    h_source = cj.calculateHeuristic(source, destination)
    open_list.append((h_source, sourceID))

    s = time.time()
    
    while len(open_list) > 0:
        curr_state = open_list[0][1]
        heap.heappop(open_list)
        closed_list[curr_state] = ""

        if curr_state == destID:
            logging.info("Reached the goal")
            break

        nbrs = cj.getNeighbours(curr_state, destination)
        values = nbrs.get(curr_state, [])
        for eachNeighbour in values:
            neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon = cj.getNeighbourInfo(eachNeighbour)
            current_inherited_cost = g_values[curr_state] + neighbourCost

            if neighbourId in closed_list:
                continue

            # Calculate streetlight influence within radius using latitude and longitude
            safety_score = 0
            # Convert UTM back to latitude and longitude for the neighbor
            neighbour_latlon = cj.convert_from_utm(neighbourLatLon[0], neighbourLatLon[1])
            
            for streetlight in streetlights:
                # Convert streetlight UTM coordinates to latitude and longitude
                streetlight_latlon = cj.convert_from_utm(streetlight['geometry']['coordinates'][1], 
                                                          streetlight['geometry']['coordinates'][0])
                distance_to_streetlight = math.sqrt((neighbour_latlon[0] - streetlight_latlon[0]) ** 2 +
                                                    (neighbour_latlon[1] - streetlight_latlon[1]) ** 2)
                if distance_to_streetlight <= streetlight_radius:
                    safety_score += (streetlight_radius - distance_to_streetlight) / streetlight_radius

            # Combine distance cost and safety score
            combined_cost = current_inherited_cost + (safety_weight * (1 - safety_score))

            # Calculate f-value for the priority queue
            neighbourFvalue = neighbourHeuristic + combined_cost

            # Only add to open list if not already in there or if we found a cheaper path
            if neighbourId not in g_values or current_inherited_cost < g_values[neighbourId]:
                g_values[neighbourId] = current_inherited_cost
                open_list.append((neighbourFvalue, neighbourId))

                # Update the path
                path[str(neighbour_latlon)] = {
                    "parent": str(cj.getLatLon(curr_state)),
                    "cost": neighbourCost
                }

        open_list = list(set(open_list))  # Remove duplicates
        heap.heapify(open_list)

    logging.info(f"Time taken to find path (in seconds): {time.time() - s}")
    return path

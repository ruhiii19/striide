import convertJSON as cj
import heapq as heap
import time

def aStar(source, destination):
    open_list = []
    g_values = {}
    path = {}
    closed_list = {}
    
    sourceID = cj.getOSMId(source[0], source[1])
    destID = cj.getOSMId(destination[0], destination[1])
    
    g_values[sourceID] = 0
    h_source = cj.calculateHeuristic(source, destination)
    heap.heappush(open_list, (h_source, sourceID))
    
    s = time.time()
    while open_list:
        f_value, curr_state = heap.heappop(open_list)
        closed_list[curr_state] = ""
        
        if curr_state == destID:
            print("We have reached the goal")
            break 
        
        nbrs = cj.getNeighbours(curr_state, destination)
        values = nbrs[curr_state]
        for eachNeighbour in values:
            neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon = cj.getNeighbourInfo(eachNeighbour)
            current_inherited_cost = g_values[curr_state] + neighbourCost
    
            if neighbourId in closed_list:
                continue
            
            # If it's a better path to the neighbor, process it
            if neighbourId not in g_values or current_inherited_cost < g_values[neighbourId]:
                g_values[neighbourId] = current_inherited_cost
                f_value = neighbourHeuristic + current_inherited_cost
                heap.heappush(open_list, (f_value, neighbourId))
                
                path[str(neighbourLatLon)] = {"parent": str(cj.getLatLon(curr_state)), "cost": neighbourCost}
    
    print("Time taken to find path (in seconds): " + str(time.time() - s))
    return path

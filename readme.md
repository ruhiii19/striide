
__Data:__
* Data has been extracted from [OSM](https://www.openstreetmap.org/).<br> 
* It contains ~27k nodes and ~63k edges <br>
* _Bounded by :- min: (40.4961000, -74.5015000); max: (40.5333000, -74.4143000)_ <br>
* More on data:
  * Data provided by OSM is in __.osm__ format, which is nothing but the XML file. 
  * Converted this file to lighter XML _(.graphml)_ file, which can be parsed easily as compared to .osm. [Code] <br>
  * Used OSMNX for this -> [OSMNX Documentation](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.core.graph_from_file) <br>
  * This .graphml file will be used for rest of the tasks. <br>
  * [convertJSON.py](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py) is helper class which contains all the methods which we will be needed to achieve the task. <br>
    - [getLatLon](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L13) - to get latitude and longitude of a node by passing its OSMId. <br>
    - [getOSMId](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L22) - to get OSMId of the node from its latitude and longitude. <br>
    - [calculateHeuristic](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L32) - gives heuristic value from the given node to destination. <br>
      - Heuristic used:- __Haversine__ (also called as "As crow flies" distance.) <br>
    - [getNeighbours](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L35) - it generates all the neighbours of the given node(given its OSMId).
    - [getNeighbourInfo](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L60) - helper function to extract informtation of the particular neighbour while implementing A*.
    - [getKNN](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L75) - it finds K-Nearest Neighbour(s) of particular node (given its coordinates).
      - Why do we need it?:- 
        - Application allows users to select any marker on map. So, there might be case that marker selected by user is not present in nodes of our _.graphml_ file. So, in order to make algorithm work - I have used [KD Tree library from sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn-neighbors-kdtree) <br>
        - The first index of the output given by _KDTree_ is the most nearest node to the given node. <br> _for example:_ if we were to find nearest neighbour of the point (40.48834484237183,-74.4464808486693), which is not there in our .osm file. Then output will be [0.00662018 0.00676685 0.00680585] and  first index of the output is nearest and corresponding node is (40.492516, -74.4413367).
    - [getResponsePathDict](https://github.com/vraj152/googlemapsastar/blob/63c0d686ee192ef10623a42097e52e07cf7f28ab/convertJSON.py#L91) - helper function in order to get the final path from source to destination.

__Algorithm: A*__

__Output:__

* Due to larger number of nodes present in a map-snippet, A* becomes really slow. As it highly depends on branching factor : __O(b^d)__ 
* Hence, it works really well when source and destination are placed nearby.

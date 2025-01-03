
# !/usr/bin/env python3
import sys

from collections import defaultdict
import math
import heapq


#global road, heuristic_distance, coodinates_cache
heuristic_distance = {}
coodinates_cache ={}

def plotroadsegmentsroad(filename):

    road = defaultdict(list)
    
    with open(filename, 'r') as file:

        for line in file:
            
            sentence = line.split()
            
            city1 = sentence[0]
            
            city2 = sentence[1]
            
            length = float(sentence[2])
           
            speedLimit = float(sentence[3])
            
            Highway = sentence[4]



            road[city1].append((city2, length, speedLimit, Highway))


            road[city2].append((city1, length, speedLimit, Highway))

    return road

def getlatitudelongitudehelper(target_city):
    #print(target_city)
    
    filename ='city-gps.txt'

    with open(filename, 'r') as file:
        
        for line in file:

            sentence = line.split()

            #print(sentence)

            city_name = sentence[0]

            latitude = float(sentence[1])

            longitude = float(sentence[2])

            if city_name == target_city:


                return latitude, longitude
            


    return None

def getNeighborCoordinates(city, road):
    neighbors = []
    

    for neighbor, length, speedLimit, Highway in road.get(city, []):
        
        
        coords = getlatitudelongitudehelper(neighbor)
    

            
        neighbors.append((coords,neighbor, length, speedLimit, Highway ))
    
    return neighbors



def GetLatitudeLongitude(target_city, road):
    
    if target_city in coodinates_cache:
        
        return coodinates_cache[target_city]
   
    coordinates = getlatitudelongitudehelper(target_city)
    
    if coordinates is not None:
        coodinates_cache[target_city] = coordinates
        return coordinates  

    #print(123, target_city)
    neighbors = getNeighborCoordinates(target_city, road)
    
    if neighbors:
        
        coordinates = EstimateCoordinateWithWeightedAverage(neighbors)

        if coordinates is not None:
            coodinates_cache[target_city] = coordinates

        return coordinates
    
    return None 



def EstimateCoordinateWithWeightedAverage(neighbors):
  
    if not neighbors[0]:
        
        return None
        
    total = 0

    weightedLatitude = 0

    weightedLongitude = 0
    
    for  coords, neighbor, distance, speedLimit, Highway  in neighbors:
       
        if coords is not  None:

            lat, lon = coords
            
            weight = 1.0 / max(distance, 0.1)

            weightedLatitude += lat * weight

            weightedLongitude += lon * weight

            total += weight
    
    if total == 0:
        
        return None
    #print(weightedLatitude/total, weightedLongitude/total)
    return (weightedLatitude/total, weightedLongitude/total)



def distanceCalculationbtwCities(city1, city2, road):
    
    if (city1, city2) in heuristic_distance:
        return heuristic_distance[(city1, city2)]
    

    
    
    coord1 = GetLatitudeLongitude(city1, road)
    coord2 = GetLatitudeLongitude(city2, road)
    
    if coord1 is None or coord2 is None:
       
        return 0  
    

    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 3959  
    latdifference = math.radians(lat2 - lat1)
    longdifference = math.radians(lon2 - lon1)
    a = math.sin(latdifference / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(longdifference / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    heuristic_distance[(city1, city2)] = distance  # Cache result
    return distance



def calculate_cost(distance=0, speedLimit=0, cost='distance'):
    if cost == "segments":
        return 1
    elif cost == "distance":
        return distance
    elif cost == "time":
        return distance/ (speedLimit +5)  # Remove +5 adjustment
    elif cost == "delivery":
        probaccident = 0.000001 *  (speedLimit +5) 
        return probaccident * distance




def AstarSearch(source_city, destination_city, cost, road):
    
    open_list = []
    start = source_city
    
    
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0


    totaltime = defaultdict(lambda: float('inf'))
    totaltime[start] = 0

    totalsegments = defaultdict(lambda: float('inf'))
    totalsegments[start] = 0   

    totaldistance = defaultdict(lambda: float('inf'))
    totaldistance[start] = 0 

    totalaccidents = defaultdict(lambda: float('inf'))
    totalaccidents[start] = 0     


    visited = set()
    
    # Initial state
    g_score = 0


    h_score = distanceCalculationbtwCities(source_city, destination_city, road)
  

    f_score = g_score + calculate_cost(h_score,0,cost)

    
    # Push initial state: (fcost, time_count, current_city, accumulated_distance, accumulated_time, highway)
    heapq.heappush(open_list, (f_score, 0, start))
    
    came_from = {}

    while open_list:

        _, curr_time, current = heapq.heappop(open_list)

 
        
        if current == destination_city:

            return reconstruct_path(came_from, start, current)
            
        #if current not in visited  :  # Only process unvisited nodes

        for coord, neighbor, length, speedLimit, Highway in getNeighborCoordinates(current, road):
            
            # Calculate new time cost properly
            new_time = totaltime[current] + (length/speedLimit)  # Remove +5 adjustment
            new_segments = totalsegments[current] +1
            new_distance = totaldistance[current] + length
            new_accidents = totalaccidents[current] +  0.000001 * (speedLimit +5) * length

            IsBetterNode = False

    
            if cost == "time" and new_time < totaltime[neighbor]:
                g_score = new_time
                IsBetterNode = True
            elif cost == "segments" and new_segments < totalsegments[neighbor]:
                g_score = new_segments
                IsBetterNode = True
            elif cost == "distance" and new_distance  < totaldistance[neighbor]:
                g_score = new_distance
                IsBetterNode = True
            elif cost == "delivery" and new_accidents < totalaccidents[neighbor]:
                g_score = new_accidents
                IsBetterNode = True                    
            
            # Update node if better time found
            if IsBetterNode:

                came_from[neighbor] = (current, length, speedLimit, Highway)
                
                totaltime[neighbor] = new_time
                
                totalsegments[neighbor] = new_segments
                
                totaldistance[neighbor] = new_distance
                
                totalaccidents[neighbor] = new_accidents
                
                
                
                # Calculate f_score with proper heuristic
                h_score = distanceCalculationbtwCities(neighbor, destination_city, road)
                

                    
                f_score = g_score + calculate_cost(h_score, speedLimit, cost)

                heapq.heappush(open_list, (f_score, curr_time + 1, neighbor))
                    
            
            visited.add(current)

    return None






def reconstruct_path(came_from, start, current):
    total_segments =0 
    total_miles =0 
    total_hours =0 
    total_expected_accidents =0 
    
    path = []
    while current in came_from:
        
        prev_city, length, speedLimit, Highway = came_from[current]
        path.append((current, Highway + ' for ' + str(int(length))  + ' miles' + ' for ' + str(speedLimit,)  + ' mph'))
        total_segments += 1
        total_miles += length
        total_expected_accidents += 0.000001 * speedLimit * length
        total_hours += length / max(speedLimit, 1)
        current = prev_city
    
    path.append(start)
    
    path.reverse()
    
    return total_segments, total_miles, round(total_hours,4), total_expected_accidents, path


def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-expected-accidents": a float indicating the expected (average) accidents
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    road = plotroadsegmentsroad('road-segments.txt')

    result = AstarSearch(start, end, cost, road)

    if not result:

        return None

    total_segments, total_miles, total_hours, total_expected_accidents, path = result




    route_taken = path[1:]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-expected-accidents" : total_expected_accidents, 
            "route-taken" : path[1:]}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total expected accidents: %8.3f" % result["total-expected-accidents"])



# Optimal Route Finder: A* Search with Multi-Cost Optimization

This project implements an intelligent route-finding algorithm using **A* Search**. It incorporates flexible cost functions, robust data handling, and optimized performance, making it suitable for real-world navigation problems.

---

## Problem Abstraction

### Key Elements:
1. **Valid States**:  
   Any city in the road network that can be reached via connected road segments. Each segment includes details such as distance, speed limit, and highway name.

2. **Initial State**:  
   The starting city, as specified by the user, and the chosen cost function (segments, distance, time, or delivery).

3. **Goal State**:  
   Reaching the destination city while optimizing the path according to the specified cost function.

4. **Successor Function**:  
   For any city, valid successors are all neighboring cities connected by road segments.

5. **Cost Functions**:  
   The program supports four distinct cost optimization strategies:
   - **Segments**: Minimize the number of road segments.
   - **Distance**: Minimize total miles traveled.
   - **Time**: Minimize travel time based on speed limits.
   - **Delivery**: Minimize expected accidents based on speed and distance.

---

## Implementation Overview

### A* Search Algorithm:
- Utilizes a priority queue to explore paths based on the formula:  
  \( f(n) = g(n) + h(n) \)  
  - \( g(n) \): Actual cost from the start to the current city.  
  - \( h(n) \): Heuristic estimate (straight-line distance) to the goal city.
- Employs **heapq** for efficient priority queue management.  
- Implements a robust heuristic using the haversine formula for distance estimation.

### GPS Coordinate Management:
- **Source**: City coordinates from `city-gps.txt`.  
- **Handling Missing Data**: Estimates missing coordinates using weighted averages of neighboring cities.  
- **Caching**: Speeds up repeated distance and coordinate lookups.

### Distance Calculations:
- Uses the haversine formula for accurate great-circle distances.  
- Caches previously calculated distances for efficiency.

---

## Dataset Description

### **city-gps.txt**
This file contains GPS data for cities in North America (mostly U.S. cities). Each line in the file corresponds to one city and includes three fields:
- **City Name**: The name of the city.
- **Latitude**: The latitude of the city.
- **Longitude**: The longitude of the city.

Example:
Chicago 41.8781 -87.6298 LosAngeles 34.0522 -118.2437 ...


### **road-segments.txt**
This file defines road segments that connect pairs of cities. Each line contains:
- **First City**: The starting city of the road segment.
- **Second City**: The destination city of the road segment.
- **Length (in miles)**: The length of the road segment.
- **Speed Limit (in miles per hour)**: The speed limit on the road segment.
- **Highway Name**: The name of the highway on the road segment.

Example:
Chicago LosAngeles 2000 60 I-80 LosAngeles NewYork 2500 65 I-10 ...


### **Handling Data Issues**
There are some common issues in the dataset that need to be addressed:
- **Missing GPS Data**: Some cities in the road-segments.txt file may not have corresponding GPS data in city-gps.txt. In such cases, the program estimates the missing coordinates using weighted averages of neighboring cities' coordinates to maintain route-finding accuracy.
- **Bidirectional Roads**: The road segments are bidirectional, meaning that travel from one city to another can be made in either direction with the same road properties (distance and speed limit).
- **Data Integrity**: The code is designed to handle and bypass any errors or missing data in the files to ensure robustness in route finding. For instance, if a road segment has no corresponding city coordinates, the system continues by estimating the location based on neighboring cities, ensuring the algorithm can still find a path.

---

## Key Features

1. **Efficient Path Finding**:  
   - Implements **A* Search** for optimal route discovery.  
   - Handles large datasets with efficient data structures and caching.  

2. **Support for Multiple Cost Functions**:
   - **Segments**: Optimized for the fewest road segments.  
   - **Distance**: Calculates actual road segment lengths.  
   - **Time**: Accounts for travel time using speed limits (with a 5 mph buffer).  
   - **Delivery**: Incorporates accident probabilities based on speed and distance.

3. **Advanced GPS Data Handling**:
   - Implements robust mechanisms for estimating missing GPS coordinates.  
   - Uses weighted averages based on neighboring cities.  
   - Caches estimated coordinates to improve runtime efficiency.

4. **Performance Optimization**:
   - Caches both coordinate estimations and distance calculations.  
   - Uses `defaultdict` for efficient road network representation.  
   - Prioritizes performance without compromising accuracy.

---

## Challenges and Solutions

1. **Missing Coordinates**:
   - **Challenge**: Some cities lacked GPS data.  
   - **Solution**: Implemented weighted average estimation for missing coordinates and cached results for reuse.

2. **Performance Bottlenecks**:
   - **Challenge**: Calculating distances repeatedly caused delays.  
   - **Solution**: Cached calculated distances and used efficient data structures such as `heapq` for priority queue management.

3. **Flexible Cost Functions**:
   - **Challenge**: Supporting multiple cost functions with consistent calculations.  
   - **Solution**: Designed a modular and scalable cost-calculation system with tailored heuristics for each function.

---

## Program Structure

1. **Core Functions**:
   - `get_route()`: Main interface for route finding.  
   - `AstarSearch()`: Implements the A* Search algorithm.  
   - `calculate_cost()`: Handles logic for multiple cost functions.  
   - `distanceCalculationbtwCities()`: Computes great-circle distances.

2. **Helper Functions**:
   - `plotroadsegmentsroad()`: Parses and loads road network data.  
   - `GetLatitudeLongitude()`: Retrieves or estimates city coordinates.  
   - `EstimateCoordinateWithWeightedAverage()`: Handles GPS coordinate estimation.

---

## Assumptions

1. The road network is connected and undirected, ensuring solvability for all test cases.  
2. Speed limits and distances are positive values.  
3. Missing GPS data is estimated with high accuracy using neighboring cities.

---

## Results

The program successfully finds optimal routes based on the specified cost function while handling missing data gracefully. It demonstrates efficient pathfinding and accurate distance calculations.

### Example Use Cases:
- **Segments Optimization**: Routes that minimize road changes.  
- **Distance Optimization**: Routes that minimize travel distance.  
- **Time Optimization**: Routes with the fastest travel time.  
- **Delivery Optimization**: Routes that minimize expected accidents.

---

## Conclusion

This project demonstrates my ability to design and implement efficient algorithms for real-world applications. The use of **A* Search**, robust data handling techniques, and optimized performance showcases expertise in Python, data structures, and algorithm design.

---

## Key Skills Demonstrated:
- **Algorithm Design**: A* Search implementation with heuristic optimization.  
- **Data Handling**: Robust management of incomplete GPS data.  
- **Performance Optimization**: Use of caching and efficient data structures.  
- **Software Design**: Modular implementation with support for scalability.


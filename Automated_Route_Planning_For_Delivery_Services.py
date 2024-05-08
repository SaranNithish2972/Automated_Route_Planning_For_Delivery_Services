import heapq
import hashlib
from geopy.distance import geodesic
import csv

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}
    def add_node(self, value):
        self.nodes.add(value)
    def add_edge(self, from_node, to_node, distance):
        self.edges.setdefault(from_node, []).append(to_node)
        self.edges.setdefault(to_node, []).append(from_node)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance
    def dijkstra_shortest_path(self, initial):
        shortest_distances = {}
        for node in self.nodes:
            shortest_distances[node] = float('inf')
        shortest_distances[initial] = 0
        h = [(0, initial)]
        while h:
            (distance, node) = heapq.heappop(h)
            if distance > shortest_distances[node]:
                continue
            for neighbor in self.edges[node]:
                new_distance = distance + self.distances[(node, neighbor)]
                if new_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = new_distance
                    heapq.heappush(h, (new_distance, neighbor))
        return shortest_distances
def calculate_hash(value):
    return hashlib.md5(str(value).encode()).hexdigest()
def calculate_distance(coords1, coords2):
    return geodesic(coords1, coords2).meters
def backtrack_assignments(vehicle_assignments, delivery_locations, shortest_distances, visited_locations=set(), memo={}):
    # Check if all delivery locations have been assigned
    if len(visited_locations) == len(delivery_locations):
        return True
    # Generate a hash for the current route configuration
    route_hash = calculate_hash([(v, v_info["route"]) for v, v_info in vehicle_assignments.items()])
    if route_hash in memo:
        return memo[route_hash]
    for vehicle, v_info in vehicle_assignments.items():
        current_location = v_info["route"][-1]
        min_distance = float('inf')
        min_location = None
        for location in delivery_locations:
            if location not in visited_locations:
                distance_to_location = shortest_distances[current_location][location]
                if distance_to_location < min_distance:
                    min_distance = distance_to_location
                    min_location = location
        if min_location:
            info = delivery_locations[min_location]
            if v_info["remaining_capacity"] >= info["demand"]:
                v_info["route"].append(min_location)
                v_info["remaining_capacity"] -= info["demand"]
                v_info["total_distance"] += min_distance
                visited_locations.add(min_location)
                # Recursive call to assign the next location
                if backtrack_assignments(vehicle_assignments, delivery_locations, shortest_distances, visited_locations, memo):
                    memo[route_hash] = True
                    return True

                # If the assignment does not lead to a solution, backtrack
                v_info["route"].pop()
                v_info["remaining_capacity"] += info["demand"]
                v_info["total_distance"] -= min_distance
                visited_locations.remove(min_location)
    memo[route_hash] = False
    return False
def print_distances(delivery_locations, vehicle_assignments):
    print("\nVehicle assignments, distances, and remaining capacity:")
    for vehicle, info in vehicle_assignments.items():
        route = info['route']
        total_distance = 0
        for i in range(len(route) - 1):
            start_location = route[i]
            end_location = route[i + 1]
            start_coords = delivery_locations[start_location]['coordinates']
            end_coords = delivery_locations[end_location]['coordinates']
            distance = calculate_distance(start_coords, end_coords)
            total_distance += distance
            print(f"{vehicle}: {start_location} -> {end_location} - Distance: {distance:.2f} meters")
        print(f"Total distance for {vehicle}: {total_distance:.2f} meters")
        print(f"Remaining capacity for {vehicle}: {info['remaining_capacity']}")
# Function to read sample data from CSV
def read_sample_data_from_csv(file_path):
    delivery_locations = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location = row['Location']
            latitude = float(row['Latitude'])
            longitude = float(row['Longitude'])
            demand = int(row['Demand'])
            coordinates = (latitude, longitude)
            delivery_locations[location] = {"coordinates": coordinates, "demand": demand}
    return delivery_locations
# Sample data file path
sample_data_file = 'delivery_locations.csv'
# Read sample data from CSV
delivery_locations = read_sample_data_from_csv(sample_data_file)
vehicles = {
    "Vehicle1": {"capacity": 50, "start_location": "Coimbatore Railway Station"},
    "Vehicle2": {"capacity": 50, "start_location": "Coimbatore International Airport"}
}
# Create graph and add nodes and edges
graph = Graph()
for location, loc_info in delivery_locations.items():
    graph.add_node(location)
    for other_location, other_info in delivery_locations.items():
        if location != other_location:
            distance = calculate_distance(loc_info["coordinates"], other_info["coordinates"])
            graph.add_edge(location, other_location, distance)
# Use Dijkstra's algorithm to find shortest distances between all pairs of locations
shortest_distances = {}
for location in delivery_locations.keys():
    shortest_distances[location] = graph.dijkstra_shortest_path(location)
# Reset vehicle assignments
vehicle_assignments = {}
for vehicle, info in vehicles.items():
    vehicle_assignments[vehicle] = {"route": [info["start_location"]], "remaining_capacity": info["capacity"], "total_distance": 0}
# Perform backtracking for assignments
if not backtrack_assignments(vehicle_assignments, delivery_locations, shortest_distances):
    print("No feasible assignment found.")
else:
    print_distances(delivery_locations, vehicle_assignments)
import folium
def plot_routes_on_map(delivery_locations, vehicle_assignments):
    # Create a map centered around Coimbatore
    m = folium.Map(location=[11.0168, 76.9558], zoom_start=12)
    # Add markers for delivery locations
    for location, loc_info in delivery_locations.items():
        folium.Marker(loc_info['coordinates'], popup=location).add_to(m)
    # Define custom icons for vehicles
    icons = {
        "Vehicle1": folium.Icon(color='green', icon='truck', prefix='fa'),  # Green car icon for Vehicle1
        "Vehicle2": folium.Icon(color='blue', icon='truck', prefix='fa')  # Blue truck icon for Vehicle2
    }

    # Add routes for each vehicle
    for vehicle, info in vehicle_assignments.items():
        route = info['route']
        route_coords = [delivery_locations[loc]['coordinates'] for loc in route]
        folium.PolyLine(locations=route_coords, color='blue', weight=5, opacity=0.7, popup=vehicle).add_to(m)
        # Add vehicle name as a marker with custom icon at the start of the route
        start_location = route[0]
        start_coords = delivery_locations[start_location]['coordinates']
        folium.Marker(start_coords, icon=icons[vehicle], popup=vehicle).add_to(m)
    # Save the map to an HTML file
    m.save('vehicle_routes_map.html')
# Call the function to plot routes on the map
plot_routes_on_map(delivery_locations, vehicle_assignments)

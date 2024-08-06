# Databricks notebook source
import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great-circle distance between two points
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

class Node:
    def __init__(self, city, g=0, h=0, parent=None):
        self.city = city  # The name of the city
        self.g = g  # Cost from the start node to the current node
        self.h = h  # Heuristic cost from the current node to the goal
        self.f = g + h  # Estimated total cost (f = g + h)
        self.parent = parent  # The parent node in the path
        print(f"Node created: {self.city}, g: {self.g}, h: {self.h}, f: {self.f}")
    
    def __lt__(self, other):
        # Less-than operator for sorting nodes by their f value
        return self.f < other.f

def rbfs(problem, node, f_limit):
    print(f"\nRBFS called with node: {node.city}, f_limit: {f_limit}, f: {node.f}")
    
    successors = []
    if problem.goal_test(node):
        print(f"Goal found: {node.city} with cost: {node.g}")
        return node, node.f  # Solution found, return the node and cost
    
    for succ in problem.get_successors(node):
        successors.append(succ)  # Generate all successors of the current node
    
    if not successors:
        print(f"No successors for node: {node.city}")
        return None, float('inf')  # No successors, return failure with infinite cost
    
    for succ in successors:
        succ.f = max(succ.f, node.f)  # Update f value of successors to be at least the parent's f value
        print(f"Updated successor {succ.city} with f: {succ.f}")
    
    while True:
        successors.sort()  # Sort successors by their f value
        best = successors[0]  # Best successor (lowest f value)
        print(f"Best successor: {best.city}, f: {best.f}")
        
        if best.f > f_limit:
            print(f"Best f value {best.f} exceeds f_limit {f_limit}")
            return None, best.f  # Best node exceeds the limit, return failure and best alternative
        
        alternative = successors[1].f if len(successors) > 1 else float('inf')
        print(f"Alternative f value: {alternative}")
        
        result, best.f = rbfs(problem, best, min(f_limit, alternative))
        
        if result is not None:
            return result, best.f  # If a solution is found, return it

class RouteProblem:
    def __init__(self, start, goal, locations, road_map):
        self.start = start  # Start city
        self.goal = goal  # Goal city
        self.locations = locations  # Dictionary of city locations (latitude, longitude)
        self.road_map = road_map  # Dictionary of roads and distances between cities
    
    def goal_test(self, node):
        print(f"Checking if {node.city} is goal: {self.goal}")
        return node.city == self.goal  # Check if the current node is the goal
    
    def get_successors(self, node):
        print(f"Generating successors for node: {node.city}")
        successors = []
        for next_city in self.road_map[node.city]:
            g = node.g + self.road_map[node.city][next_city]  # Calculate g cost
            h = haversine(self.locations[next_city][0], self.locations[next_city][1], self.locations[self.goal][0], self.locations[self.goal][1])  # Calculate h cost
            successors.append(Node(next_city, g, h, node))  # Create successor node
            print(f"Successor generated: {next_city}, g: {g}, h: {h}, f: {g+h}")
        return successors

def reconstruct_path(node):
    print(f"Reconstructing path for node: {node.city}")
    path = []
    while node:
        path.append(node.city)  # Add current city to the path
        node = node.parent  # Move to the parent node
    return path[::-1]  # Reverse the path to get it from start to goal

def main():
    # Cities and their coordinates
    locations = {
        'Panji': (15.4909, 73.8278),
        'Raichur': (16.2076, 77.3463),
        'Mangalore': (12.9141, 74.8560),
        'Bellari': (15.1394, 76.9214),
        'Tirupati': (13.6288, 79.4192),
        'Kurnool': (15.8281, 78.0373),
        'Kozhikode': (11.2588, 75.7804),
        'Bangalore': (12.9716, 77.5946),
        'Nellore': (14.4426, 79.9865),
        'Chennai': (13.0827, 80.2707),
    }

    # Road map with distances
    road_map = {
        'Panji': {'Raichur': 457, 'Mangalore': 365},
        'Raichur': {'Panji': 457, 'Tirupati': 453, 'Kurnool': 100},
        'Mangalore': {'Panji': 365, 'Kozhikode': 233, 'Bangalore': 352},
        'Tirupati': {'Raichur': 453, 'Bellari': 379, 'Chennai': 153},
        'Bellari': {'Tirupati': 379, 'Bangalore': 153},
        'Kurnool': {'Raichur': 100, 'Nellore': 325},
        'Kozhikode': {'Mangalore': 233, 'Bangalore': 356},
        'Bangalore': {'Bellari': 153, 'Mangalore': 352, 'Kozhikode': 356, 'Chennai': 346},
        'Nellore': {'Kurnool': 325, 'Chennai': 175},
        'Chennai': {'Tirupati': 153, 'Nellore': 175, 'Bangalore': 346}
    }

    start_city = input("Enter the start city: ")
    goal_city = input("Enter the goal city: ")

    # Initialize problem
    problem = RouteProblem(start_city, goal_city, locations, road_map)

    # Start RBFS
    start_node = Node(start_city, 0, haversine(locations[start_city][0], locations[start_city][1], locations[goal_city][0], locations[goal_city][1]))
    result, f_cost = rbfs(problem, start_node, float('inf'))

    if result:
        path = reconstruct_path(result)
        print("Path found:", path)
        print("Total cost:", f_cost)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()


# COMMAND ----------

import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

haversine(15.4909, 73.8278,11.2588, 75.7804)


# COMMAND ----------



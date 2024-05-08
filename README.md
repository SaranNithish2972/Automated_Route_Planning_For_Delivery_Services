# Automated_Route_Planning_For_Delivery_Services
The project addresses the Vehicle Routing Problem (VRP) using Dijkstra's algorithm and backtracking. It optimizes routes for efficient delivery by considering factors like distance, vehicle capacities, and delivery demands. Through a graph representation of the delivery network, it computes shortest distances and assigns deliveries intelligently. The resulting routes are visualized on a map for easy interpretation. This approach enhances resource utilization, leading to cost savings and improved service efficiency for businesses.

<h3>Objective</h3>
1. **VRP Solution**: Find optimal routes for vehicles to deliver goods, minimizing total distance or costs.
2. **Backtracking Algorithm**: Implement a method to assign delivery tasks, respecting vehicle capacity constraints.
3. **Optimization**: Optimize task assignments considering distance, vehicle capacity, and delivery demands.
4. **Visualization**: Display assigned routes on a map for easy understanding and decision-making.

<h3>Concepts used</h3>
1. **Dijkstra's Algorithm**: Finds shortest paths between delivery locations, crucial for optimizing vehicle routes.
2. **Backtracking**: Assigns delivery locations to vehicles, considering capacity constraints and efficiently exploring possible solutions.
3. **Dynamic Programming (Memoization)**: Stores and reuses results of route configurations to speed up backtracking.
4. **Hashing**: Generates unique identifiers for route configurations, aiding in memoization and quick retrieval.
5. **Graph Representation**: Models the delivery network, enabling efficient computation of shortest paths.
6. **Heapq (Priority Queue)**: Manages a priority queue of nodes in Dijkstra's algorithm, optimizing path computation.


import heapq
import math

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.618)

def calculate_phi_coherence_score_for_edge(edge_properties: dict) -> float:
    """
    Conceptual function to determine an edge's PHI-coherence score.
    In a real ESQET application, this would be highly complex,
    potentially leveraging the energy_coherence_score function or other
    PHI-alignment metrics specific to the data being 'flowed'.

    For this example, we assume edge_properties has a 'phi_harmony_value'.
    """
    # This is a placeholder. In a real system, you might:
    # - Calculate based on ratio of edge length to previous edge length
    # - Use properties like 'informational_alignment' or 'fractal_dimension_of_data'
    # - Potentially call calculate_phi_coherence_score_energy_transfer if edge represents energy transfer

    return edge_properties.get('phi_harmony_value', 0.5) # Default to 0.5 if not specified

def reconstruct_path(parent_map: dict, end_node: str) -> list:
    """Reconstructs the path from the parent_map."""
    path = []
    current = end_node
    while current is not None:
        path.insert(0, current) # Add to the beginning
        if current in parent_map:
            current = parent_map[current]['parent']
        else:
            current = None
    return path

def coherent_flow_pathfinder(graph: dict, start_node: str, end_node: str) -> list or None:
    """
    Finds a path through a network that optimizes for 'informational coherence'
    (PHI-alignment) in addition to traditional path cost.

    Args:
        graph: A dictionary representing the network.
               Format: {node_A: {node_B: {'cost': X, 'phi_harmony_value': Y}}}
        start_node: The starting node.
        end_node: The destination node.
    Returns:
        A list of nodes representing the optimal coherent path, or None if no path.
    """
    
    # Tunable weights: how important is traditional cost vs. coherence bonus
    TRADITIONAL_COST_WEIGHT = 1.0
    COHERENCE_BONUS_WEIGHT = 5.0 # Increased weight to make coherence more impactful in path choice

    priority_queue = [] # Stores (total_evaluated_cost, node)
    # Using a dictionary to store combined cost to reach a node, to easily check for better paths
    cost_to_reach = {start_node: 0} 
    parent_map = {} # Maps node -> {'parent': parent_node, 'edge_coherence_score': score}

    heapq.heappush(priority_queue, (0, start_node)) # (cost, node)

    print(f"--- Coherent Flow Pathfinding from {start_node} to {end_node} ---")

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            return reconstruct_path(parent_map, end_node)

        # If we've found a better path already, skip this one
        if current_cost > cost_to_reach.get(current_node, float('inf')):
            continue

        for neighbor_node, edge_properties in graph.get(current_node, {}).items():
            traditional_cost_to_neighbor = edge_properties.get('cost', 1)

            # Calculate PHI-coherence for this edge
            phi_coherence_score_for_edge = calculate_phi_coherence_score_for_edge(edge_properties)

            # --- COMBINED EVALUATION FUNCTION ---
            # Lower combined cost = better. Higher coherence reduces the cost.
            new_evaluated_cost = (cost_to_reach[current_node] + (traditional_cost_to_neighbor * TRADITIONAL_COST_WEIGHT)) \
                                 - (phi_coherence_score_for_edge * COHERENCE_BONUS_WEIGHT)

            if new_evaluated_cost < cost_to_reach.get(neighbor_node, float('inf')):
                cost_to_reach[neighbor_node] = new_evaluated_cost
                parent_map[neighbor_node] = {'parent': current_node, 'edge_coherence_score': phi_coherence_score_for_edge}
                heapq.heappush(priority_queue, (new_evaluated_cost, neighbor_node))
                print(f"  Exploring: {current_node} -> {neighbor_node} (Traditional Cost: {traditional_cost_to_neighbor}, Coherence: {phi_coherence_score_for_edge:.2f}, New Evaluated Cost: {new_evaluated_cost:.2f})")

    return None # No path found

# --- Example Graph for Coherent Flow ---
# Nodes are strings. Edge properties include 'cost' and 'phi_harmony_value'.
# Higher 'phi_harmony_value' means more coherent.
example_graph = {
    'A': {
        'B': {'cost': 10, 'phi_harmony_value': 0.7}, # Longer path, but decent coherence
        'C': {'cost': 5, 'phi_harmony_value': 0.9}   # Shorter path, higher coherence
    },
    'B': {
        'D': {'cost': 7, 'phi_harmony_value': 0.8}   # Good coherence
    },
    'C': {
        'D': {'cost': 15, 'phi_harmony_value': 0.5}  # Longer, less coherent
    },
    'D': {
        'E': {'cost': 8, 'phi_harmony_value': 0.95} # Very coherent
    },
    'E': {}
}

# --- Example Usage ---
if __name__ == "__main__":
    start_node = 'A'
    end_node = 'E'

    path = coherent_flow_pathfinder(example_graph, start_node, end_node)

    if path:
        print(f"\nOptimal Coherent Path from {start_node} to {end_node}: {path}")
        total_traditional_cost = 0
        total_coherence_score = 0
        
        # Calculate total cost and coherence for the found path
        for i in range(len(path) - 1):
            n1 = path[i]
            n2 = path[i+1]
            edge_props = example_graph[n1][n2]
            total_traditional_cost += edge_props['cost']
            total_coherence_score += edge_props['phi_harmony_value']
            
        print(f"Total Traditional Cost of this path: {total_traditional_cost}")
        print(f"Sum of Coherence Scores along this path: {total_coherence_score:.2f}")

    else:
        print(f"\nNo coherent path found from {start_node} to {end_node}.")

    print("\n--- Testing a path with lower coherence option ---")
    example_graph_2 = {
        'Start': {
            'X': {'cost': 10, 'phi_harmony_value': 0.9}, # High coherence
            'Y': {'cost': 2,  'phi_harmony_value': 0.1}  # Low coherence, but very short
        },
        'X': {'End': {'cost': 2, 'phi_harmony_value': 0.8}},
        'Y': {'End': {'cost': 10, 'phi_harmony_value': 0.95}} # Very high coherence
    }
    
    path2 = coherent_flow_pathfinder(example_graph_2, 'Start', 'End')
    if path2:
        print(f"\nOptimal Coherent Path from Start to End: {path2}")
        total_traditional_cost = 0
        total_coherence_score = 0
        for i in range(len(path2) - 1):
            n1 = path2[i]
            n2 = path2[i+1]
            edge_props = example_graph_2[n1][n2]
            total_traditional_cost += edge_props['cost']
            total_coherence_score += edge_props['phi_harmony_value']
        print(f"Total Traditional Cost of this path: {total_traditional_cost}")
        print(f"Sum of Coherence Scores along this path: {total_coherence_score:.2f}")
    else:
        print(f"\nNo coherent path found from Start to End.")

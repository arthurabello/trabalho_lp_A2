"""
This module defines the graph structure for the board, managing connectivity between squares and reachable positions.
"""

from typing import Dict, Tuple, Set, List
from collections import defaultdict
import heapq

class BoardGraph:

    """
    Represents the board graph, enabling identification of neighbors and reachable positions.

    Attributes:
        m (int): Number of rows on the board.
        n (int): Number of columns on the board.
        terrain (Dict[Tuple[int, int], str]): Mapping from positions to terrain types.
        units (List[dict]): List of units with their positions and statuses.
        graph (defaultdict): Dictionary representing the graph, where each position is connected to its neighbors.

    Methods:
        _is_valid_position(row, col): Checks if a position is within the board boundaries.
        _build_graph(): Builds the board graph by linking each position to its neighbors.
        _calculate_edge_weight(pos1, pos2): Calculates the edge weight between two positions based on the terrain
        get_neighbors(position): Returns the neighbors of a position on the board.
        get_reachable_positions(start_pos, movement_points): Calculates reachable positions from a starting position, considering movement points.
    """

    def __init__(self, m: int, n: int, terrain: Dict, units: List[Dict]) -> None:

        """
        Initializes the graph with the board dimensions and creates connections between squares.

        Args:
            m (int): number of rows on the board.
            n (int): number of columns on the board.
            terrain (dict): dict that represents each position to its respective terrain.
            units (List[dict]): List of units with their positions and alive status.
        """

        self.m = m  
        self.n = n

        if not isinstance(m, int) or not isinstance(n, int):
            raise TypeError("Board dimensions must be integers in graph/init")
        if m <= 0 or n <= 0:
            raise ValueError("Board dimensions must be positive in graph/init")

        self.terrain = terrain
        self.units = units
        self.graph = defaultdict(dict)
        self._build_graph()
    
    def _is_valid_position(self, row: int, col: int) -> bool:

        """
        Checks if a position is within the board boundaries.

        Args:
            row (int): Row index of the position.
            col (int): Column index of the position.

        Returns:
            bool: Returns True if the position is within boundaries, False otherwise.
        """

        return 0 <= row < self.m and 0 <= col < self.n
    
    def _build_graph(self):

        """
        Constructs the graph linking each board position to its valid neighboring positions with associated weights.
        """

        directions = [
                     (-1, 0),
            (0, -1),           (0, 1),   
                     (1, 0),      
        ]
    
        for row in range(self.m):
            for col in range(self.n):
                current_node = (row, col)
                
                for dx, dy in directions:
                    new_row, new_col = row + dx, col + dy
                    
                    if self._is_valid_position(new_row, new_col):
                        neighbor = (new_row, new_col)
                        weight = self._calculate_edge_weight(current_node, neighbor)    
                        self.graph[current_node][neighbor] = weight
    
    def _calculate_edge_weight(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):

        """
        Calculates the edge weight between two positions based on the terrain
        Args:
            pos1 (Tuple[int, int]): The starting position.
            pos2 (Tuple[int, int]): The ending position.

        Returns:
            float: The cost of moving from pos1 to pos2. Infinite if the path is blocked by a living unit.
        """
        
        for unit in self.units:
            if unit.is_alive and unit.position == pos2:
                return float('infinity')

        terrain1 = self.terrain[pos1]
        terrain2 = self.terrain[pos2]

        weight_map = {
            ('plains', 'plains'): 1,
            ('plains', 'mountain'): 2,
            ('mountain', 'plains'): 1,
            ('plains', 'forest'): 2,
            ('forest', 'plains'): 1,
            ('mountain', 'mountain'): 2,
            ('forest', 'mountain'): 2,
            ('mountain', 'forest'): 2,
            ('forest', 'forest'): 2,
        }

        return weight_map.get((terrain1, terrain2))
    
    def update_units(self, units: list) -> None:

        """
        Updates the current unit positions on the board and rebuilds the graph
        
        Args:
            units (list): Current list of all units
        """
        
        self.units = units
        self._build_graph()  # Rebuild graph with new unit positions

    def get_neighbors(self, position: Tuple[int, int]) -> Dict[Tuple[int,int], int]:

        """
        Retrieves the neighbors and their movement costs for a given position.
        
        Args:
            position (Tuple[int, int]): Position on the board (row, column).

        Returns:
            Dict[Tuple[int, int], int]: Dictionary with neighbors and edge weights for each.
        """

        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Invalid position format in graph/get_neighbors")
        
        row, col = position
        if not self._is_valid_position(row, col):
            raise ValueError("Position out of bounds in graph/get_neighbors")
            
        return self.graph[position]
        

    def dijksboard_algorithm(self, start_pos: Tuple[int, int]) -> Dict[Tuple[int, int], int]:

        """
        Calculates all reachable positions on the board starting from a given position, without a predefined limit on movement points
        and with variable weights for each edge.

        This generalized Dijkstra's algorithm computes the minimum "movement cost" (distance) from the starting position ("start_pos")
        to all other positions on the board. It stops when no further reachable positions with a finite movement cost are available.

        The algorithm works as follows:
        
        1. Initialize a "distances" dictionary where each position on the board starts with an "infinite" distance, representing
        unreachable positions. Set the distance of the starting position ("start_pos") to 0, as it requires no movement cost to
        "reach" itself.

        2. Use a priority queue ("min_heap") to keep track of positions with their current movement costs. Add the starting position
        to the queue with a cost of 0.

        3. Initialize an empty set "visited" to keep track of positions that have already been processed.

        4. Enter a loop to process each position from the queue:
            - Pop the position with the smallest current movement cost from the queue.
            - If this position has already been visited, skip it.
            - Mark the current position as visited.
            - Add the position to "reachable" if it's reachable within the computed cost.

        5. For each neighbor of the current position, calculate the new tentative distance from the starting position
        (current position's distance + movement cost to the neighbor).
            - If this new distance is less than the currently recorded distance for that neighbor, update the neighbor’s distance
            and push it onto the queue with its updated distance.

        6. Repeat steps 4 and 5 until the queue is empty.

        The result is a dictionary of all positions on the board with their minimum movement cost from the starting position.
        This allows the player to see which squares are accessible within their computed movement range.
        
        Args:
            start_pos (Tuple[int, int]): Starting position (row, column) from where the cost is calculated.

        Returns:
            Dict[Tuple[int, int], int]: Dictionary with each position and its minimum movement cost from the starting position.
        """

        if not isinstance(start_pos, tuple) or len(start_pos) != 2:
            raise ValueError("Invalid start position format in graph/dijksboard_algorithm")

        row, col = start_pos
        if not self._is_valid_position(row, col):
            raise ValueError("Start position out of bounds in graph/dijksboard_algorithm")
        
        distances = {pos: float('infinity') for pos in self.graph}
        distances[start_pos] = 0

        min_heap = [(0, start_pos)]  #(distance, position)
        
        visited = set()
        reachable = {}

        while min_heap:
            current_dist, current_pos = heapq.heappop(min_heap)

            if current_pos in visited:
                continue

            visited.add(current_pos)

            reachable[current_pos] = current_dist

            for neighbor, weight in self.graph[current_pos].items():
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(min_heap, (new_dist, neighbor))

        return reachable

    def get_reachable_positions(self, start_pos: Tuple[int, int], movement_points: int, current_units) -> Tuple[Set[Tuple[int, int]], Dict[Tuple[int, int], int]]:

        """
        Calculates reachable positions from a starting position, considering movement points.

        Args:
            start_pos (Tuple[int, int]): Starting position on the board.
            movement_points (int): Movement points available to reach positions.

        Returns:
            Tuple containing:
                Set[Tuple[int, int]]: Set of reachable positions from the starting position
                Dict[Tuple[int, int], int]: Dictionary mapping each reachable position to its minimum movement cost
        """

        self.update_units(current_units)

        if not isinstance(start_pos, tuple) or len(start_pos) != 2:
            raise ValueError("Invalid start position format")
        
        row, col = start_pos
        if not self._is_valid_position(row, col):
            raise ValueError("Start position out of bounds")
        
        if not isinstance(movement_points, (int, float)):
            raise TypeError("Movement points must be a natural number in graph/get_reachable_positions")
        
        if movement_points < 0:
            raise ValueError("Movement points cannot be negative in graph/get_reachable_positions")
        
        reachable_with_costs = self.dijksboard_algorithm(start_pos)
            
        reachable_positions = {
            pos for pos, cost in reachable_with_costs.items() 
            if cost <= movement_points
        }

        movement_costs = {
            pos: cost for pos, cost in reachable_with_costs.items()
            if cost <= movement_points
        }

        return reachable_positions, movement_costs
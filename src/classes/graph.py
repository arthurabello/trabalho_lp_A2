"""
This module defines the graph structure for the board, managing connectivity between squares and reachable positions.
"""

from collections import defaultdict
import heapq

class BoardGraph:

    """
    Represents the board graph, enabling identification of neighbors and reachable positions.

    Attributes:
        m (int): Number of rows on the board.
        n (int): Number of columns on the board.
        graph (defaultdict): Dictionary representing the graph, where each position is connected to its neighbors.

    Methods:
        _is_valid_position(row, col): Checks if a position is within the board boundaries.
        _build_graph(): Builds the board graph by linking each position to its neighbors.
        get_neighbors(position): Returns the neighbors of a position on the board.
        get_reachable_positions(start_pos, movement_points): Calculates reachable positions from a starting position, considering movement points.
    """

    def __init__(self, m, n):

        """
        Initializes the graph with the board dimensions and creates connections between squares.
        
        m -> umber of rows on the board.
        n ->  number of columns on the board.
        """

        self.m = m  
        self.n = n  
        self.graph = defaultdict(dict)
        self._build_graph()
    
    def _is_valid_position(self, row, col):

        """
        Checks if a position is within the board boundaries.
        """

        return 0 <= row < self.m and 0 <= col < self.n
    
    def _build_graph(self):

        """
        Builds the board graph by linking each position to its neighbors.
        """

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),   
            (1, -1),  (1, 0),  (1, 1)    
        ]
    
        for row in range(self.m):
            for col in range(self.n):
                current_node = (row, col)
                
                for dx, dy in directions:
                    new_row, new_col = row + dx, col + dy
                    
                    if self._is_valid_position(new_row, new_col):
                        weight = 1 
                        self.graph[current_node][(new_row, new_col)] = weight
    
    def get_neighbors(self, position):

        """
        Returns the neighbors of a position on the board.
        """

        return self.graph[position]
       

    def dijksboard_algorithm(self, start_pos):

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
        """

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

    def get_reachable_positions(self, start_pos, movement_points):

        """
        ablublublé
        """

        reachable_with_costs = self.dijksboard_algorithm(start_pos)
            
        reachable_positions = {
            pos for pos, cost in reachable_with_costs.items() 
            if cost <= movement_points
        }
            
        return reachable_positions
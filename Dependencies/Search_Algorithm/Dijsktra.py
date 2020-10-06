"""Dijkstra's algorithm to solve a given maze"""


class Dijkstra:
    class Maze:
        class Node:
            """Coords are in form (X, Y) - (0,0) being top left"""
            def __init__(self, coords, value):
                self.coords = coords    # Co-ordinates of node
                self.value = value  # Value of the node. E.G 1, 0 S, G
                self.connections = []   # List of available adjacent nodes (not wall nodes)
                self.parent = None
                self.visited = False
                self.distance = None

            def add_connection(self, node):
                """Used to add which adjacent blocks are visitable"""
                self.connections.append(node)

            def get_parent(self):
                """return the nodes parent node"""
                return self.parent

            def __str__(self):
                return """
                            name: %s
                            distance: %d
                            visited: %s""" % (self.coords, self.distance, str(self.visited))

            def __lt__(self, other):
                if self.distance is None:
                    return False
                elif self.distance < other.distance:
                    return True
                else:
                    return False

            def __gt__(self, other_value):
                if self.distance is None:
                    return True
                elif self.distance > other_value:
                    return True
                else:
                    return False

        class Given_Maze:
            def __init__(self, maze):
                self.maze = maze

            def add_path_step(self, coords):
                """Params: coords - (X, Y) - (Column, Row) - (0 ,0) = Top left"""
                X, Y = coords[0], coords[1]
                self.maze[Y][X] = 'X'

            def __str__(self):
                for row in self.maze:
                    for column in row[:-1]:
                        print(column, end=" ")
                    print(row[-1])
                return ""

        def __init__(self, maze):
            self.maze = []
            self.string_maze = self.Given_Maze(maze)
            self.start = None   # Store the start node
            self.goal = None    # Store the goal node
            self.load(maze)

        def load(self, maze):
            y = 0
            for row in maze:
                self.maze.append([]) # [[]]
                x = 0
                for column in row:
                    next_node = self.Node((x, y), column)
                    self.maze[y].append(next_node)
                    if column == 'M' or column == "G/M" or column == "C/M":
                        self.start = next_node
                    elif column == 'H':
                        self.goal = next_node

                    x += 1
                y += 1

        def get_adj(self, node):
            """Check the available adjacent nodes to a given node
            node.coords = (X, Y) = (Column, Row)"""
            given = []  # Store the values returned from the methods

            # Check above
            given.append(self.get_node((node.coords[0], int(node.coords[1] - 1))))

            # Check below
            given.append(self.get_node((node.coords[0], int(node.coords[1] + 1))))

            # Check right
            given.append(self.get_node((int(node.coords[0]) + 1, node.coords[1])))

            # Check left
            given.append(self.get_node((int(node.coords[0]) - 1, node.coords[1])))

            # Iterate over the given list and add the non-none values to the nodes connections
            for v in given:
                if v is not None:
                    if not v.visited and v.value != 1:
                        node.add_connection(v)

        def get_node(self, coords):
            """Params: coords - Tuple - (X, Y) - (Column, Row)
            Return: Node in that co-ordinates of the maze -> None if not valid"""
            X, Y = int(coords[0]), int(coords[1])
            # Check Y value is valid
            if Y < 0:
                return None
            else:
                try:
                    # Try access the Y row
                    row = self.maze[Y]
                except:
                    return None

            # Check X value is valid
            if X < 0:
                return None
            else:
                try:
                    # Access the X node
                    node = row[X]
                except:
                    return None
            return node

    def __init__(self, maze, monster_coords):
        self.grid = self.Maze(maze)
        self.string_maze = self.grid.string_maze
        self.found = False  # Has the goal been found?
        self.visited = []
        self.unvisted = [self.grid.start]  # Populates at runtime
        self.search()

    def search(self):
        # Run Dijkstra's algorithm
        self.Dijk()
        # If goals parent is None, no route is available
        if self.grid.goal.parent is None:
            print("No path found!")
        else:
            # Construct Path
            # Start at the goal and work towards the start
            steps = []
            current_node = self.grid.goal
            while current_node is not self.grid.start:
                steps.append(current_node)
                current_node = current_node.parent
            steps.append(self.grid.start)
            self.steps = steps

            self.show_solution(steps)

    def show_solution(self, steps):
        for s in steps:
            self.grid.string_maze.add_path_step(s.coords)

    def find_min_node(self):
        """Return the nearest unvisited node from the start"""
        min = self.unvisted[0]  # Initialize
        for n in self.unvisted:
            if n < min:
                min = n
        return min

    def add_to_unvisited(self, node):
        """Check if node is already in self.unvisited"""
        if node not in self.unvisted:
            self.unvisted.append(node)

    def Dijk(self):
        self.grid.start.distance = 0

        # While loop to keep on iterating until the goal is found or until every reachable node has been visited
        while not self.grid.goal.parent and self.unvisted:
            # Visit the vertex with the smallest distance from the start. must be an unvisited vertex
            minNode = self.find_min_node()

            # Make sure minNodes unvisited neighbours are in self.unvisited
            self.grid.get_adj(minNode)
            for n in minNode.connections:
                self.add_to_unvisited(n)
                if not n.visited:
                    # Calculate distance
                    if minNode.distance + 1 < n:
                        n.distance = minNode.distance + 1
                        n.parent = minNode

            minNode.visited = True
            self.visited.append(minNode)
            self.unvisted.remove(minNode)


#######################################################################################################################
if __name__ == "__main__":
    maze = []
    maze.append([0, 0, "S", 1, 0, 0, 0])
    maze.append([0, 1, 0, 0, 0, 1, 0])
    maze.append([0, 1, 1, 1, 1, 1, 0])
    maze.append([0, 0, 0, 0, 1, 0, 0])
    maze.append([0, 1, 1, 1, 1, 0, 0])
    maze.append([0, 1, "G", 0, 0, 0, 0])

    Dijkstra(maze)
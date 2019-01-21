import csv as c


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, compartment, endstored, startcompartment):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Initialize path
    path = []

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:

            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            if compartment == 1:  # Makes the path go passed the choke points if necessary
                if startcompartment == 3 or startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
                    startcompartment = 0
                    path1 = astar(maze, (5, 18), (6, 12), 2, endstored, startcompartment)
                    path = path1 + path
                    end = endstored
                    path1 = astar(maze, (6, 12), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 2:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (6, 2), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 6:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (6, 12), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 2:
                if startcompartment == 3 or startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
                    startcompartment = 0
                    path1 = astar(maze, (5, 18), (6, 2), 2, endstored, startcompartment)
                    path = path1 + path
                    end = endstored
                    path1 = astar(maze, (6, 2), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 1 or startcompartment == 6:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (6, 2), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 3:
                if startcompartment == 1 or startcompartment == 2 or startcompartment == 6:
                    startcompartment = 0
                    path1 = astar(maze, (5, 18), (4, 2), 3, endstored, startcompartment)
                    path = path1 + path
                    end = endstored
                    path1 = astar(maze, (4, 2), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (4, 2), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 4:
                if startcompartment == 1 or startcompartment == 2 or startcompartment == 6:
                    startcompartment = 0
                    path1 = astar(maze, (5, 18), (4, 9), 0, endstored, startcompartment)
                    path = path1 + path
                    end = endstored
                    path1 = astar(maze, (4, 9), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 3:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (4, 2), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 5 or startcompartment == 7:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (4, 9), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 5:
                if startcompartment == 6 or startcompartment == 1 or startcompartment == 2:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (5, 18), end, 0, endstored, startcompartment)
                    path = path1 + path
                if startcompartment == 3 or startcompartment == 4:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (4, 9), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 6:
                if startcompartment == 1 or startcompartment == 2:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (6, 12), end, 0, endstored, startcompartment)
                    path = path1 + path

            if compartment == 7:
                if startcompartment == 3 or startcompartment == 4:
                    startcompartment = 0
                    end = endstored
                    path1 = astar(maze, (4, 15), end, 0, endstored, startcompartment)
                    path = path1 + path


            return path  # Return path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            # print(child.position)
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def matrix_reader():
    with open(r"maps/mapmatrix02v3.txt", "r") as map:
        reader = c.reader(map)
        matrix = list()
        for row in reader:
            new_row = list()
            for x in row:
                new_row.append(int(x))
            matrix.append(list(new_row))
    better = [e for e in matrix if e]

    return(better)


def dmain(start, end):
    compartment = int()
    startcompartment = int()
    maze = matrix_reader()
    endfirst = end

    for i in range(2, 12):
        for j in range(6, 13):
            if end == (j, i):
                compartment = 1  # Lower middle
            if start == (j, i):
                startcompartment = 1

    for i in range(0, 2):
        for j in range(6, 13):
            if end == (j, i):
                compartment = 2  # Lower left
            if start == (j, i):
                startcompartment = 2

    for i in range(0, 2):
        for j in range(0, 5):
            if end == (j, i):
                compartment = 3  # Upper left
            if start == (j, i):
                startcompartment = 3

    for i in range(2, 10):
        for j in range(0, 5):
            if end == (j, i):
                compartment = 4  # Upper Middle
            if start == (j, i):
                startcompartment = 4

    for i in range(10, 18):
        for j in range(0, 6):
            if end == (j, i):
                compartment = 5  # Upper Right
            if start == (j, i):
                startcompartment = 5

    for i in range(12, 25):
        for j in range(6, 13):
            if end == (j, i):
                compartment = 6  # Lower Right
            if start == (j, i):
                startcompartment = 6

    for i in range(18, 25):
        for j in range(0, 6):
            if end == (j, i):
                compartment = 7  # Upper Right Right
            if start == (j, i):
                startcompartment = 7

    if compartment == 1:  # Checks whether it should get passed a choke point or not for all routes
        if startcompartment == 3 or startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
            endfirst = (5, 18)
        if startcompartment == 2:
            endfirst = (6, 2)
        if startcompartment == 6:
            endfirst = (6, 12)

    if compartment == 2:
        if startcompartment == 3 or startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
            endfirst = (5, 18)
        if startcompartment == 1 or startcompartment == 6:
            endfirst = (6, 2)

    if compartment == 3:
        if startcompartment == 1 or startcompartment == 2 or startcompartment == 6:
            endfirst = (5, 18)
        if startcompartment == 4 or startcompartment == 5 or startcompartment == 7:
            endfirst = (4, 2)

    if compartment == 4:
        if startcompartment == 1 or startcompartment == 2 or startcompartment == 6:
            endfirst = (5, 18)
        if startcompartment == 3:
            endfirst = (4, 2)
        if startcompartment == 5 or startcompartment == 7:
            endfirst = (4, 9)

    if compartment == 5:
        if startcompartment == 1 or startcompartment == 2 or startcompartment == 6:
            endfirst = (5, 18)
        if startcompartment == 3 or startcompartment == 4:
            endfirst = (4, 9)

    if compartment == 6:
        if startcompartment == 1 or startcompartment == 2:
            endfirst = (6, 12)

    if compartment == 7:
        if startcompartment == 3 or startcompartment == 4:
            endfirst = (4, 15)

    path = astar(maze, start, endfirst, compartment, end, startcompartment)

    return path

#if __name__ == '__main__':
#    main()
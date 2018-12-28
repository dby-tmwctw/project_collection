"""
Map Search
"""

import comp140_module7 as maps

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """
        Initialize the queue.
        """
        self._queue_list = []

    def __len__(self):
        """
        Return number of items in the queue.
        """
        return len(self._queue_list)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return str(self._queue_list)

    def push(self, item):
        """
        Add item to the queue.
        """
        self._queue_list.append(item)

    def pop(self):
        """
        Remove and return the least recently inserted item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._queue_list.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._queue_list = []

class Stack:
    """
    A simple implementation of a LIFO stack.
    """
    def __init__(self):
        """
        Initialize the stack.
        """
        self._stack_list = []

    def __len__(self):
        """
        Return number of items in the stack.
        """
        return len(self._stack_list)

    def __str__(self):
        """
        Returns a string representation of the stack.
        """
        return str(self._stack_list)

    def push(self, item):
        """
        Add item to the stack.
        """
        self._stack_list.append(item)

    def pop(self):
        """
        Remove and return the least recently inserted item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.
        """
        return self._stack_list.pop(len(self._stack_list) - 1)

    def clear(self):
        """
        Remove all items from the stack.
        """
        self._stack_list = []

#test_stack = Stack()
#test_stack.push(1)
#test_stack.push(2)
#test_stack.push(3)
#print str(test_stack)
#test_stack.pop()
#print str(test_stack)

class PriorityQueue(Queue):
    """
    An implementation of PriorityQueue
    """
    def push(self, element_tuple):
        """
        This function pushes an element into Priority Queue
        """
        self._queue_list.append(element_tuple)
        # Sort the Priority Queue according to the second element of the tuple
        self._queue_list.sort(key = lambda tuple : tuple[1])

    def exist(self, node):
        """
        This function checks whether a node is in Priority Queue
        """
        for existing_element in self._queue_list:
            if node == existing_element[0]:
                return True
        return False

    def pop_node(self, node):
        """
        Pop an element out of Priority Queue by node
        """
        node_index = 0
        for index in range(0, len(self._queue_list)):
            if node == self._queue_list[index][0]:
                node_index = index
        return self._queue_list.pop(node_index)

#test_priority = PriorityQueue()
#test_priority.push(tuple([1, 2]))
#test_priority.push(tuple([3, 4]))
#test_priority.push(tuple([2, 3]))
#print str(test_priority)


def bfs_dfs(graph, rac_class, start_node, end_node):
    """
    Performs a breadth-first search or a depth-first search on graph
    starting at the start_node.  The rac_class should either be a
    Queue class or a Stack class to select BFS or DFS.

    Completes when end_node is found or entire graph has been
    searched.

    Returns a dictionary associating each visited node with its parent
    node.
    """
    rac_object = rac_class()
    dist = {}
    parent = {}
    # Initialise all the information for nodes
    for node in graph.nodes():
        dist[node] = float("inf")
        parent[node] = None
    dist[start_node] = 0
    rac_object.push(start_node)
    # Below is the core algorithm for Bread First Search/Depth First Search
    while len(rac_object) != 0:
        node1 = rac_object.pop()
        # Check if we already reached the end node. If so, break out of the loop
        if node1 == end_node:
            break
        for neighbor in graph.get_neighbors(node1):
            if dist[neighbor] == float("inf"):
                dist[neighbor] = dist[node1] + 1
                parent[neighbor] = node1
                rac_object.push(neighbor)
    return parent

def dfs(graph, start_node, end_node, parent):
    """
    Performs a recursive depth-first search on graph starting at the
    start_node.

    Completes when end_node is found or entire graph has been
    searched.

    Modifies parent dictionary to associate each visited node with its
    parent node.  Assumes that parent initially has one entry that
    associates the original start_node with None.
    """
    # Check whether all the neighhbors in start_node is in parent already
    all_inside_indicator = True
    for neighbor in graph.get_neighbors(start_node):
        if not (neighbor in parent.keys()):
            all_inside_indicator = False
    # Two base cases below:
    # If we already reached the end node, then return parent
    if start_node == end_node:
        return parent
    # If all the neighbors in start_node is already in parent, that means this
    # way cannot take us to end node
    elif all_inside_indicator == True:
        return parent
    # Recursive case below:
    for neighbor in graph.get_neighbors(start_node):
        if not (neighbor in parent.keys()):
            parent[neighbor] = start_node
            dfs(graph, neighbor, end_node, parent)
    return parent

def astar(graph, start_node, end_node,
          edge_distance, straight_line_distance):
    """
    Performs an A* search on graph starting at start_node.

    edge_distance and straigh_line_distance are functions that take
    two nodes and a graph and return a distance.  edge_distance should
    return the actual distance between two neighboring nodes.
    straigh_line_distance should return the heuristic distance between
    any two nodes in the graph.

    Completes when end_node is found or entire graph has been
    searched.

    Returns a dictionary associating each visited node with its parent
    node.
    """
    # Open set is an priority queue
    open_set = PriorityQueue()
    # Claose set is a set. We only need to check whether a certain node is in it
    close_set = set([])
    # We also need a place to store g cost
    g_cost_storage = {}
    # Below is the parent dictionary
    parent = {}
    # Initialise all nodes in parent and g_cost_storage
    for node in graph.nodes():
        parent[node] = None
        g_cost_storage[node] = float("inf")
    # Set inital values for the start_node
    g_cost_storage[start_node] = 0
    initial_distance = straight_line_distance(start_node, end_node, graph)
    open_set.push(tuple([start_node, initial_distance]))
    # Run the while loop till the open_set is empty
    while len(open_set) != 0:
        now_tuple = open_set.pop()
        now_node = now_tuple[0]
        close_set.add(now_node)
        # If we have already reached the end node, we break out of the loop
        if now_node == end_node:
            break
        for neighbor in graph.get_neighbors(now_node):
            # If the node is in close set, we skip it
            if neighbor in close_set:
                continue
            # If it is not in the close set but in open set, we compare the
            # f cost from previous path and f cost from current path. The path
            # that gives a smaller f cost should remain
            elif open_set.exist(neighbor):
                original_tuple = open_set.pop_node(neighbor)
                current_g_cost = g_cost_storage[now_node] + edge_distance(now_node, neighbor, graph)
                current_h_cost = straight_line_distance(neighbor, end_node, graph)
                current_f_cost = current_g_cost + current_h_cost
                if current_f_cost < original_tuple[1]:
                    open_set.push(tuple([neighbor, current_f_cost]))
                    g_cost_storage[neighbor] = current_g_cost
                    parent[neighbor] = now_node
                else:
                    open_set.push(original_tuple)
            # If the node is neither in open set nor in close set, then we
            # reached this node for the first time. We will then calculate its
            # g cost and f cost, and push it into open_set and store its g cost
            # in g cost storage respectively
            else:
                parent[neighbor] = now_node
                current_g_cost = g_cost_storage[now_node] + edge_distance(now_node, neighbor, graph)
                current_h_cost = straight_line_distance(neighbor, end_node, graph)
                current_f_cost = current_g_cost + current_h_cost
                g_cost_storage[neighbor] = current_g_cost
                open_set.push(tuple([neighbor, current_f_cost]))
    return parent


# You can replace functions/classes you have not yet implemented with
# None in the call to "maps.start" below and the other elements will
# work.
maps.start(bfs_dfs, Queue, Stack, dfs, astar)

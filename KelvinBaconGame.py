"""
The Kevin Bacon Game.

Replace "pass" with your code.
"""

import simpleplot
import comp140_module4 as movies
from collections import defaultdict

# Below is the class for queue
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

#queue1 = Queue()
#queue1.push(1)
#queue1.push(2)
#print queue1.pop()
#print str(queue1)


def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the
    start_node.

    Returns a two-element tuple containing a dictionary
    associating each visited node with the order in which it
    was visited and a dictionary associating each visited node
    with its parent node.
    """
    queue = Queue()
    dist = {}
    parent = {}
    # Initialise all the information for nodes
    for node in graph.nodes():
        dist[node] = float("inf")
        parent[node] = None
    dist[start_node] = 0
    queue.push(start_node)
    # Below is the core algorithm for Bread First Search
    while len(queue) != 0:
        node1 = queue.pop()
        for neighbor in graph.get_neighbors(node1):
            if dist[neighbor] == float("inf"):
                dist[neighbor] = dist[node1] + 1
                parent[neighbor] = node1
                queue.push(neighbor)
    return dist, parent


def distance_histogram(graph, node):
    """
    Given a graph and a node in that graph, returns a histogram
    (in the form of a dictionary mapping distance to counts) of
    the distances from node to every other node in the graph.
    """
    # Get the "dist" dictionary from bfs
    result_total= bfs(graph, node)
    result_distance = result_total[0]
    # Declare a dictionary to store information
    result_histogram = defaultdict(int)
    for key in result_distance.keys():
        result_histogram[result_distance[key]] += 1
    return result_histogram

def find_path(graph, start_person, end_person, parents):
    """
    Finds the path from start_person to end_person in the graph,
    and returns the path in the form:

    [(actor1, set([movie1a, ...])), (actor2, set([movie2a, ...])), ...]
    """
    now_node = end_person
    # Check whether start_person and end_person is the same node
    # If it is, there is no need to go through the whole function
    if start_person == end_person:
        return [(start_person, set([]))]
    # The while loop below will append all the paths in the
    # reverse order, hence the initial list is in reverse order
    reverse_path = []
    path = []
    reverse_path.append((end_person, set([])))
    while now_node != start_person:
        now_node1 = now_node
        now_node = parents[now_node1]
        if now_node == None:
            return []
        reverse_path.append((now_node, graph.get_attrs(now_node, now_node1)))
    # Reverse order of the list
    count_index = len(reverse_path)
    while count_index != 0:
        path.append(reverse_path[count_index - 1])
        count_index -= 1
    return path

def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given
    graph, where startperson is the "Kevin Bacon"-esque
    actor from which the search will start and endpeople
    is a list of end people to which the search will be
    performed.

    Prints the results out.
    """
    result_total = bfs(graph, start_person)
    result_parents = result_total[1]
    for end_person in end_people:
        print movies.print_path(find_path(graph, start_person, end_person, result_parents))


def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')

    if len(graph5000.nodes()) > 0:
        # You can/should use smaller graphs and other actors while
        # developing and testing your code.
        play_kevin_bacon_game(graph5000, 'Kevin Bacon',
            ['Amy Adams', 'Andrew Garfield', 'Anne Hathaway', 'Barack Obama', \
             'Benedict Cumberbatch', 'Chris Pine', 'Daniel Radcliffe', \
             'Jennifer Aniston', 'Joseph Gordon-Levitt', 'Morgan Freeman', \
             'Sandra Bullock', 'Tina Fey'])

        # Plot distance histograms
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])

# Uncomment the call to run below when you have completed your code.
run()

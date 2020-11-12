import sys

visited = {}
distance = {}
prev = {}


class Node:
    def __init__(self, n_type, n_name):
        self.type = n_type
        self.name = n_name
        self.strength = 5

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, type, name):
        new_node = Node(n_type=type, n_name=name)
        if new_node not in self.graph.keys():
            self.graph[new_node] = set()
            return True
        return False

    def add_edge(self, source, dest):
        source_node = self.get_node_by_name(source)
        dest_node = self.get_node_by_name(dest)

        if source_node is None or dest_node is None:
            return False
        self.graph[source_node].add(dest_node)
        self.graph[dest_node].add(source_node)
        return True

    def edge_exists(self, source, dest):
        source_node = self.get_node_by_name(source)
        dest_node = self.get_node_by_name(dest)
        return source_node is not None and dest_node is not None and dest_node in self.graph[source_node]

    def get_node_by_name(self, name):
        for n in self.graph.keys():
            if n.name == name:
                return n
        return None

    def print_graph(self):

        for v in self.graph.keys():
            neigh = []
            for n in self.graph[v]:
                neigh.append(n.name)
            print(v.name + "(" + str(v.strength) + ")" + " : " + str(neigh))

    def dijkstra(self, source):
        """

        :param source: Source node
        :return: No return value

        Dijkstra algorithm or single source shortest path finds the shortest path from a single source node to all the
        destination nodes.

        In this scenario, all the edge weights are single units and we need to consider the strength of the node.

        We update the distance as we do BFS, in addition to decreasing strength. If a REPEATER is encountered,
        we double the strength. We ensure that strength is positive so that it can reach the destination.

        We keep three dicts
        visited = {} -> to keep track of visited nodes
        distance = {} -> to update the min distance from source (Initially its infinity)
        prev = {} -> The previous node which has resulted in this minimum distance
        """
        current_strength = source.strength
        queue = []
        self.initialise_dijkstra_table_to_default()
        visited[source] = True
        distance[source] = 0
        prev[source] = source
        queue.append((0, source, current_strength))

        while queue:
            curr_dist, popped_node, strength = min(queue, key=lambda x: x[0])
            neighbours = self.graph[popped_node]
            for n in neighbours:
                if visited[n]:
                    continue

                # Updating distance as well as strength
                new_dist = 1 + curr_dist
                new_strength = strength - 1 if n.type == "COMPUTER" else strength * 2
                if new_dist < distance[n] and new_strength >= 0:
                    prev[n] = popped_node
                    distance[n] = new_dist
                    queue.append((new_dist, n, new_strength))
            queue.remove((curr_dist, popped_node, strength))
            visited[popped_node] = True

        # Printing the node, distance, previous node
        for d in distance.keys():
            print(d.name + " : " + str(distance[d]) + " : " + str(prev[d].name))

    def get_path(self, source, dest):

        """

        :param source: Source node from which path is to be printed
        :param dest: Destination node to which path ends
        :return: Path list

        After Dijkstra algorithm is processed, we look at the distance = {} and previous = {} table and trace
        the path.
        """
        self.dijkstra(source)
        path = []
        if source == dest:
            return [source.name, source.name]
        elif distance[dest] >= sys.maxsize:
            return [None]
        path.append(dest.name)
        while prev[dest] != dest:
            dest = prev[dest]
            path.append(dest.name)

        # the path would be in reverse now. Thus returning reverse list
        return path[::-1]

    def initialise_dijkstra_table_to_default(self):
        """
        Before calling dijkstra algorithm, we need to ensure that distance = {}, visited = {} and prev = {}
        are initialised to default values
        :return:
        """
        for curr_node in self.graph.keys():
            distance[curr_node] = sys.maxsize
            visited[curr_node] = False
            prev[curr_node] = curr_node


if __name__ == '__main__':
    """
    Main function to test with different set of nodes in graph
    """
    graph = Graph()
    graph.add_node(type="COMPUTER", name="A1")
    graph.add_node(type="COMPUTER", name="A2")
    graph.add_node(type="COMPUTER", name="A3")
    graph.add_node(type="COMPUTER", name="A4")
    graph.add_node(type="COMPUTER", name="A5")
    graph.add_node(type="REPEATER", name="R1")
    graph.add_node(type="COMPUTER", name="A6")

    graph.add_edge("A1", "A2")
    graph.add_edge("A1", "A3")
    graph.add_edge("A2", "R1")
    graph.add_edge("A2", "A4")
    graph.add_edge("R1", "A5")
    graph.add_edge("A5", "A4")

    if graph.add_node(name="A6", type="COMPUTER"):
        print("Added")
    else:
        print("Not added")

    graph.print_graph()

    # a2.strength=3

    node = graph.get_node_by_name("R1")
    node.strength = 10
    print(node.name, node.type, node.strength)
    graph.print_graph()

    node = graph.get_node_by_name("R1")
    node.strength = 10
    print(node.name, node.type, node.strength)
    a1 = graph.get_node_by_name("A1")
    a5 = graph.get_node_by_name("A5")
    path = graph.get_path(a1, a5)
    print(path)
    if path[0] is not None:
        print("->".join(path))
    # print(graph.get_path(a1, a4))

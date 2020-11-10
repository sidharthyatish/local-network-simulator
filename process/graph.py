import sys

visited = {}
distance = {}
prev = {}
path = []

class Node:
    def __init__(self, n_type, n_name):
        self.type = n_type
        self.name = n_name
        self.strength = 5


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, val):
        if val not in self.graph:
            self.graph[val] = set()
            distance[val] = sys.maxsize
            visited[val] = False
            return True
        return False

    def add_edge(self, source, dest):
        if source in self.graph and dest in self.graph:
            self.graph[source].add(dest)
            self.graph[dest].add(source)
            return True
        return False

    def print_graph(self):

        for v in self.graph.keys():
            neigh = []
            for n in self.graph[v]:
                neigh.append(n.name)
            print(v.name + " : " + str(neigh))

    def dijkstra(self, source, dest):
        current_strength = source.strength
        queue = []
        visited[source] = True
        distance[source] = 0
        prev[source] = source
        queue.append((0, source))

        while queue:
            curr_dist, popped_node = min(queue, key=lambda x: x[0])
            neighbours = self.graph[popped_node]
            for n in neighbours:
                print(n.name)
                if visited[n]:
                    continue
                new_dist = 1 + curr_dist
                if new_dist < distance[n]:
                    prev[n] = popped_node
                    distance[n] = new_dist
                    queue.append((new_dist, n))
            queue.remove((curr_dist, popped_node))
            visited[popped_node] = True

        for d in distance.keys():
            print(d.name + " : " + str(distance[d]) + " : " + str(prev[d].name))
        # print(prev)

        path.append(dest.name)
        while prev[dest] != dest:
            dest = prev[dest]
            path.append(dest.name)
        print(path[::-1])





if __name__ == '__main__':
    graph = Graph()
    a1 = Node(n_type="computer", n_name="A1")
    a2 = Node(n_type="computer", n_name="A2")
    a3 = Node(n_type="computer", n_name="A3")
    a4 = Node(n_type="computer", n_name="A4")
    a5 = Node(n_type="computer", n_name="A5")
    r1 = Node(n_type="router", n_name="R1")

    graph.add_node(a1)
    graph.add_node(a2)
    graph.add_node(a3)
    graph.add_node(a4)
    graph.add_node(a5)
    graph.add_node(r1)
    graph.add_edge(a1, a2)
    graph.add_edge(a1, a3)
    graph.add_edge(a2, r1)
    graph.add_edge(a2, a4)
    graph.add_edge(r1, a5)
    graph.add_edge(a5, a4)

    graph.print_graph()
    graph.dijkstra(a1, a5)

import Graph
import random

class SocialSphere(object):

    g = Graph.Graph()

    def __init__(self, n=100):
        """Creates a new SocialSphere
        n:  number of nodes/people (must be at least 3)
        """

        "Starts by creating a graph with 3 nodes"
        v1 = Graph.Vertex("1")
        v2 = Graph.Vertex("2")
        v3 = Graph.Vertex("3")
        self.g.add_vertex(v1)
        self.g.add_vertex(v2)
        self.g.add_vertex(v3)
        e1 = Graph.Edge(v1, v3)
        e2 = Graph.Edge(v2, v3)
        self.g.add_edge(e1)
        self.g.add_edge(e2)

        "Now, adds nodes using preferential attachment until n nodes are achieve"
        while (len(self.g) != n):
            self.add_preferential()

    def get_size(self):
        return len(self.g)

    def add_preferential(self):
        "Adds a new node to the graph using preferential attachment"

        "Get list of all nodes in graph"
        nodes = self.g.vertices()

        "Get sum of all existing node degrees"
        sumOfDegrees = 0
        for node in nodes:
            sumOfDegrees = sumOfDegrees + len(self.g[node])

        "Add new node"
        v = Graph.Vertex(str(len(self.g)+1))
        self.g.add_vertex(v)

        "Loop over all nodes in graph, and randomly add edge from new node to each based on preferential attachment"
        for node in nodes:
            "Get number of edges connected to current node"
            curDegree = len(self.g[node])

            "Probability to add edge is curDegree/sumOfDegrees"
            prob = float(float(curDegree) / float(sumOfDegrees))
            if random.random() <= prob:
                "Add edge between new node and current node"
                e = Graph.Edge(v, node)
                self.g.add_edge(e)

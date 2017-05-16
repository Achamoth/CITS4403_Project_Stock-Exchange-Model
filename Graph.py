""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

class Vertex(object):
    """A Vertex is a node in a graph."""

    label = ''

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """Returns a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """The str and repr forms of this object are the same."""

    def getLabel(self):
        return self.label


class Edge(tuple):
    """An Edge is a list of two vertices."""

    def __new__(cls, *vs):
        """The Edge constructor takes two vertices."""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """Return a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Graph(dict):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.

    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """Creates a new graph.
        vs: list of vertices;
        es: list of edges.
        """
        for v in vs:
            self.add_vertex(v)

        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        self[v] = {}

    def add_edge(self, e):
        """Adds and edge to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v1, v2):
        """Take two vertices and return the edge between them if it exists, and None otherwise"""
        try:
            return self[v1][v2]
        except KeyError:
            print 'An edge does not exist between these two vertices'

    def remove_edge(self, e):
        """Take an edge and remove all references to it from the graph"""
        v, w = e
        try:
            del self[v][w]
            del self[w][v]
        except:
            pass

    def vertices(self):
        """Return a list of the vertices in the graph"""
        nodes = []
        for i in self.keys():
            nodes.append(i)
        return nodes

    def edges(self):
        """Return a list of the edges in the graph"""
        edge_set = set()
        for i in self.keys():
            for j in self[i].keys():
                edge_set.add(self[i][j])
        return edge_set

    def out_vertices(self, v):
        """"Method takes a vertex and returns a list of its adjacent vertices"""
        adjacentNodes = []
        try:
            for i in self[v].keys():
                adjacentNodes.append(i)
        except:
            pass
        return adjacentNodes

    def out_edges(self, v):
        """Method takes a vertex and returns a list of edges connected to it"""
        adjacentEdges = []
        try:
            for i in self[v].keys():
                adjacentEdges.append(self[v][i])
        except:
            pass
        return adjacentEdges

    def add_all_edges(self):
        """Method takes a graph with no edges, and makes it complete"""
        vertices = self.vertices() #Get all vertices
        #Loop over all vertices
        for i in range(len(vertices)):
            #Loop over all vertices again
            for j in range(len(vertices)):
                if (i == j):
                    continue
                else:
                    #Add edge between pair of vertices
                    self[vertices[i]][vertices[j]] = Edge(vertices[i], vertices[j])

    def add_regular_edges(self, deg):
        """Starts with edgeless graph, and adds edges until all nodes have same degree"""
        """THIS METHOD DOES NOT CURRENTLY WORK PROPERLY"""
        numNodes = len(self)
        #Ensure degree is <= (n-1), where n is number of vertices in graph
        if(deg > (numNodes-1)):
            return False
        elif(deg % 2 != 0 and numNodes % 2 != 0):
            #If degree is odd, number of nodes in graph must be even
            return False

        #It is possible to generate graph with the required degree
        for curNode in self.keys():
            #Ensure that 'deg' edges aren't alreay attached to this node
            if(len(self[curNode]) == deg):
                break;
            #Add 'deg' edges to this node, ensuring that we're not breaking the rule for any other nodes
            visited = []
            #Loop over all nodes in graph and find one that we can add an edge to
            for secondNode in self.keys():
                if curNode == secondNode:
                    continue
                if(len(self[secondNode]) != deg):
                    #Add edge between curNode and secondNode
                    e = Edge(curNode, secondNode)
                    self.add_edge(e)
                    #Check if we've hit the degree
                    if(len(self[curNode]) == deg):
                        break;

    def is_regular(self):
        """Checks if the graph is regular. Returns true if it is; false otherwise"""
        lastDeg = 0
        curDeg = 0
        firstIteration = True

        #Loop over all vertices in graph
        for curNode in self.keys():
            #Ensure degrees of current node and last node are the same
            if(lastDeg != curDeg):
                return False
            #Update current and last node's degrees
            lastDeg = curDeg
            curDeg = len(self[curNode])
            #Special code for first iteration
            if(firstIteration):
                firstIteration = False
                lastDeg = curDeg

        #Check very last node in graph (won't be checked in loop)
        if(lastDeg != curDeg):
                return False
        #If method hasn't returned yet, graph is regular
        return True

    def is_connected(self):
        """Checks if the graph is connected. Returns true if it is, false otherwise"""
        visited = [] #List of visited nodes
        q = [] #Queue for BFS
        vs = self.keys() #Nodes in graph
        q.append(vs[0]) #Starting node
        visited.append(vs[0]) #Visit first node

        #Perform BFS
        while(len(q) > 0):
            #Pop node off top of queue
            curNode = q.pop(0)
            #Visit any unvisited adjacent nodes, and add them to end of queue
            for i in self[curNode].keys():
                if i not in visited:
                    q.append(i)
                    visited.append(i)

        #Check if graph is connected
        if(len(visited) == len(vs)):
            return True
        else:
            return False

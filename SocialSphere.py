import Graph
import random

class SocialSphere(object):

    g = Graph.Graph()

    def __init__(self, n=100, model='ba', k=2, p=0.15):
        """Creates a new SocialSphere
        n:  number of nodes/people (must be at least 3)
        model:  model used for network construction. Should be 'ba' for Barabase-Albert, or 'ws' for Watts-Strogatz
        k: The degree of each vertex. (Not relevant if the chosen model is Barabase-Albert)
        """
        if(model == 'ba'): #Barabase-Albert model to be used. Construct scale-free network of specified size
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

            "Now, adds nodes using preferential attachment until n nodes are achieved"
            while (len(self.g) != n):
                self.add_preferential()
        elif(model == 'ws'): #Watts-Strogatz model to be used. Construct small-world graph of specified size
            for i in range(n):
                #Add all nodes
                v = Graph.Vertex(str(i+1))
                self.g.add_vertex(v)
            #Make graph k-regular
            self.g.add_regular_edges(k)
            #Rewire edges to produce small world graph (according to WS model)
            self.rewire(p)


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

        "Add 2 edges to nodes within the graph"
        for i in range(2):
            "Use roulette wheel selection to determine where new edge goes"
            s = random.randint(0, sumOfDegrees)
            chosenNode = None
            for node in nodes:
                s = s - len(self.g[node])
                if(s <= 0):
                    chosenNode = node
                    break
            "Add edge and remove selected vertex from roulette wheel"
            e = Graph.Edge(v, chosenNode)
            self.g.add_edge(e)
            sumOfDegrees = sumOfDegrees - len(self.g[chosenNode])

    def rewire(self, p):
        "Probabilistically rewires the edges in the graph to produce a Watts-Strogatz model of a small-world graph"

        #Start from ring lattice
        vertices = self.g.vertices()
        numVertices = len(vertices)

        #Get degree of vertices
        k = len(self.g[vertices[0]])
        numLoops = k/2

        #We have k/2 total loops. Within each loop, we loop over all nodes and probabilistically rewire an edge
        for i in range(k/2):

            #Loop over all nodes
            for index in range(numVertices):

                #Check link to (i+1)th nearest neighbour in clockwise direction, and probabilistically rewire it
                neighbourIndex = (index + i + 1) % numVertices

                #Get edge between current node and its (i+1)th nearest neighbour in clockwise direction
                e = self.g.get_edge(vertices[index], vertices[neighbourIndex])

                #Determine whether or not it will be rewired
                if(random.random() <= p):
                    #It's getting rewired. Pick a node to move the edge to, disallowing duplicate edges and loops
                    self.g.remove_edge(e) #Remove old edge
                    found = False
                    targetIndex = 0
                    #Find vertex for new edge
                    while(not found):
                        targetIndex = random.randint(0,numVertices-1)
                        if (targetIndex != index and targetIndex != neighbourIndex):
                            #It's not a loop. Make sure it isn't a duplicate
                            eCheck = self.g.get_edge(vertices[index], vertices[targetIndex])
                            if(eCheck == False):
                                found = True #Not a duplicate
                        if(found):
                            #We've found the new node. Rewire the edge by removing the old edge and adding a new one
                            newEdge = Graph.Edge(vertices[index], vertices[targetIndex])
                            self.g.add_edge(newEdge) #Add new edge

                else:
                    #Leave it be
                    pass

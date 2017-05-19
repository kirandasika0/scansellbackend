class Node():
    def __init__(self, dataIn, parent=None, rank = 0):
        self.data = dataIn
        self.parent = parent
        self.rank = rank

    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return str(self.data)

class DisjointSet():
    def __init__(self):
        self.djSet = dict()

    def makeSet(self, dataIn):
        node = Node(dataIn)
        node.parent = node
        self.djSet[dataIn] = node

    def findSet(self, dataIn):
        if type(dataIn) == int:
            return self.findSet(self.djSet[dataIn])
        parent = dataIn.parent
        if parent == dataIn:
            return parent
        dataIn.parent = self.findSet(dataIn.parent)
        return dataIn.parent

    def union(self, data1, data2):
        node1 = self.djSet[data1]
        node2 = self.djSet[data2]

        parent1 = self.findSet(node1)
        parent2 = self.findSet(node2)

        if parent1.data is parent2.data:
            return False

        if parent1.rank >= parent2.rank:
            if parent1.rank == parent2.rank:
                parent1.rank += 1
            else:
                parent1.rank = parent1.rank
            parent2.parent = parent1
        else:
            parent1.parent = parent2

        return True

#!/usr/bin/env python3
from collections import OrderedDict


class SimpleGraph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.doubleNodes = []
        """
        doubleNodes looks like:

        start   Target  Weight
        ----------------------
        (0,1)   (1,0)   2
        """

    def printAll(self):
        for element in self.doubleNodes:
            print(element)
            print("\n")
            pass

    # duplicate all edges - they are undirected
    def doubleAllNodes(self):
        for element in self.nodes:
            # remove edges starting and ending on same point
            if element[0] == element[1]:
                pass
            else:
                self.doubleNodes.append(element)
                self.doubleNodes.append([element[1], element[0], element[2]])

    def dijkstra(self, start, target):
        # paths with same weight is still a problem...
        startNode = [None, start, 0]
        currentNode = startNode
        shortestPath = []
        availablePaths = []
        usedNodes = []  # conatins nodes already have been used
        shortestPath.append(startNode)
        usedNodes.append(startNode[1])
        while currentNode[1] != target:
            weights = []
            # add possible paths to availablePaths - but only unused
            for edge in self.doubleNodes:
                if currentNode[1] == edge[0] and not (edge[1] in usedNodes):
                    newWeightEdge = edge
                    newWeightEdge[2] += currentNode[2]
                    availablePaths.append(newWeightEdge)
            # add here cleaning if same edges with diffrent weigths exist
            availablePaths = self.listCleaning(availablePaths)
            # find the shortest of them
            for edge in availablePaths:
                weights.append(edge[2])
            # get the index of smallest
            shortestWay = weights.index(min(weights))
            # move from availablePaths to shortestPath
            shortestPath.append(availablePaths[shortestWay])
            del availablePaths[shortestWay]
            # make latest shortest node to currentNode
            currentNode = shortestPath[-1]
            usedNodes.append(shortestPath[-1][1])
            # remove all elements from availablePaths containing
            # a node from usedNodes as targets
            for edge in availablePaths:
                if edge[1] in usedNodes:
                    availablePaths.remove(edge)
        return shortestPath

    def listCleaning(self, paths):
        newPath = OrderedDict()
        for edge in paths:
            key = (edge[0], edge[1])
            if key not in newPath:
                newPath[key] = edge[2]
            else:
                value = newPath[key]
                if edge[2] < value:
                    newPath[key] = edge[2]
                else:
                    pass
        newPathList = []
        for key, value in newPath.items():
            newPathList.append([key[0], key[1], value])
        return newPathList

#!/usr/bin/env python3


class SimpleGraph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.doubleNodes = []

    def printAll(self):
        for element in self.doubleNodes:
            print(element)
            print("\n")
            pass
    # duplicate all edges - they are undirected
    def doubleNodes(self):
        for element in self.nodes:
            self.doubleNodes.append(element[0], element[1], element[2])
            self.doubleNodes.append(element[1], element[0], element[2])

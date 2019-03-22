#!/usr/bin/env python3

class SearchableGraph:

    def __init__(self, graph, node, unknown):
        self.graph = graph
        """
        graph should look like:
        {
            node: [nodes, connected, to]
        }
        """
        self.node = node
        self.unknown = unknown

    def find_next_node(self):
        queue = [[self.node]]
        foundNode = True
        level = 1
        nextNodeElement = 0
        while foundNode:
            # check available paths in level
            if not queue[nextNodeElement]:
                nextNodeElement += 1
                level += 1
            # set next node
            try:
                nextNode = queue[nextNodeElement].pop()
            except:
                return None
            # get nodes from this node
            value = self.graph[nextNode]
            try:
                known_data = queue[level]
                for element in value:
                    known_data.append(element)
                queue[level] = known_data
                # dann erweitern
            except IndexError:
                queue.append(value)
            # if one of these nodes is missing return it
            # else keep on searching
            for known in queue[level]:
                # known node as unknown directions
                if known in self.unknown:
                    return known

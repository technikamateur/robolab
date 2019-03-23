#!/usr/bin/env python3
import logging


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
        self.logger = logging.getLogger('SearchableGraph')
        logging.basicConfig(level=logging.DEBUG)

    def find_next_node(self):
        queue = [[self.node]]
        usedNodes = []
        foundNode = True
        level = 1
        nextNodeElement = 0
        while foundNode:
            print(queue)
            # check available paths in level
            if not queue[nextNodeElement]:
                nextNodeElement += 1
                level += 1
            # set next node
            try:
                nextNode = queue[nextNodeElement].pop()
                usedNodes.append(nextNode)
                print(nextNode)
            except IndexError:
                self.logger.error(
                    "There are undiscovered directions, but they are not reachable!"
                )
                return None
            # get nodes from this node
            value = self.graph[nextNode]
            # filter nodes - you shouldnt go back
            value = [
                unknown_node for unknown_node in value
                if unknown_node not in usedNodes
            ]
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
                # known node has unknown directions
                if known in self.unknown:
                    return known

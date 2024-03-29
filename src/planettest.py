#!/usr/bin/env python3

import unittest
from planet import *


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):

        # set your data structure
        self.havok = Planet()

        self.havok.add_path(((15, 37), Direction.NORTH),
                            ((15, 39), Direction.SOUTH), 1)
        # loop
        self.havok.add_path(((15, 39), Direction.NORTH),
                            ((15, 39), Direction.WEST), 1)
        self.havok.add_path(((15, 39), Direction.EAST),
                            ((16, 39), Direction.WEST), 1)
        self.havok.add_path(((15, 37), Direction.WEST),
                            ((14, 39), Direction.SOUTH), 1)
        self.havok.add_path(((14, 39), Direction.WEST),
                            ((13, 38), Direction.NORTH), 1)
        self.havok.add_path(((13, 38), Direction.SOUTH),
                            ((13, 37), Direction.NORTH), 1)
        # blocked paths
        self.havok.add_path(((15, 37), Direction.SOUTH),
                            ((15, 37), Direction.SOUTH), -1)
        self.havok.add_path(((16, 39), Direction.NORTH),
                            ((16, 39), Direction.NORTH), -1)
        self.havok.add_path(((17, 38), Direction.SOUTH),
                            ((17, 37), Direction.NORTH), 1)

    def test_empty_planet(self):
        self.assertIsNotNone(self.havok.get_paths())
        self.assertNotEqual(self.havok.get_paths(), {})

    def test_target_not_reachable(self):
        self.assertIsNone(self.havok.shortest_path((13, 37), (20, 38)))
        self.assertIsNone(self.havok.shortest_path((13, 37), (17, 38)))


class shortestPathTestPlanet(unittest.TestCase):
    def setUp(self):
        # set your data structure
        self.havok = Planet()

        self.havok.add_path(((15, 37), Direction.NORTH),
                            ((15, 39), Direction.SOUTH), 1)
        self.havok.add_path(((15, 37), Direction.EAST),
                            ((17, 37), Direction.WEST), 1)
        # loop
        self.havok.add_path(((15, 39), Direction.NORTH),
                            ((15, 39), Direction.WEST), 1)
        self.havok.add_path(((15, 39), Direction.EAST),
                            ((16, 39), Direction.WEST), 1)
        self.havok.add_path(((15, 37), Direction.WEST),
                            ((14, 39), Direction.SOUTH), 1)
        self.havok.add_path(((14, 39), Direction.WEST),
                            ((13, 38), Direction.NORTH), 1)
        self.havok.add_path(((13, 38), Direction.SOUTH),
                            ((13, 37), Direction.NORTH), 1)
        self.havok.add_path(((17, 38), Direction.SOUTH),
                            ((17, 37), Direction.NORTH), 1)
        # changed this weight to make dijkstra predictable
        self.havok.add_path(((17, 38), Direction.EAST),
                            ((17, 37), Direction.EAST), 2)
        self.havok.add_path(((16, 39), Direction.EAST),
                            ((17, 38), Direction.NORTH), 1)
        self.havok.add_path(((16, 39), Direction.SOUTH),
                            ((17, 38), Direction.WEST), 1)
        # blocked paths
        self.havok.add_path(((15, 37), Direction.SOUTH),
                            ((15, 37), Direction.SOUTH), -1)
        self.havok.add_path(((16, 39), Direction.NORTH),
                            ((16, 39), Direction.NORTH), -1)

    def test_shortest_path(self):
        print("HI")
        print(self.havok.shortest_path((17, 38), (17, 38)))
        self.assertEqual(
            self.havok.shortest_path((13, 37), (17, 38)),
            [((13, 37), Direction.NORTH), ((13, 38), Direction.NORTH),
             ((14, 39), Direction.SOUTH), ((15, 37), Direction.EAST),
             ((17, 37), Direction.NORTH)])


class ExploringTestPlanet(unittest.TestCase):
    def setUp(self):
        self.havok = Planet()
        self.havok.add_path(((15, 37), Direction.NORTH),
                            ((15, 39), Direction.SOUTH), 1)
        self.havok.add_path(((15, 37), Direction.EAST),
                            ((17, 37), Direction.WEST), 1)
        self.havok.add_path(((15, 39), Direction.NORTH),
                            ((15, 39), Direction.WEST), 1)
        self.havok.add_path(((15, 39), Direction.EAST),
                            ((16, 39), Direction.WEST), 1)
        self.havok.add_path(((16, 39), Direction.EAST),
                            ((17, 38), Direction.NORTH), 1)
        self.havok.add_path(((16, 39), Direction.SOUTH),
                            ((17, 38), Direction.WEST), 1)
        self.havok.add_path(((17, 38), Direction.SOUTH),
                            ((17, 37), Direction.NORTH), 1)
        self.havok.add_path(((17, 38), Direction.EAST),
                            ((17, 37), Direction.EAST), 1)
        self.havok.add_path(((15, 37), Direction.WEST),
                            ((14, 39), Direction.SOUTH), 1)
        self.havok.add_path(((14, 39), Direction.WEST),
                            ((13, 38), Direction.NORTH), 1)
        self.havok.add_path(((13, 38), Direction.SOUTH),
                            ((13, 37), Direction.NORTH), 1)

        self.havok.add_unknown_paths({(13, 37): [(Direction.SOUTH, -2)]})
        self.havok.add_unknown_paths({(16, 39): [(Direction.NORTH, -2)]})

    def test_go_direction(self):
        self.assertTrue(self.havok.go_direction((13, 37)))
        self.assertFalse(self.havok.go_direction((15, 37)))

    def test_get_next_node(self):
        self.assertEqual(
            self.havok.get_next_node((15, 37)), [((15, 37), Direction.NORTH),
                                                 ((15, 39), Direction.EAST)])
        self.assertEqual(
            self.havok.get_next_node((15, 39)), [((15, 39), Direction.EAST)])

    def test_get_direction(self):
        self.assertEqual(self.havok.get_direction((13, 37)), Direction.SOUTH)


class ExploringNodes(unittest.TestCase):
    def setUp(self):
        self.nugget = Planet()
        self.nugget.add_path(((0, 0), Direction.NORTH),
                             ((0, 1), Direction.SOUTH), 1)
        # 0,1 all known
        self.nugget.add_path(((0, 1), Direction.NORTH),
                             ((1, 0), Direction.SOUTH), 1)
        self.nugget.add_path(((0, 1), Direction.EAST),
                             ((1, 1), Direction.SOUTH), 1)
        self.nugget.add_path(((0, 1), Direction.WEST),
                             ((1, 1), Direction.SOUTH), 1)

    def test_next_node(self):
        self.assertFalse(self.nugget.go_direction((0, 0)))
        self.assertNotEqual(
            self.nugget.get_next_node((0, 0)), [((0, 0), Direction.NORTH)])


if __name__ == "__main__":
    unittest.main()

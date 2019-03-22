#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        example planet:

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """

        # set your data structure
        self.planet = Planet()

        # add the paths: Planet Doctor Starnge (with loop)
        self.planet.add_path(((0, 0), Direction.NORTH),
                             ((0, 1), Direction.SOUTH), 50)
        self.planet.add_path(((0, 1), Direction.NORTH),
                             ((1, 2), Direction.WEST), 70)
        self.planet.add_path(((1, 2), Direction.SOUTH),
                             ((2, 0), Direction.WEST), 120)
        self.planet.add_path(((2, 0), Direction.NORTH),
                             ((2, 2), Direction.SOUTH), 100)
        # loop
        self.planet.add_path(((2, 2), Direction.NORTH),
                             ((2, 2), Direction.WEST), 100)
        self.planet.add_path(((2, 2), Direction.EAST),
                             ((3, 2), Direction.WEST), 50)
        self.planet.add_path(((3, 2), Direction.EAST),
                             ((4, 1), Direction.NORTH), 70)
        # temporary removed
        #self.planet.add_path(((3, 2), Direction.SOUTH), ((4, 1), Direction.WEST), 150)
        #self.planet.add_path(((4, 1), Direction.SOUTH), ((4, 0), Direction.NORTH), 50)
        self.planet.add_path(((4, 1), Direction.EAST),
                             ((4, 0), Direction.EAST), 70)
        self.planet.add_path(((4, 0), Direction.WEST),
                             ((2, 0), Direction.EAST), 100)
        self.planet.add_unknown_paths({(4, 0): [(Direction.NORTH, -2)]})
        self.planet.add_unknown_paths(
            {(4, 1): [(Direction.SOUTH, -2), (Direction.WEST, -2)]})
        self.planet.add_unknown_paths({(3, 2): [(Direction.SOUTH, -2)]})

    # def test_empty_planet(self):
    #     self.assertIsNotNone(self.planet.get_paths())
    #     self.assertNotEqual(self.planet.get_paths(), {})
    #
    # def test_target_not_reachable(self):
    #     # does the shortest path algorithm loop infinitely?
    #     # there is no shortest path
    #     self.assertIsNone(self.planet.shortest_path((0, 0), (5, 0)))
    #
    # def test_shortest_path(self):
    #     # does the shortest path algorithm loop infinitely?
    #     # there is no shortest path
    #     self.assertEqual(self.planet.shortest_path((0, 0), (4, 1)), [((0, 0), Direction.NORTH), ((0, 1), Direction.NORTH), ((1, 2), Direction.SOUTH), ((2, 0), Direction.EAST), ((4, 0), Direction.NORTH)])

    def test_go_direction(self):
        self.assertFalse(self.planet.go_direction((2, 0)))

    def test_get_next_node(self):
        self.assertIsNotNone(self.planet.get_next_node((2, 0)))


if __name__ == "__main__":
    unittest.main()

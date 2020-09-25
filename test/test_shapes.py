#!/usr/bin/env python3

import unittest
import math

from samplersnek import shapes
from VectorSnek.vectorsnek.vectors import Vector

class TestAxisAlignedRectangle(unittest.TestCase):

    def test_contains(self):
        aar = shapes.AxisAlignedRectangle(Vector([-1, 0]), Vector([5, 2]))
        self.assertTrue(aar.contains(Vector([3, 1])))
        self.assertFalse(aar.contains(Vector([-2, 5])))
        # boundary case
        self.assertTrue(aar.contains(Vector([5, 1])))

class TestTriangle(unittest.TestCase):
    
    def test_contains(self):
        a = Vector([-5, -6])
        b = Vector([-5, 5])
        c = Vector([10, 0])
        triangle = shapes.Triangle(a, c, b)
        self.assertTrue(triangle.contains(Vector([0, 1])))
        self.assertFalse(triangle.contains(Vector([2.5, 3])))
        # edge case
        self.assertTrue(triangle.contains(Vector([1, 3])))
        # corner case
        self.assertTrue(triangle.contains(a))

class TestRectangle(unittest.TestCase):

    def test_contains(self):
        bl_corner = Vector([-4, -2])
        dimensions = Vector([8, 10])
        orientation = 60.0
        rectangle = shapes.Rectangle(bl_corner, dimensions, orientation)
        # inside near left corner
        self.assertTrue(rectangle.contains(Vector([-10.97, 3.2])))
        # inside near top corner
        self.assertTrue(rectangle.contains(Vector([-8.31, 8.7])))
        # inside near right corner
        self.assertTrue(rectangle.contains(Vector([-1.13, 4.7])))
        # inside near bottom corner
        self.assertTrue(rectangle.contains(Vector([-4.27, -0.9])))
        # right on diagonal
        diagonal = dimensions.rotated(orientation * math.pi / 180) 
        self.assertTrue(rectangle.contains(bl_corner + 0.2 * diagonal))
        # corner
        self.assertTrue(rectangle.contains(bl_corner + diagonal))
        # outside 
        self.assertFalse(rectangle.contains(Vector([-3.71, 8.7])))

if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python3

import unittest
import math

import sys
sys.path.append('..')
import shapes

from VectorSnek.vectorsnek.vectors import Vector

class TestAxisAlignedRectangle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.aar = shapes.AxisAlignedRectangle(Vector([-1, 0]), Vector([5, 2]))

    def test_0_inside(self):
        self.assertTrue(self.aar.contains(Vector([3, 1])))

    def test_1_outside(self):
        self.assertFalse(self.aar.contains(Vector([-2, 5])))

    def test_2_boundary(self):
        self.assertTrue(self.aar.contains(Vector([5, 1])))

class TestTriangle(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.a = Vector([-5, -6])
        cls.b = Vector([-5, 5])
        cls.c = Vector([10, 0])
        cls.triangle = shapes.Triangle(cls.a, cls.c, cls.b)

    def test_0_inside(self):
        self.assertTrue(self.triangle.contains(Vector([0, 1])))

    def test_1_outside(self):
        self.assertFalse(self.triangle.contains(Vector([2.5, 3])))

    def test_2_boundary(self):
        self.assertTrue(self.triangle.contains(Vector([1, 3])))

    def test_3_corner(self):
        self.assertTrue(self.triangle.contains(self.a))

class TestRectangle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.corner = Vector([-4, -2])
        cls.diagonal = Vector([8, 10])
        cls.orientation = math.radians(60.0)
        cls.rectangle = shapes.Rectangle(cls.corner, cls.diagonal, cls.orientation)

    def test_0_inside(self):
        # inside near left corner
        self.assertTrue(self.rectangle.contains(Vector([-10.97, 3.2])))
        # inside near top corner
        self.assertTrue(self.rectangle.contains(Vector([-8.31, 8.7])))
        # inside near right corner
        self.assertTrue(self.rectangle.contains(Vector([-1.13, 4.7])))
        # inside near bottom corner
        self.assertTrue(self.rectangle.contains(Vector([-4.27, -0.9])))
        # right on diagonal
        self.assertTrue(self.rectangle.contains(
            self.corner + 0.2 * self.diagonal.rotated(self.orientation))
        )

    def test_1_outside(self):
        self.assertFalse(self.rectangle.contains(Vector([-3.71, 8.7])))

    def test_2_boundary(self):
        p = self.corner + Vector([0.2 * self.diagonal.x, 0]).rotated(self.orientation)
        self.assertTrue(self.rectangle.contains(p))

    def test_3_corner(self):
        self.assertTrue(self.rectangle.contains(self.corner + self.diagonal.rotated(self.orientation)))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)

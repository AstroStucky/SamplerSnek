# ---------------------------------------------------------------------------
#
#   PROJECT       : SamplerSnek
#   AUTHOR        : Thomas R. Stucky
#   FILENAME      : shapes.py
#   CREATED       : 2020-09-21
#   TAB SIZE      : 4
#   DESCRIPTION   : Defines 2D shape objects that describe a sampling domain.
#
# -------------------------GPL 3.0 LICENSE-----------------------------------
#
#  Copyright (C) 2020 Thomas R. Stucky
#
#  This file is part of SamplerSnek
#
#  SamplerSnek is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------

import abc
import sys
import math

from VectorSnek.vectorsnek.vectors import Vector

class Shape2D(abc.ABC):

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
    
    """ Returns true if x is inside the shape, false otherwise
    
    Args:
        x (2D Vector): Point being tested
    
    Returns:
        bool """
    @abc.abstractmethod
    def contains(self, P):
        pass

class AxisAlignedRectangle(Shape2D):

    """ initialize with shape parameters
    
    Args:
        corner1 (2D Vector): first corner of the rectangle
        corner2 (2D Vector): second corner across the diagonal from the first
    
    Returns:
        None """
    def __init__(self, corner1, corner2):
        super().__init__(min(corner1.x, corner2.x), max(corner1.x, corner2.x), min(corner1.y, corner2.y), max(corner1.y, corner2.y))

    def contains(self, P):
        return self.xmin <= P.x and P.x <= self.xmax and self.ymin <= P.y and P.y <= self.ymax

class Triangle(Shape2D):

    def __init__(self, a, b, c):
        # calculate limits
        x_values = [vec.x for vec in [a, b, c]]
        y_values = [vec.y for vec in [a, b, c]]
        super().__init__(min(x_values), max(x_values), min(y_values), max(y_values))
        self.a = a
        self.b = b
        self.c = c

    def contains(self, P):
        denominator = (self.b.y - self.c.y) * (self.a.x - self.c.x) + (self.c.x - self.b.x) * (self.a.y - self.c.y)
        alpha = ((self.b.y - self.c.y) * (P.x - self.c.x) + (self.c.x - self.b.x) * (P.y - self.c.y)) / denominator
        beta = ((self.c.y - self.a.y) * (P.x - self.c.x) + (self.a.x - self.c.x) * (P.y - self.c.y)) / denominator
        gamma = 1 - beta - alpha
        return 0 <= alpha and alpha <= 1 and 0 <= beta and beta <= 1 and 0 <= gamma and gamma <= 1

class Rectangle(Shape2D):

    """ initialize with shape parameters
    
    Args:
        bottomleft_corner (2D Vector): position of the bottom left corner
        dimensions (2D Vector): height and width of rectangle (without rotation)
        orientation (float): angle in degrees rectangle is rotated around the 
                             bottom left corner

    Returns:
        None """
    def __init__(self, bottomleft_corner, dimensions, orientation):
        # find corners
        self.a = bottomleft_corner
        diagonal = dimensions.rotated(orientation * math.pi / 180)
        # unit vectors along edges of rectangle
        left_hat = Vector([0,1]).rotated(orientation * math.pi / 180)
        base_hat = Vector([1,0]).rotated(orientation * math.pi / 180)
        # projection onto left side of rectangle
        self.b = self.a + (diagonal * left_hat) * left_hat
        self.c = self.a + diagonal
        # projection onto base of rectangle
        self.d = self.a + (diagonal * base_hat) * base_hat
        self._triangle_1 = Triangle(self.a, self.b, self.c)
        self._triangle_2 = Triangle(self.a, self.c, self.d)

    def contains(self, P):
        return self._triangle_1.contains(P) or self._triangle_2.contains(P)

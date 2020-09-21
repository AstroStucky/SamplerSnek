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
import vectors

class Shape2D(metaclass=abc.ABCMeta):

    def __init__(self):
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.xmax = None
    
    """ Returns true if x is inside the shape, false otherwise
    
    Args:
        x (2-tuple): Point being tested
    
    Returns:
        bool """
    @abc.abstractmethod
    def contains(x):
        pass

class AxisAlignedRectangle(Shape2D):

    """ initialize with shape parameters
    
    Args:
        xmin (float): left boundary of rectangle
        xmax (float): right boundary of rectangle
        ymin (float): bottom boundary of rectangle
        ymax (float): top boundary of rectangle
    
    Returns:
        None """
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.xmax = ymax

    def contains(x):
        return x[0] > self.xmin and x[0] < self.xmax and x[1] > self.ymin and x[1] < self.ymax:

def Rectangle(Shape2D):

    """ initialize with shape parameters
    
    Args:
        bottom_left_corner_position (2-tuple of floats): position of the bottom 
            left corner of the rectangle
        orientation (float): angle in degrees rectangle is rotated
        extents (2-tuple of floats): dimensions of the rectangle

    Returns:
        None """
    def __init__(self, bottom_left_corner_position, orientation, extents):

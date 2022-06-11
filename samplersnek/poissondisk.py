#!/usr/bin/env python3
# ---------------------------------------------------------------------------
#  
#   PROJECT       : SamplerSnek
#   AUTHOR        : Thomas Stucky
#   FILENAME      : poisssondisk.py
#   CREATED       : 2020-09-16
#   TAB SIZE      : 4
#   DESCRIPTION   : Library for generating uniformly distributed samples
#                   within an area/volume using the fast Poisson disk sampling
#                   algorithm described by Bridson et al. 2007.
#
# --------------------------GPL 3.0 LICENSE----------------------------------
#
#  Copyright (C) 2020 Thomas R. Stucky
# 
#  This file is part of SamplerSnek
#
#  SampleSnek is free software: you can redistribute it and/or modify
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

import sys
import math
import random
import argparse

import matplotlib.pyplot as plt
import numpy as np

from VectorSnek.vectorsnek.vectors import Vector

import shapes

# Plotting parameters
FIGSIZE = [6,6] # inches
FIGDPI = 120
MPL_STYLE = "dark_background"

""" Calculate distance squared between two N-dimensional points x and y"""
def distance_sqrd(x, y):
    diff = y - x
    return diff.dot(diff)

""" Calculate coordinates on a 2D background grid. Assumes square grids
Args:
    x (2D Vector): Point
    grid_dx (float): Grid size
    mins (2D Vector): Minimum grid value
Returns:
    2D Vector of indices"""
def get_2d_grid_coordinates(p, grid_dx, mins):
    # print(p)
    # print(grid_dx)
    # print(mins)
    return math.floor(Vector([(p.x - mins.x) / grid_dx, (p.y - mins.y) / grid_dx]))

# returns sample in an annulus around x
""" Return random 2d sample in an annulus around a point (radius < R < 2*radius)
Args:
    radius (float): inner radius of annulus
    center (2D vector): point annulus is centered around
Returns:
    2D Vector"""
def sample_2d_annulus(radius, center):
    while True:
        r = Vector([random.uniform(-2, 2), random.uniform(-2, 2)])
        r_sqrd = r.dot(r)
        if r_sqrd > 1 and r_sqrd <= 4:
            return center + radius * r

""" Generate a list of uniformly distributed 2D samples using poisson disk
    sampling. Assumes a square sampling region.
Args:
    radius (float): Minimum distance between points
    shape (Shape2D): Sampling domain
    max_sample_attempts (integer): Higher number of attempts tends to create 
                                   tighter packings
    verbose (boolean): Print details about algorithm during execution
    draw_algorithm (boolean): Draw algorithm results live to a matplotlib plot
Returns:
    List of 2D vectors"""
def poisson_sample_2d_square(radius, shape, max_sample_attempts=30, verbose=False, draw_algorithm=False):

    xmin = shape.xmin
    xmax = shape.xmax
    ymin = shape.ymin
    ymax = shape.ymax

    if draw_algorithm:
        plt.ion()
        plt.style.use(MPL_STYLE)
        plt.figure()
        ax = plt.subplot()
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))

    # randomize
    random.seed()
    # initialize sample list
    sample = []

    ## Step 0
    # initialize 2D background grid for accelerating spatial search
    grid_dx = radius / math.sqrt(2.0) # contain at most 1 sample 
    dims = Vector([math.ceil((xmax - xmin) / grid_dx), math.ceil((ymax - ymin) / grid_dx)])
    # -1 indictes no sample in cell, non-negative is index of sample in cell
    background_grid = np.full((dims.x, dims.y), -1)

    ## Step 1
    # randomly select initial sample
    while True:
        x = Vector([random.uniform(xmin, xmax), random.uniform(ymin, ymax)])
        if shape.contains(x):
            sample.append(x)
            break
    # insert into background grid with the index of the sample
    p = get_2d_grid_coordinates(x, grid_dx, Vector([xmin, ymin]))
    background_grid[p.x][p.y] = 0
    # initialize active list with the index of the sample
    active_list = list([0])

    ## Step 2
    # while active_list is not empty, choose random indices to test
    while len(active_list) > 0:
        r = random.randrange(0, len(active_list))
        p = active_list[r]
        k = None

        found_sample = False
        for attempt in range(max_sample_attempts):
            x = sample_2d_annulus(radius, sample[p])

            # check if sample is within shape
            if not shape.contains(x):
                continue

            # check if point is within distance r of existing samples
            k = get_2d_grid_coordinates(x, grid_dx, Vector([xmin, ymin]))
            i_min = max(k.x - 2, 0)
            i_max = min(k.x + 2, dims.x - 1)
            j_min = max(k.y - 2, 0)
            j_max = min(k.y + 2, dims.y - 1)
            
            reject_sample = False
            for i in range(i_min, i_max + 1):
                for j in range(j_min, j_max + 1):
                    # ignore corner cells
                    if i in (i_max, i_min) and j in (j_max, j_min):
                        continue

                    grid_value = background_grid[i][j]
                    if grid_value >= 0 and grid_value != p:
                        if distance_sqrd(x, sample[grid_value]) < radius*radius:
                            # sample is too close to background_grid[k]
                            reject_sample = True
                            break
                if reject_sample:
                    break

            if reject_sample == False:
                found_sample = True
                break

        if found_sample:
            q = len(sample)
            sample.append(x)
            active_list.append(q)
            background_grid[k.x][k.y] = q
            if draw_algorithm:
                # plot sample
                plt.scatter(x.x, x.y, cmap=plt.cm.copper, s=2.0)
                # update drawing
                plt.draw()
                # sleep for a microsecond to allow MPL backend to catch up
                plt.pause(0.001)
        else:
            active_list.pop(r)
            if verbose:
                print("Rejected")
        
        if verbose:
            print("%s Samples, %s Active Points" % (len(sample), len(active_list)))

    if draw_algorithm:
        plt.ioff()

    return sample

def plot_sample(sample, x_limits, y_limits, **kwargs):

    plt.style.use(MPL_STYLE)
    fig = plt.figure(figsize=FIGSIZE, dpi=FIGDPI)
    for s in sample:
        plt.scatter(s.x, s.y, **kwargs)
    fig.axes[0].set_xlim(x_limits)
    fig.axes[0].set_ylim(y_limits)
    return fig

if __name__ == "__main__":

    radius = float(sys.argv[1])

    # shape = shapes.AxisAlignedRectangle(Vector([-1, 0]), Vector([5, 2]))

    a = Vector([-10, -6])
    b = Vector([-5, 5])
    c = Vector([10, 0])
    shape = shapes.Triangle(a, c, b)

    # bl_corner = Vector([-4, -2])
    # dimensions = Vector([8, 10])
    # orientation = 60.0
    # shape = shapes.Rectangle(bl_corner, dimensions, orientation)

    sample = poisson_sample_2d_square(radius, shape, draw_algorithm=False, max_sample_attempts=100)

    fig = plot_sample(sample, (shape.xmin, shape.xmax), (shape.ymin, shape.ymax), s=3.0, cmap=plt.cm.jet)

    plt.show()

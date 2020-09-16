#!/usr/bin/env python3
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import sys
from functools import partial

def distance_sqrd(x, y):
    qsum = 0
    for i in range(len(x)):
        qsum += (y[i] - x[i]) ** 2
    return qsum

def get_2d_grid_coordinates(x, grid_dx, xmin):
    return [math.floor((x[0] - xmin)/ grid_dx), math.floor((x[1] - xmin)/ grid_dx)]

def flatten_2d_index(index, dim):
    return index[1] + index[0] * dim

# returns sample in an annulus around x
def sample_2d_annulus(radius, center):
    r = None
    while True:
        r = np.array([random.uniform(-2, 2), random.uniform(-2, 2)])
        r_sqrd = np.dot(r, r)
        if r_sqrd > 1 and r_sqrd <= 4:
            break;
    return center + radius * r;

# def box_boundary(point, x_lim, y_lim):

def poisson_sample_2d_square(radius, xmin, xmax, max_sample_attempts=30):
    
    plt.ion()
    plt.figure()
    ax = plt.subplot()
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((xmin, xmax))

    # randomize
    random.seed()
    # initialize sample list
    sample = []

    ## Step 0
    # initialize 2D background grid for accelerating spatial search
    grid_dx = radius / math.sqrt(2.0) # contain at most 1 sample 
    dimension = math.ceil((xmax - xmin)/grid_dx)
    # -1 indictes no sample in cell, non-negative is index of sample in cell
    background_grid = np.full((dimension, dimension), -1)

    ## Step 1
    # randomly select initial sample
    x = np.array([random.uniform(xmin, xmax), random.uniform(xmin, xmax)])
    sample.append(x)
    # insert into background grid with the index of the sample
    p = get_2d_grid_coordinates(x, grid_dx, xmin)
    background_grid[p[0]][p[1]] = 0
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

            # check if sample is within bounds
            if x[0] < xmin  or x[1] < xmin or x[0] > xmax or x[1] > xmax:
                continue

            # check if point is within distance r of existing samples
            k = get_2d_grid_coordinates(x, grid_dx, xmin)
            i_min = max(k[0] - 2, 0)
            i_max = min(k[0] + 2, dimension - 1)
            j_min = max(k[1] - 2, 0)
            j_max = min(k[1] + 2, dimension - 1)
            
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
            background_grid[k[0]][k[1]] = q
            plt.scatter(x[0], x[1], cmap=plt.cm.copper, s=1.0)
            plt.draw()
            plt.pause(0.001)
        else:
            active_list.pop(r)
            # active_list[r] = active_list.pop()
            print("Rejected")

        print("%s Samples, %s Active Points" % (len(sample), len(active_list)))

    plt.ioff()

    return sample

if __name__ == "__main__":

    radius = float(sys.argv[1])
    xmin = float(sys.argv[2])
    xmax = float(sys.argv[3])

    sample = poisson_sample_2d_square(radius, xmin, xmax)

    # plot the result
    fig = plt.figure(figsize=[3,3])
    for s in sample:
        plt.scatter(s[0],s[1], color='red', s=1.0)
    fig.axes[0].set_xlim((xmin, xmax))
    fig.axes[0].set_ylim((xmin, xmax))
    plt.show()


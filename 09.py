# --- Day 9: Smoke Basin ---
#
# These caves seem to be lava tubes.  Parts are even still
# volcanically active; small hydrothermal vents release smoke into the
# caves that slowly settles like rain.
#
# If you can model how the smoke flows through the caves, you might be
# able to avoid it and be that much safer.  The submarine generates a
# heightmap of the floor of the nearby caves for you (your puzzle
# input).
#
# Smoke flows to the lowest point of the area it's in.  For example,
# consider the following heightmap:
#
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
#
# Reformatting to support highlighting:
#
#  2 (1) 9  9  9  4  3  2  1 (0)
#  3  9  8  7  8  9  4  9  2  1
#  9  8 (5) 6  7  8  9  8  9  2
#  8  7  6  7  8  9  6  7  8  9
#  9  8  9  9  9  6 (5) 6  7  8
#
# Each number corresponds to the height of a particular location,
# where 9 is the highest and 0 is the lowest a location can be.
#
# Your first goal is to find the low points - the locations that are
# lower than any of its adjacent locations.  Most locations have four
# adjacent locations (up, down, left, and right); locations on the
# edge or corner of the map have three or two adjacent locations,
# respectively.  (Diagonal locations do not count as adjacent.)
#
# In the above example, there are four low points, all highlighted:
# two are in the first row (a 1 and a 0), one is in the third row (a
# 5), and one is in the bottom row (also a 5).  All other locations on
# the heightmap have some lower adjacent location, and so are not low
# points.
#
# The risk level of a low point is 1 plus its height.  In the above
# example, the risk levels of the low points are 2, 1, 6, and 6.  The
# sum of the risk levels of all low points in the heightmap is
# therefore 15.
#
# Find all of the low points on your heightmap.  What is the sum of
# the risk levels of all low points on your heightmap?

from common import neighbors4

grid = [[int(v) for v in l.strip()] for l in open("09.in")]
R, C = len(grid), len(grid[0])  # grid dimensions

lowpoints = [
    (r, c)
    for r in range(R)
    for c in range(C)
    if all(grid[r][c] < grid[nr][nc] for nr, nc in neighbors4(r, c, R, C))
]

print(sum(grid[r][c]+1 for r, c in lowpoints))

# --- Part Two ---
#
# Next, you need to find the largest basins so you know what areas are
# most important to avoid.
#
# A basin is all locations that eventually flow downward to a single
# low point.  Therefore, every low point has a basin, although some
# basins are very small.  Locations of height 9 do not count as being
# in any basin, and all other locations will always be part of exactly
# one basin.
#
# The size of a basin is the number of locations within the basin,
# including the low point.  The example above has four basins.
#
# The top-left basin, size 3:
#
# (2)(1) 9  9  9  4  3  2  1  0
# (3) 9  8  7  8  9  4  9  2  1
#  9  8  5  6  7  8  9  8  9  2
#  8  7  6  7  8  9  6  7  8  9
#  9  8  9  9  9  6  5  6  7  8
#
# The top-right basin, size 9:
#
#  2  1  9  9  9 (4)(3)(2)(1)(0)
#  3  9  8  7  8  9 (4) 9 (2)(1)
#  9  8  5  6  7  8  9  8  9 (2)
#  8  7  6  7  8  9  6  7  8  9
#  9  8  9  9  9  6  5  6  7  8
#
# The middle basin, size 14:
#
#  2  1  9  9  9  4  3  2  1  0
#  3  9 (8)(7)(8) 9  4  9  2  1
#  9 (8)(5)(6)(7)(8) 9  8  9  2
# (8)(7)(6)(7)(8) 9  6  7  8  9
#  9 (8) 9  9  9  6  5  6  7  8
#
# The bottom-right basin, size 9:
#
#  2  1  9  9  9  4  3  2  1  0
#  3  9  8  7  8  9  4  9  2  1
#  9  8  5  6  7  8  9 (8) 9  2
#  8  7  6  7  8  9 (6)(7)(8) 9
#  9  8  9  9  9 (6)(5)(6)(7)(8)
#
# Find the three largest basins and multiply their sizes together.  In
# the above example, this is 9 * 14 * 9 = 1134.
#
# What do you get if you multiply together the sizes of the three
# largest basins?
#
# --------------------
#
# We assume a basin's height increases monotonically until a 9 is
# reached; that is, there are no local maxima, saddles, etc., to deal
# with.

from common import bfs
from functools import reduce
from operator import mul

def flood(node, prev, dist, accum, seen):
    r, c = node
    accum[0] += 1
    return [
        (nr, nc)
        for nr, nc in neighbors4(r, c, R, C)
        if grid[r][c] < grid[nr][nc] < 9
    ]

print(
    reduce(
        mul,
        sorted(bfs(low, flood, accum_start=0) for low in lowpoints)[-3:]
    )
)

# --- Day 19: Beacon Scanner ---
#
# As your probe drifted down through this area, it released an
# assortment of beacons and scanners into the water.  It's difficult
# to navigate in the pitch black open waters of the ocean trench, but
# if you can build a map of the trench using data from the scanners,
# you should be able to safely reach the bottom.
#
# The beacons and scanners float motionless in the water; they're
# designed to maintain the same position for long periods of time.
# Each scanner is capable of detecting all beacons in a large cube
# centered on the scanner; beacons that are at most 1000 units away
# from the scanner in each of the three axes (x, y, and z) have their
# precise position determined relative to the scanner.  However,
# scanners cannot detect other scanners.  The submarine has
# automatically summarized the relative positions of beacons detected
# by each scanner (your puzzle input).
#
# For example, if a scanner is at x,y,z coordinates 500,0,-500 and
# there are beacons at -500,1000,-1500 and 1501,0,-500, the scanner
# could report that the first beacon is at -1000,1000,-1000 (relative
# to the scanner) but would not detect the second beacon at all.
#
# Unfortunately, while each scanner can report the positions of all
# detected beacons relative to itself, the scanners do not know their
# own position.  You'll need to determine the positions of the beacons
# and scanners yourself.
#
# The scanners and beacons map a single contiguous 3d region.  This
# region can be reconstructed by finding pairs of scanners that have
# overlapping detection regions such that there are at least 12
# beacons that both scanners detect within the overlap.  By
# establishing 12 common beacons, you can precisely determine where
# the scanners are relative to each other, allowing you to reconstruct
# the beacon map one scanner at a time.
#
# For a moment, consider only two dimensions.  Suppose you have the
# following scanner reports:
#
# --- scanner 0 ---
# 0,2
# 4,1
# 3,3
#
# --- scanner 1 ---
# -1,-1
# -5,0
# -2,1
#
# Drawing x increasing rightward, y increasing upward, scanners as S,
# and beacons as B, scanner 0 detects this:
#
# ...B.
# B....
# ....B
# S....
#
# Scanner 1 detects this:
#
# ...B..
# B....S
# ....B.
#
# For this example, assume scanners only need 3 overlapping beacons.
# Then, the beacons visible to both scanners overlap to produce the
# following complete map:
#
# ...B..
# B....S
# ....B.
# S.....
#
# Unfortunately, there's a second problem: the scanners also don't
# know their rotation or facing direction.  Due to magnetic alignment,
# each scanner is rotated some integer number of 90-degree turns
# around all of the x, y, and z axes.  That is, one scanner might call
# a direction positive x, while another scanner might call that
# direction negative y.  Or, two scanners might agree on which
# direction is positive x, but one scanner might be upside-down from
# the perspective of the other scanner.  In total, each scanner could
# be in any of 24 different orientations: facing positive or negative
# x, y, or z, and considering any of four directions "up" from that
# facing.
#
# For example, here is an arrangement of beacons as seen from a
# scanner in the same position but in different orientations:
#
# --- scanner 0 ---
# -1,-1,1
# -2,-2,2
# -3,-3,3
# -2,-3,1
# 5,6,-4
# 8,0,7
#
# --- scanner 0 ---
# 1,-1,1
# 2,-2,2
# 3,-3,3
# 2,-1,3
# -5,4,-6
# -8,-7,0
#
# --- scanner 0 ---
# -1,-1,-1
# -2,-2,-2
# -3,-3,-3
# -1,-3,-2
# 4,6,5
# -7,0,8
#
# --- scanner 0 ---
# 1,1,-1
# 2,2,-2
# 3,3,-3
# 1,3,-2
# -4,-6,5
# 7,0,8
#
# --- scanner 0 ---
# 1,1,1
# 2,2,2
# 3,3,3
# 3,1,2
# -6,-4,-5
# 0,7,-8
#
# By finding pairs of scanners that both see at least 12 of the same
# beacons, you can assemble the entire map.  For example, consider the
# following report:
#
# --- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401
#
# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390
#
# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562
#
# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596
#
# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14
#
# Because all coordinates are relative, in this example, all
# "absolute" positions will be expressed relative to scanner 0 (using
# the orientation of scanner 0 and as if scanner 0 is at coordinates
# 0,0,0).
#
# Scanners 0 and 1 have overlapping detection cubes; the 12 beacons
# they both detect (relative to scanner 0) are at the following
# coordinates:
#
# -618,-824,-621
# -537,-823,-458
# -447,-329,318
# 404,-588,-901
# 544,-627,-890
# 528,-643,409
# -661,-816,-575
# 390,-675,-793
# 423,-701,434
# -345,-311,381
# 459,-707,401
# -485,-357,347
#
# These same 12 beacons (in the same order) but from the perspective
# of scanner 1 are:
#
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# -476,619,847
# -460,603,-452
# 729,430,532
# -322,571,750
# -355,545,-477
# 413,935,-424
# -391,539,-444
# 553,889,-390
#
# Because of this, scanner 1 must be at 68,-1246,-43 (relative to
# scanner 0).
#
# Scanner 4 overlaps with scanner 1; the 12 beacons they both detect
# (relative to scanner 0) are:
#
# 459,-707,401
# -739,-1745,668
# -485,-357,347
# 432,-2009,850
# 528,-643,409
# 423,-701,434
# -345,-311,381
# 408,-1815,803
# 534,-1912,768
# -687,-1600,576
# -447,-329,318
# -635,-1737,486
#
# So, scanner 4 is at -20,-1133,1061 (relative to scanner 0).
#
# Following this process, scanner 2 must be at 1105,-1205,1229
# (relative to scanner 0) and scanner 3 must be at -92,-2380,-20
# (relative to scanner 0).
#
# The full list of beacons (relative to scanner 0) is:
#
# -892,524,684
# -876,649,763
# -838,591,734
# -789,900,-551
# -739,-1745,668
# -706,-3180,-659
# -697,-3072,-689
# -689,845,-530
# -687,-1600,576
# -661,-816,-575
# -654,-3158,-753
# -635,-1737,486
# -631,-672,1502
# -624,-1620,1868
# -620,-3212,371
# -618,-824,-621
# -612,-1695,1788
# -601,-1648,-643
# -584,868,-557
# -537,-823,-458
# -532,-1715,1894
# -518,-1681,-600
# -499,-1607,-770
# -485,-357,347
# -470,-3283,303
# -456,-621,1527
# -447,-329,318
# -430,-3130,366
# -413,-627,1469
# -345,-311,381
# -36,-1284,1171
# -27,-1108,-65
# 7,-33,-71
# 12,-2351,-103
# 26,-1119,1091
# 346,-2985,342
# 366,-3059,397
# 377,-2827,367
# 390,-675,-793
# 396,-1931,-563
# 404,-588,-901
# 408,-1815,803
# 423,-701,434
# 432,-2009,850
# 443,580,662
# 455,729,728
# 456,-540,1869
# 459,-707,401
# 465,-695,1988
# 474,580,667
# 496,-1584,1900
# 497,-1838,-617
# 527,-524,1933
# 528,-643,409
# 534,-1912,768
# 544,-627,-890
# 553,345,-567
# 564,392,-477
# 568,-2007,-577
# 605,-1665,1952
# 612,-1593,1893
# 630,319,-379
# 686,-3108,-505
# 776,-3184,-501
# 846,-3110,-434
# 1135,-1161,1235
# 1243,-1093,1063
# 1660,-552,429
# 1693,-557,386
# 1735,-437,1738
# 1749,-1800,1813
# 1772,-405,1572
# 1776,-675,371
# 1779,-442,1789
# 1780,-1548,337
# 1786,-1538,337
# 1847,-1591,415
# 1889,-1729,1762
# 1994,-1805,1792
#
# In total, there are 79 beacons.
#
# Assemble the full map of beacons.  How many beacons are there?
#
# --------------------
#
# The most difficult puzzle of the year!  Fortunately, the input is
# well-behaved in critical ways.
#
# Suppose the pairwise distances between the beacon points are
# distinct.  Our fundamental idea is that distances are invariate
# under isometries, and hence can serve as patterns to match on: if
# two scanners see at least 12 points in common, they will see at
# least (12 2) = 66 distinct distances in common.  Indeed, in our
# input, pairs of scanners see either 66 distances in common or a much
# smaller number.  (The distances in our input are not quite
# completely pairwise distinct: there are a couple repeated distances.
# But the endpoints of those distances are not seen in common, hence
# do not impact our approach.)
#
# We assume that if two scanners see 66 distinct distances in common,
# those distances correspond to 12 points seen in common.  We also
# assume that at least one of those distances has the property that
# the component axis deltas between the two endpoints have distinct,
# nonzero absolute values.  From this one distance and its endpoints
# we can reconstruct the permutation of the axes and the axis
# reflections, and from there the axis offsets between the two
# scanners.

from common import pick, cmp, bfs, bfs_path
from collections import namedtuple
from itertools import combinations, permutations
from math import comb
import re

I = 12  # intersection size
T = comb(I, 2)  # number of common distances
axes = [0, 1, 2]  # axis indexes

class Point(namedtuple("Point_base", "x y z")):

    def __sub__(self, other):
        # Returns the component-wise difference between this point and
        # another.  In a slight abuse of terminology, the return is a
        # Point.
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def abs(self):
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def euclidean2(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2

    def manhattan(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y) + abs(self.z-other.z)

    def axis_deltas_are_distinct(self, other):
        # Returns True if the absolute values of the distances along
        # each axis to another point are all nonzero and all
        # different.
        v = (self-other).abs()
        return 0 not in v and v.x != v.y and v.y != v.z and v.z != v.x

    def permute_axes(self, x_idx, y_idx, z_idx):
        return Point(self[x_idx], self[y_idx], self[z_idx])

class Transform(namedtuple("Transform_base", "p s o")):
    """An isometry, i.e., a rigid affine transformation.

    The transformation is described by `p`, a permutation of axis
    indexes; `s`, +/-1 signs that indicate axis reflections; and `o`,
    axis offsets.  For example, the transformation

    Transform(p=(1, 2, 0), s=(1, -1, -1), o=(2, -3, 5))

    describes transformation equations:

    x =  y + 2
    y = -z - 3
    z = -x + 5

    Or, expressed as a matrix in homogeneous coordinates:

    [ 0  1  0  2]
    [ 0  0 -1 -3]
    [-1  0  0  5]
    [ 0  0  0  1]

    Apply the transformation by treating it as a function and calling
    it on a Point.
    """

    def __call__(self, point):
        return Point(*[point[self.p[i]]*self.s[i]+self.o[i] for i in axes])

    def __mul__(self, other):
        # Returns the functional composition of this transformation
        # with another.
        new_p = tuple(other.p[self.p[i]] for i in axes)
        new_s = tuple(self.s[i]*other.s[self.p[i]] for i in axes)
        new_o = tuple(self.s[i]*other.o[self.p[i]]+self.o[i] for i in axes)
        return Transform(new_p, new_s, new_o)

    def inverse(self):
        new_p = tuple(self.p.index(i) for i in axes)
        new_s = tuple(self.s[new_p[i]] for i in axes)
        new_o = tuple(-self.o[new_p[i]]*self.s[new_p[i]] for i in axes)
        return Transform(new_p, new_s, new_o)

    @staticmethod
    def identity():
        return Transform((0, 1, 2), (1, 1, 1), (0, 0, 0))

# Step 1.  Load the scanners and compute the distances seen by each
# scanner.  Each dictionary in `distances` maps a distance to a pair
# of points, or to a list of pairs of points if the distance is seen
# more than once.  Interestingly, Euclidean distance yields mostly
# distinct distances, whereas Manhattan distance does not.  (Since we
# use distances for comparisons only, we skip taking square roots.)

scanners = [
    set(
        Point(*map(int, re.findall(r"-?\d+", l)))
        for l in section.splitlines()[1:]
    )
    for section in open("19.in").read().split("\n\n")
]
S = len(scanners)  # number of scanners

distances = []  # indexed by scanner
for s in scanners:
    d = {}
    for p1, p2 in combinations(s, 2):
        dist = p1.euclidean2(p2)
        if dist in d:
            if type(d[dist]) is list:
                d[dist].append((p1, p2))
            else:
                d[dist] = [d[dist], (p1, p2)]
        else:
            d[dist] = (p1, p2)
    distances.append(d)

# Step 2.  Compute transformations between those scanners that see
# sufficiently many distances in common.

def make_transform(pdist, qdist, common):
    # In the following, the "p" variables (pdist, pa, pb) are in the
    # destination coordinate system and the "q" variables (qdist, qa,
    # qb, etc.) are in the source coordinate system; this function
    # returns a transformation from q to p.  First, find a distance
    # with distinct axis components between some points a and b.
    d_ab = pick(
        lambda d: pdist[d][0].axis_deltas_are_distinct(pdist[d][1]),
        common
    )
    pa, pb = pdist[d_ab]
    qa, qb = qdist[d_ab]
    # We don't know yet whether qa/qb correspond to pa/pb or vice
    # versa:
    #
    #     =pa        =pb              =pa        =pb
    #     =qa  d_ab  =qb              =qb  d_ab  =qa
    #     (a)--------(b)              (a)--------(b)
    #      |                           |
    # d_ac |               -OR-   d_ac |
    #      |                           |
    #     (c)                         (c)
    #
    # To find out, pick an arbitrary point c connected to point a and
    # use it to disambiguate.
    d_ac = pick(lambda d: d != d_ab and pa in pdist[d], common)
    if qb in qdist[d_ac]:
        qa, qb = qb, qa
    # Now the axis permutation can be uniquely identified.
    permutation = pick(
        lambda p: (
            (qb.permute_axes(*p)-qa.permute_axes(*p)).abs() == (pb-pa).abs()
        ),
        permutations(axes)
    )
    # And from there the reflections and offsets.
    qa_p, qb_p = qa.permute_axes(*permutation), qb.permute_axes(*permutation)
    signs = tuple(
        1 if cmp(pa[i], pb[i]) == cmp(qa_p[i], qb_p[i]) else -1
        for i in axes
    )
    offsets = tuple(pa[i]-signs[i]*qa_p[i] for i in axes)
    return Transform(permutation, signs, offsets)

transforms = {}  # {(i, j): Transform}
for i, j in combinations(range(S), 2):
    common = set(distances[i]) & set(distances[j])
    if len(common) >= T:
        assert all(
            type(distances[i][d]) is tuple and type(distances[j][d]) is tuple
            for d in common
        )
        transforms[(i, j)] = make_transform(distances[i], distances[j], common)

# Step 3.  Transform all points to the coordinate system of scanner 0.
# We don't have transformations in hand for every possible pair of
# scanners, but the transformations we do have form a directed graph
# that connects all scanners.  We use breadth-first search to find a
# path between a scanner and scanner 0, and compute a net
# transformation.

def transform(i, j):
    # Returns a transformation from coordinate system j to coordinate
    # system i.
    if i == j:
        return Transform.identity()
    def visit(node, prev, dist, accum, seen):
        if node == j:
            raise StopIteration(bfs_path(node, seen))
        return (
            [a for a, b in transforms if b == node]
            + [b for a, b in transforms if a == node]
        )
    path = bfs(i, visit)
    t = Transform.identity()
    for k in range(len(path)-1):
        if (path[k], path[k+1]) in transforms:
            t *= transforms[(path[k], path[k+1])]
        else:
            t *= transforms[(path[k+1], path[k])].inverse()
    return t

universe = set()
for i in range(S):
    t = transform(0, i)
    universe.update(t(p) for p in scanners[i])
print(len(universe))

# --- Part Two ---
#
# Sometimes, it's a good idea to appreciate just how big the ocean is.
# Using the Manhattan distance, how far apart do the scanners get?
#
# In the above example, scanners 2 (1105,-1205,1229) and 3
# (-92,-2380,-20) are the largest Manhattan distance apart.  In total,
# they are 1197 + 1175 + 1249 = 3621 units apart.
#
# What is the largest Manhattan distance between any two scanners?

origin = Point(0, 0, 0)
scanner_positions = [transform(0, i)(origin) for i in range(S)]
print(max(a.manhattan(b) for a, b in combinations(scanner_positions, 2)))

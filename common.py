from collections import deque
from heapq import heappush, heappop

def each_do(fn, iterable):
    """Call a function on each item of an iterable.  Inspired by Ruby."""
    for item in iterable:
        fn(item)

def cmp(a, b):
    """Return -1, 0, 1 if a > b, a == b, or a < b.  From Python 2."""
    return (a < b) - (a > b)

def pick(fn, iterable):
    """Return the (first) item of an iterable that matches a predicate."""
    return next(filter(fn, iterable))

def lmap(*args):
    """Materialize a map iterator as a list."""
    return list(map(*args))

def lfilter(*args):
    """Materialize a filter iterator as a list."""
    return list(filter(*args))

def bfs(start_node, visit_fn, accum_start=None):
    """Breadth-first search: call a function on each node visited.

    Nodes can be any hashable quantity.

    The function should have the signature:

        visit_fn(node, prev, dist, accum, seen)
            node: current node
            prev: node that led to current node
            dist: number of steps to current node from start node
            accum: list whose sole element can be used as an accumulator
            seen: search hash table

    The function should either return a list of neighboring nodes to
    visit, or raise StopIteration.

    The return from this function is either the value of the
    StopIteration exception or the accumulator value.

    Idiomatic usages.  To find a node and return a shortest path to
    it:

        def visit(node, prev, dist, accum, seen):
            if node is the one desired:
                raise StopIteration(bfs_path(node, seen))
            return neighbors...

        path = bfs(start_node, visit)

    To count reachable nodes:

        def visit(node, prev, dist, accum, seen):
            accum[0] += 1
            return neighbors...

        num_nodes = bfs(start_node, visit, accum_start=0)
    """
    accum = [accum_start]
    seen = {start_node: None}
    frontier = deque([(start_node, 0)])
    while len(frontier) > 0:
        node, dist = frontier.popleft()
        try:
            neighbors = visit_fn(node, seen[node], dist, accum, seen)
        except StopIteration as e:
            return e.value
        for n in neighbors:
            if n not in seen:
                seen[n] = node
                frontier.append((n, dist+1))
    return accum[0]

def bfs_path(to_node, seen):
    """Companion function to bfs; return the path to a node."""
    path = []
    p = to_node
    while p != None:
        path.append(p)
        p = seen[p]
    path.reverse()
    return path

def a_star(start_node, goal_node, visit_fn):
    """A* search: return a lowest cost path to a goal node.

    Nodes can be any hashable and equality-testable quantity.

    The function should have the signature visit_fn(node) and is
    called on each visited node.  It should return a list of tuples
    (n, c, h) where n is a neighboring node to visit, c is the cost of
    moving from the visited node to the neighboring node, and h is a
    heuristic estimate of the cost of moving from the neighboring node
    to the goal node.

    If the heuristic is admissible (never overestimates the actual
    lowest cost) then a lowest cost path will be returned.  If the
    heuristic is always zero, the algorithm falls back to Djikstra's.

    The return is a list of tuples [(node, cumulative cost), ...].  If
    the goal node is not found, None is returned.
    """
    def serial_num(num=[0]):
        # In the heap it may happen that two nodes have the same
        # priority.  To avoid assuming that nodes can be compared, we
        # use this function to insert a unique serial number.
        num[0] += 1
        return num[0]
    frontier = [(0, serial_num(), start_node)]
    costs = {start_node: 0}  # lowest costs seen so far; subject to revision
    previous = {start_node: (None, 0)}
    while len(frontier) > 0:
        node = heappop(frontier)[2]
        if node == goal_node:
            path = []
            p = node
            while p != None:
                path.append((p, previous[p][1]))
                p = previous[p][0]
            path.reverse()
            return path
        for n, c, h in visit_fn(node):
            g = costs[node] + c
            if n not in costs or g < costs[n]:
                costs[n] = g
                previous[n] = (node, g)
                heappush(frontier, (g+h, serial_num(), n))
    return None

def neighbors4(*args):
    """Return a grid cell's 4 (up/down/left/right) neighbors.
    Optionally return only those cells whose coodinates are within
    [0, xlim) and [0, ylim).

    Call as follows:
        neighbors4((x, y))
        neighbors4(x, y)
        neighbors4((x, y), xlim, ylim)
        neighbors4(x, y, xlim, ylim)
    """
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return _neighbors(deltas, *args)

def neighbors8(*args):
    """Return a grid cell's 8 (up/down/left/right/diagonal) neighbors.
    Optionally return only those cells whose coodinates are within
    [0, xlim) and [0, ylim).

    Call as follows:
        neighbors8((x, y))
        neighbors8(x, y)
        neighbors8((x, y), xlim, ylim)
        neighbors8(x, y, xlim, ylim)
    """
    deltas = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]
    return _neighbors(deltas, *args)

def _neighbors(*args):
    deltas = args[0]
    if len(args)%2 == 0:
        x, y = args[1]
    else:
        x, y = args[1:3]
    if len(args) > 3:
        xlim, ylim = args[-2:]
    else:
        xlim = ylim = None
    return [
        (x+dx, y+dy)
        for dx, dy in deltas
        if xlim == None or (0 <= x+dx < xlim and 0 <= y+dy < ylim)
    ]

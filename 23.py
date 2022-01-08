# --- Day 23: Amphipod ---
#
# A group of amphipods notice your fancy submarine and flag you down.
# "With such an impressive shell," one amphipod says, "surely you can
# help us with a question that has stumped our best scientists."
#
# They go on to explain that a group of timid, stubborn amphipods live
# in a nearby burrow.  Four types of amphipods live there: Amber (A),
# Bronze (B), Copper (C), and Desert (D).  They live in a burrow that
# consists of a hallway and four side rooms.  The side rooms are
# initially full of amphipods, and the hallway is initially empty.
#
# They give you a diagram of the situation (your puzzle input),
# including locations of each amphipod (A, B, C, or D, each of which
# is occupying an otherwise open space), walls (#), and open space
# (.).
#
# For example:
#
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
#
# The amphipods would like a method to organize every amphipod into
# side rooms so that each side room contains one type of amphipod and
# the types are sorted A-D going left to right, like this:
#
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #########
#
# Amphipods can move up, down, left, or right so long as they are
# moving into an unoccupied open space.  Each type of amphipod
# requires a different amount of energy to move one step: Amber
# amphipods require 1 energy per step, Bronze amphipods require 10
# energy, Copper amphipods require 100, and Desert ones require 1000.
# The amphipods would like you to find a way to organize the amphipods
# that requires the least total energy.
#
# However, because they are timid and stubborn, the amphipods have
# some extra rules:
#
# - Amphipods will never stop on the space immediately outside any
#   room.  They can move into that space so long as they immediately
#   continue moving.  (Specifically, this refers to the four open
#   spaces in the hallway that are directly above an amphipod starting
#   position.)
# - Amphipods will never move from the hallway into a room unless that
#   room is their destination room and that room contains no amphipods
#   which do not also have that room as their own destination.  If an
#   amphipod's starting room is not its destination room, it can stay
#   in that room until it leaves the room.  (For example, an Amber
#   amphipod will not move from the hallway into the right three
#   rooms, and will only move into the leftmost room if that room is
#   empty or if it only contains other Amber amphipods.)
# - Once an amphipod stops moving in the hallway, it will stay in that
#   spot until it can move into a room.  (That is, once any amphipod
#   starts moving, any other amphipods currently in the hallway are
#   locked in place and will not move again until they can move fully
#   into a room.)
#
# In the above example, the amphipods can be organized using a minimum
# of 12521 energy.  One way to do this is shown below.
#
# Starting configuration:
#
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
#
# One Bronze amphipod moves into the hallway, taking 4 steps and using
# 40 energy:
#
# #############
# #...B.......#
# ###B#C#.#D###
#   #A#D#C#A#
#   #########
#
# The only Copper amphipod not in its side room moves there, taking 4
# steps and using 400 energy:
#
# #############
# #...B.......#
# ###B#.#C#D###
#   #A#D#C#A#
#   #########
#
# A Desert amphipod moves out of the way, taking 3 steps and using
# 3000 energy, and then the Bronze amphipod takes its place, taking 3
# steps and using 30 energy:
#
# #############
# #.....D.....#
# ###B#.#C#D###
#   #A#B#C#A#
#   #########
#
# The leftmost Bronze amphipod moves to its room using 40 energy:
#
# #############
# #.....D.....#
# ###.#B#C#D###
#   #A#B#C#A#
#   #########
#
# Both amphipods in the rightmost room move into the hallway, using
# 2003 energy in total:
#
# #############
# #.....D.D.A.#
# ###.#B#C#.###
#   #A#B#C#.#
#   #########
#
# Both Desert amphipods move into the rightmost room using 7000
# energy:
#
# #############
# #.........A.#
# ###.#B#C#D###
#   #A#B#C#D#
#   #########
#
# Finally, the last Amber amphipod moves into its room, using 8
# energy:
#
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #########
#
# What is the least energy required to organize the amphipods?
#
# --------------------
#
# The hardest part about this puzzle was finding a representation that
# allows the logic of the puzzle to be succinctly and clearly
# expressed.  Unfortunately, in even this, our second attempt, the
# logic is complicated and the expression unsatisfactory.
#
# Run this program with a "visualize" argument to see the movement of
# the amphipods animated.

from common import a_star
from collections import namedtuple
import sys
from time import sleep

visualize = (len(sys.argv) > 1 and sys.argv[1] == "visualize")
if visualize:
    import curses
    stdscr = curses.initscr()

# N.B.: Of the constants below, only the room depth is truly variable.

R = H = 4  # number of rooms; hallway index
D = 2  # room depth

cost_factor = {"A": 1, "B": 10, "C": 100, "D": 1000}
room_type = ["A", "B", "C", "D"]
room_pos = [2, 4, 6, 8]  # relative to hallway
goal_pos = {"A": 2, "B": 4, "C": 6, "D": 8}  # relative to hallway
goal_idx = {"A": 0, "B": 1, "C": 2, "D": 3}

class Room(str):
    """A room with occupants listed in order of depth, e.g., ".A"."""

    def occupants(self):
        return [(a, d) for d, a in enumerate(self) if a != "."]

    def first_occupant(self):
        try:
            return self.occupants()[0]
        except IndexError:
            return (None, -1)

    def enterable(self, type):
        # Returns True if the room can be entered by an amphipod that
        # has the room as its goal, which is to say, is only occupied
        # by amphipods of type `type`, the correct type.
        return all(self[d] == "." or self[d] == type for d in range(D))

    def num_open_spaces(self):
        return self.count(".")

class State(namedtuple("State_base", "room_a room_b room_c room_d hallway")):
    """An amphipod state.

    A state is represented as a tuple of 5 strings: (room A, room B,
    room C, room D, hallway).  Room occupants are listed in vertical
    descending order.  For example, the state

    #############
    #.....D.D.A.#
    ###.#B#C#.###
      #A#B#C#.#
      #########

    is represented as

    (Room(".A"), Room("BB"), Room("CC"), Room(".."), ".....D.D.A.").
    """

    @staticmethod
    def new(lines):
        rooms = [
            Room("".join(lines[d+2][r*2+3] for d in range(D)))
            for r in range(R)
        ]
        return State(*rooms, lines[1][1:-1])

    def __str__(self):
        rooms = [
            "#" + "".join(f"{self[r][d]}#" for r in range(R))
            for d in range(D)
        ]
        return (
            f"#############\n#{self.hallway}#\n##{rooms[0]}##\n"
            + "\n".join("  "+r for r in rooms[1:])
            + "\n  #########"
        )

    def hallway_range(self, r):
        # Returns the range of hallway positions that are accessible
        # from the room at room index `r`.
        i = room_pos[r]
        while i >= 0 and self.hallway[i] == ".":
            i -= 1
        j = room_pos[r]
        while j < len(self.hallway) and self.hallway[j] == ".":
            j += 1
        return range(i+1, j)

    def enterable(self, r):
        # Returns True if the room at room index `r` is enterable.
        return self[r].enterable(room_type[r])

    def move(self, from_r, from_d, to_r, to_d):
        # Returns a new state that reflects moving an amphipod.  An
        # amphipod position is described by a room index and depth
        # (the hallway is treated as a room here).
        l = [list(room) for room in self]
        l[from_r][from_d], l[to_r][to_d] = l[to_r][to_d], l[from_r][from_d]
        return State(*[Room("".join(r)) for r in l[:R]], "".join(l[H]))

    def next_moves(self):
        l = []
        def add(new_state, type, distance):
            l.append(
                (new_state, distance*cost_factor[type], new_state.h_func())
            )
        # Case 1: amphipods that can be moved out of their current
        # rooms, to the hallway or directly to their goal rooms.
        for r in range(R):  # for each room
            # Only the first occupant can be moved (all others are
            # blocked).  But if the first occupant and all others in
            # the room are already of the correct type, there is
            # nothing gained by moving it.
            a, d = self[r].first_occupant()
            if a != None and not self.enterable(r):
                hr = self.hallway_range(r)
                # Case 1a: moves to the hallway.
                for i in hr:
                    if i not in room_pos:  # avoid spaces in front of rooms
                        add(self.move(r, d, H, i), a, abs(room_pos[r]-i)+d+1)
                # Case 1b: move to the goal room.
                gr = goal_idx[a]  # goal room
                if gr != r and room_pos[gr] in hr and self.enterable(gr):
                    gd = self[gr].num_open_spaces()  # goal room depth
                    add(
                        self.move(r, d, gr, gd-1),
                        a,
                        abs(room_pos[r]-room_pos[gr])+d+1+gd
                    )
        # Case 2: amphipods that can be moved from the hallway to
        # their goal rooms.
        for i, a in enumerate(self.hallway):
            if a != ".":
                gr = goal_idx[a]  # goal room
                hr = self.hallway_range(gr)
                if (i-1 in hr or i+1 in hr) and self.enterable(gr):
                    gd = self[gr].num_open_spaces()  # goal room depth
                    add(
                        self.move(H, i, gr, gd-1),
                        a,
                        abs(i-room_pos[gr])+gd
                    )
        return l

    def h_func(self):
        # Our heuristic function for the A* search returns a good, but
        # underestimated cost by taking into account the distance each
        # out-of-place amphipod needs to travel out of its current
        # room, along the hallway, and at least one step down into its
        # goal room.  Other required moves (e.g., to get out of the
        # way) are not considered.
        h = 0
        for r in range(R):
            for a, d in self[r].occupants():
                if a != room_type[r]:
                    h += (abs(room_pos[r]-goal_pos[a])+d+2)*cost_factor[a]
        for i, a in enumerate(self.hallway):
            if a != ".":
                h += (abs(i-goal_pos[a])+1)*cost_factor[a]
        return h

def animate(states):
    def draw(s, highlight_idx=None):
        stdscr.clear()
        for i in range(len(s)):
            stdscr.addch(s[i], curses.A_STANDOUT if i == highlight_idx else 0)
        stdscr.refresh()
        sleep(.5)
    prev_s = None
    for s in map(str, states):
        if prev_s != None:
            from_ = to = None
            for i in range(len(s)):
                if s[i] != prev_s[i]:
                    if s[i] == ".":
                        from_ = i
                    else:
                         to = i
            draw(prev_s, from_)
            draw(s, to)
        draw(s)
        sleep(.5)
        prev_s = s

start = open("23.in").read().splitlines()

goal = [
    "#############",
    "#...........#",
    "###A#B#C#D###",
    "  #A#B#C#D#",
    "  #########"
]

path = a_star(State.new(start), State.new(goal), State.next_moves)

if visualize:
    animate(p[0] for p in path)
else:
    print(path[-1][1])

# --- Part Two ---
#
# As you prepare to give the amphipods your solution, you notice that
# the diagram they handed you was actually folded up.  As you unfold
# it, you discover an extra part of the diagram.
#
# Between the first and second lines of text that contain amphipod
# starting positions, insert the following lines:
#
#   #D#C#B#A#
#   #D#B#A#C#
#
# So, the above example now becomes:
#
# #############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# The amphipods still want to be organized into rooms similar to
# before:
#
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# In this updated example, the least energy required to organize these
# amphipods is 44169:
#
# #############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #..........D#
# ###B#C#B#.###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A.........D#
# ###B#C#B#.###
#   #D#C#B#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A........BD#
# ###B#C#.#.###
#   #D#C#B#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A......B.BD#
# ###B#C#.#.###
#   #D#C#.#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#C#.#.###
#   #D#C#.#.#
#   #D#B#.#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#.#.#.###
#   #D#C#.#.#
#   #D#B#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#B#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA...B.B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.D.B.B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#.#C#A#
#   #########
#
# #############
# #AA.D...B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D.....BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#B#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D......D#
# ###B#.#.#.###
#   #D#B#C#.#
#   #D#B#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D......D#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D.....AD#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#.#
#   #########
#
# #############
# #AA.......AD#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.......AD#
# ###.#B#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.......AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #D#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.D.....AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #.#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #A..D.....AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #...D.....AD#
# ###.#B#C#.###
#   #A#B#C#.#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #.........AD#
# ###.#B#C#.###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #..........D#
# ###A#B#C#.###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# Using the initial configuration from the full diagram, what is the
# least energy required to organize the amphipods?

D = 4

start = start[:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + start[3:]
goal  = goal[:3]  + ["  #A#B#C#D#", "  #A#B#C#D#"] + goal[3:]

path = a_star(State.new(start), State.new(goal), State.next_moves)

if visualize:
    animate(p[0] for p in path)
    curses.endwin()
else:
    print(path[-1][1])

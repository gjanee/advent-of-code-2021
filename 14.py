# --- Day 14: Extended Polymerization ---
#
# The incredible pressures at this depth are starting to put a strain
# on your submarine.  The submarine has polymerization equipment that
# would produce suitable materials to reinforce the submarine, and the
# nearby volcanically-active caves should even have the necessary
# input elements in sufficient quantities.
#
# The submarine manual contains instructions for finding the optimal
# polymer formula; specifically, it offers a polymer template and a
# list of pair insertion rules (your puzzle input).  You just need to
# work out what polymer would result after repeating the pair
# insertion process a few times.
#
# For example:
#
# NNCB
#
# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C
#
# The first line is the polymer template - this is the starting point
# of the process.
#
# The following section defines the pair insertion rules.  A rule like
# AB -> C means that when elements A and B are immediately adjacent,
# element C should be inserted between them.  These insertions all
# happen simultaneously.
#
# So, starting with the polymer template NNCB, the first step
# simultaneously considers all three pairs:
#
# - The first pair (NN) matches the rule NN -> C, so element C is
#   inserted between the first N and the second N.
# - The second pair (NC) matches the rule NC -> B, so element B is
#   inserted between the N and the C.
# - The third pair (CB) matches the rule CB -> H, so element H is
#   inserted between the C and the B.
#
# Note that these pairs overlap: the second element of one pair is the
# first element of the next pair.  Also, because all pairs are
# considered simultaneously, inserted elements are not considered to
# be part of a pair until the next step.
#
# After the first step of this process, the polymer becomes NCNBCHB.
#
# Here are the results of a few steps using the above rules:
#
# Template:     NNCB
# After step 1: NCNBCHB
# After step 2: NBCCNBBBCBHCB
# After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
# After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
#
# This polymer grows quickly.  After step 5, it has length 97; after
# step 10, it has length 3073.  After step 10, B occurs 1749 times, C
# occurs 298 times, H occurs 161 times, and N occurs 865 times; taking
# the quantity of the most common element (B, 1749) and subtracting
# the quantity of the least common element (H, 161) produces
# 1749 - 161 = 1588.
#
# Apply 10 steps of pair insertion to the polymer template and find
# the most and least common elements in the result.  What do you get
# if you take the quantity of the most common element and subtract the
# quantity of the least common element?
#
# --------------------
#
# The polymer doubles in length with every step, and given that part 2
# will surely want to go past 10 steps, we take a cue from the
# lanternfish puzzle (day 6) and count numbers of things as opposed to
# tracking arrangements of things.  The trick here is that, while we
# ultimately want to count elements, the things of interest are the
# pairs, and instead of viewing a rule as inserting an element in a
# pair, we view it as generating two new pairs from a pair.  From
# pairs we can count elements.  Because pairs overlap, every element
# will be counted twice, except for the first and last elements of the
# template, which are counted only once (and which never change).

from collections import Counter

template, p2 = open("14.in").read().split("\n\n")
rules = {
    from_: [from_[0]+to, to+from_[1]]
    for from_, _, to in map(str.split, p2.splitlines())
}

def step(counter):
    c = Counter()
    for p, v in counter.items():
        a, b = rules[p]
        c[a] += v
        c[b] += v
    return c

def tally_elements(counter, first_element, last_element):
    c = Counter()
    for p, v in counter.items():
        c[p[0]] += v
        c[p[1]] += v
    for e, v in c.items():
        if e == first_element:
            v += 1
        if e == last_element:
            v += 1
        c[e] = v//2
    return c

def solve(num_steps):
    c = Counter(template[i:i+2] for i in range(len(template)-1))
    for _ in range(num_steps):
        c = step(c)
    a = tally_elements(c, template[0], template[-1]).most_common()
    return a[0][1]-a[-1][1]

print(solve(10))

# --- Part Two ---
#
# The resulting polymer isn't nearly strong enough to reinforce the
# submarine.  You'll need to run more steps of the pair insertion
# process; a total of 40 steps should do it.
#
# In the above example, the most common element is B (occurring
# 2192039569602 times) and the least common element is H (occurring
# 3849876073 times); subtracting these produces 2188189693529.
#
# Apply 40 steps of pair insertion to the polymer template and find
# the most and least common elements in the result.  What do you get
# if you take the quantity of the most common element and subtract the
# quantity of the least common element?

print(solve(40))

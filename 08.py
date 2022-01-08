# --- Day 8: Seven Segment Search ---
#
# You barely reach the safety of the cave when the whale smashes into
# the cave mouth, collapsing it.  Sensors indicate another exit to
# this cave at a much greater depth, so you have no choice but to
# press on.
#
# As your submarine slowly makes its way through the cave system, you
# notice that the four-digit seven-segment displays in your submarine
# are malfunctioning; they must have been damaged during the escape.
# You'll be in a lot of trouble without them, so you'd better figure
# out what's wrong.
#
# Each digit of a seven-segment display is rendered by turning on or
# off any of seven segments named a through g:
#
#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
#
# So, to render a 1, only segments c and f would be turned on; the
# rest would be off.  To render a 7, only segments a, c, and f would
# be turned on.
#
# The problem is that the signals which control the segments have been
# mixed up on each display.  The submarine is still trying to display
# numbers by producing output on signal wires a through g, but those
# wires are connected to segments randomly.  Worse, the wire/segment
# connections are mixed up separately for each four-digit display!
# (All of the digits within a display use the same connections,
# though.)
#
# So, you might know that only signal wires b and g are turned on, but
# that doesn't mean segments b and g are turned on: the only digit
# that uses two segments is 1, so it must mean segments c and f are
# meant to be on.  With just that information, you still can't tell
# which wire (b/g) goes to which segment (c/f).  For that, you'll need
# to collect more information.
#
# For each display, you watch the changing signals for a while, make a
# note of all ten unique signal patterns you see, and then write down
# a single four digit output value (your puzzle input).  Using the
# signal patterns, you should be able to work out which pattern
# corresponds to which digit.
#
# For example, here is what you might see in a single entry in your
# notes:
#
# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
# cdfeb fcadb cdfeb cdbaf
#
# (The entry is wrapped here to two lines so it fits; in your notes,
# it will all be on a single line.)
#
# Each entry consists of ten unique signal patterns, a | delimiter,
# and finally the four digit output value.  Within an entry, the same
# wire/segment connections are used (but you don't know what the
# connections actually are).  The unique signal patterns correspond to
# the ten different ways the submarine tries to render a digit using
# the current wire/segment connections.  Because 7 is the only digit
# that uses three segments, dab in the above example means that to
# render a 7, signal lines d, a, and b are on.  Because 4 is the only
# digit that uses four segments, eafb means that to render a 4, signal
# lines e, a, f, and b are on.
#
# Using this information, you should be able to work out which
# combination of signal wires corresponds to each of the ten digits.
# Then, you can decode the four digit output value.  Unfortunately, in
# the above example, all of the digits in the output value (cdfeb
# fcadb cdfeb cdbaf) use five segments and are more difficult to
# deduce.
#
# For now, focus on the easy digits. Consider this larger example:
#
# be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
# fdgacbe cefdb cefbgd gcbe
# edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
# fcgedb cgb dgebacf gc
# fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
# cg cg fdcagb cbg
# fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
# efabcd cedba gadfec cb
# aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
# gecf egdcabf bgf bfgea
# fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
# gebdcfa ecba ca fadegcb
# dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
# cefg dcbef fcge gbcadfe
# bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
# ed bcgafe cdgba cbgef
# egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
# gbdfcae bgc cg cgb
# gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
# fgae cfgab fg bagce
#
# Because the digits 1, 4, 7, and 8 each use a unique number of
# segments, you should be able to tell which combinations of signals
# correspond to those digits.  Counting only digits in the output
# values (the part after | on each line), in the above example, there
# are 26 instances of digits that use a unique number of segments.
#
# In the output values, how many times do digits 1, 4, 7, or 8 appear?
#
# --------------------
#
# This was a head-scratcher.  To clarify: to the left of the |
# delimiter are 10 patterns corresponding to the digits 0-9 in some
# order and using an unknown encoding; within each pattern the wire
# codes are listed in random order; and to the right of the |
# delimiter are 4 digits (that form a single number) that use that
# same encoding.

print(
    sum(
        sum(map(lambda p: len(p) in [2, 3, 4, 7], l.split("|")[1].split()))
        for l in open("08.in")
    )
)

# --- Part Two ---
#
# Through a little deduction, you should now be able to determine the
# remaining digits.  Consider again the first example above:
#
# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
# cdfeb fcadb cdfeb cdbaf
#
# After some careful analysis, the mapping between signal wires and
# segments only makes sense in the following configuration:
#
#  dddd
# e    a
# e    a
#  ffff
# g    b
# g    b
#  cccc
#
# So, the unique signal patterns would correspond to the following
# digits:
#
# - acedgfb: 8
# - cdfbe: 5
# - gcdfa: 2
# - fbcad: 3
# - dab: 7
# - cefabd: 9
# - cdfgeb: 6
# - eafb: 4
# - cagedb: 0
# - ab: 1
#
# Then, the four digits of the output value can be decoded:
#
# - cdfeb: 5
# - fcadb: 3
# - cdfeb: 5
# - cdbaf: 3
#
# Therefore, the output value for this entry is 5353.
#
# Following this same process for each entry in the second, larger
# example above, the output value of each entry can be determined:
#
# - fdgacbe cefdb cefbgd gcbe: 8394
# - fcgedb cgb dgebacf gc: 9781
# - cg cg fdcagb cbg: 1197
# - efabcd cedba gadfec cb: 9361
# - gecf egdcabf bgf bfgea: 4873
# - gebdcfa ecba ca fadegcb: 8418
# - cefg dcbef fcge gbcadfe: 4548
# - ed bcgafe cdgba cbgef: 1625
# - gbdfcae bgc cg cgb: 8717
# - fgae cfgab fg bagce: 4315
#
# Adding all of the output values in this larger example produces
# 61229.
#
# For each entry, determine all of the wire/segment connections and
# decode the four-digit output values.  What do you get if you add up
# all of the output values?
#
# --------------------
#
# We don't need to go to the trouble of determining the correspondence
# between wire codes and segments.  Using pattern lengths and subset
# relationships, we can determine just the correspondence between
# patterns and digits which is all we need anyway.  For example, the
# pattern for digit 4 is uniquely determined by its length as noted
# above; and then, the pattern for digit 9 is the unique pattern of
# length 6 for which the pattern for digit 4 is a subset; and so
# forth.

from common import pick, lmap

def decode(patterns):
    # patterns: list of sets
    def has_len(n):
        return lambda p: len(p) == n
    def all_of_len(n):
        return filter(has_len(n), patterns)
    nums = [None]*10
    nums[1] = pick(has_len(2), patterns)
    nums[7] = pick(has_len(3), patterns)
    nums[4] = pick(has_len(4), patterns)
    nums[8] = pick(has_len(7), patterns)
    nums[9] = pick(lambda p: nums[4] < p, all_of_len(6))
    nums[2] = pick(lambda p: not (p < nums[9]), all_of_len(5))
    nums[5] = pick(lambda p: nums[9]-nums[2] < p, all_of_len(5))
    nums[3] = pick(lambda p: p != nums[2] and p != nums[5], all_of_len(5))
    nums[6] = pick(lambda p: p&nums[4] < nums[5], all_of_len(6))
    nums[0] = pick(lambda p: p != nums[6] and p != nums[9], all_of_len(6))
    return nums

total = 0
for patterns, outputs in [
    [lmap(set, l) for l in map(str.split, line.split("|"))]
    for line in open("08.in")
]:
    mapping = decode(patterns)
    total += int("".join(str(mapping.index(p)) for p in outputs))
print(total)

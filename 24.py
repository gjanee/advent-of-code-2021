# -- Day 24: Arithmetic Logic Unit ---
#
# Magic smoke starts leaking from the submarine's arithmetic logic
# unit (ALU).  Without the ability to perform basic arithmetic and
# logic functions, the submarine can't produce cool patterns with its
# Christmas lights!
#
# It also can't navigate.  Or run the oxygen system.
#
# Don't worry, though - you probably have enough oxygen left to give
# you enough time to build a new ALU.
#
# The ALU is a four-dimensional processing unit: it has integer
# variables w, x, y, and z.  These variables all start with the value
# 0.  The ALU also supports six instructions:
#
# - inp a - Read an input value and write it to variable a.
# - add a b - Add the value of a to the value of b, then store the
#   result in variable a.
# - mul a b - Multiply the value of a by the value of b, then store
#   the result in variable a.
# - div a b - Divide the value of a by the value of b, truncate the
#   result to an integer, then store the result in variable a.  (Here,
#   "truncate" means to round the value toward zero.)
# - mod a b - Divide the value of a by the value of b, then store the
#   remainder in variable a.  (This is also called the modulo
#   operation.)
# - eql a b - If the value of a and b are equal, then store the value
#   1 in variable a.  Otherwise, store the value 0 in variable a.
#
# In all of these instructions, a and b are placeholders; a will
# always be the variable where the result of the operation is stored
# (one of w, x, y, or z), while b can be either a variable or a
# number.  Numbers can be positive or negative, but will always be
# integers.
#
# The ALU has no jump instructions; in an ALU program, every
# instruction is run exactly once in order from top to bottom.  The
# program halts after the last instruction has finished executing.
#
# (Program authors should be especially cautious; attempting to
# execute div with b=0 or attempting to execute mod with a<0 or b<=0
# will cause the program to crash and might even damage the ALU.
# These operations are never intended in any serious ALU program.)
#
# For example, here is an ALU program which takes an input number,
# negates it, and stores it in x:
#
# inp x
# mul x -1
#
# Here is an ALU program which takes two input numbers, then sets z to
# 1 if the second input number is three times larger than the first
# input number, or sets z to 0 otherwise:
#
# inp z
# inp x
# mul z 3
# eql z x
#
# Here is an ALU program which takes a non-negative integer as input,
# converts it into binary, and stores the lowest (1's) bit in z, the
# second-lowest (2's) bit in y, the third-lowest (4's) bit in x, and
# the fourth-lowest (8's) bit in w:
#
# inp w
# add z w
# mod z 2
# div w 2
# add y w
# mod y 2
# div w 2
# add x w
# mod x 2
# div w 2
# mod w 2
#
# Once you have built a replacement ALU, you can install it in the
# submarine, which will immediately resume what it was doing when the
# ALU failed: validating the submarine's model number.  To do this,
# the ALU will run the MOdel Number Automatic Detector program (MONAD,
# your puzzle input).
#
# Submarine model numbers are always fourteen-digit numbers consisting
# only of digits 1 through 9.  The digit 0 cannot appear in a model
# number.
#
# When MONAD checks a hypothetical fourteen-digit model number, it
# uses fourteen separate inp instructions, each expecting a single
# digit of the model number in order of most to least significant.
# (So, to check the model number 13579246899999, you would give 1 to
# the first inp instruction, 3 to the second inp instruction, 5 to the
# third inp instruction, and so on.)  This means that when operating
# MONAD, each input instruction should only ever be given an integer
# value of at least 1 and at most 9.
#
# Then, after MONAD has finished running all of its instructions, it
# will indicate that the model number was valid by leaving a 0 in
# variable z.  However, if the model number was invalid, it will leave
# some other non-zero value in z.
#
# MONAD imposes additional, mysterious restrictions on model numbers,
# and legend says the last copy of the MONAD documentation was eaten
# by a tanuki.  You'll need to figure out what MONAD does some other
# way.
#
# To enable as many submarine features as possible, find the largest
# valid fourteen-digit model number that contains no 0 digits.  What
# is the largest model number accepted by MONAD?
#
# --------------------
#
# We solve this puzzle entirely analytically (after a lot of
# analysis!).  The program consists of 14 segments that are
# near-identical.  Each has the form:
#
# inp w
# mul x 0
# add x z
# mod x 26
# div z A
# add x B
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y C
# mul y x
# add z y
#
# A, B, C in the above are meta-variables that vary across the
# segments (they are the only things to vary).  In every segment
# meta-variable A is either 1 or 26.  A few observations:
#
# - w's only purpose is to hold the next digit of the model number.
#   It is otherwise never modified.
# - x and y are set to new values (notice how multiplying by zero acts
#   as a reset instruction) and therefore serve as temporary variables
#   within a segment.
# - z's running value is passed in from the previous segment, is
#   modified, and gets passed to the next segment.
#
# Expressing the segment in Python syntax and simplifying:
#
# w = <next digit>
# x = z%26+B
# z //= A (assuming z is positive, which it will turn out to be)
# x = (0 if w == x else 1)
# z *= 25*x+1
# z += (w+C)*x
#
# Notice that when x = 0, the last two modifications to z effectively
# turn into no-ops.  Simplifying further:
#
# w = <next digit>
# if w == z%26+B:
#     z //= A
# else:
#     z //= A
#     z = z*26 + w+C
#
# As noted previously, meta-variable A is only either 1 or 26.  The
# operation z //= 1 is a no-op.  The divisions, multiplications, and
# modulus operations against 26 strongly suggest z being interpretable
# as a base-26 number.  This view is supported by the fact that
# 0 <= C <= 15, so that 0 < w+C <= 24.  So each segment uses the last
# digit of this base-26 number in a test, and conditionally pops a
# digit off and/or pushes a new digit.
#
# So how can z end up equalling zero?  Since the only operations on z
# are pushing a nonzero base-26 digit on or popping one off, the only
# hope is that the number of digits popped off at least equals the
# number of digits pushed on.  Sure enough, the 14 segments divide
# into two types of 7 segments each (the two types are intermixed):
#
# - The test will always fail (e.g., testing w == z%26+13 will always
#   fail because 1 <= w <= 9).  In this type A = 1, so the segment
#   unconditionally pushes a digit onto z.
# - The test has the possibility of succeeding.  In this type A = 26,
#   so if the test actually succeeds a digit will be popped off
#   without a new digit being pushed on.
#
# If every test in the latter type of segment succeeds, then the
# number of pops will equal the number of pushes.  If the digits of
# the model number are denoted d1 through d14, we can recast our input
# program as follows, where the push and pop operations use z as a
# kind of stack:
#
# push d1
# push d2+3
# push d3+8
# test: d4 == d3+3
# pop
# push d5+13
# push d6+9
# push d7+6
# test: d8 == d7-8
# pop
# test: d9 == d6+1
# pop
# push d10+2
# test: d11 == d10+2
# pop
# test: d12 == d5+8
# pop
# test: d13 == d2-6
# pop
# test: d14 == d1-1
# pop
#
# Applying the required relationships between the digits and deducing
# constraints on digit ranges yields the following:
#
# d1  2..9
# d2  7..9
# d3  1..6
# d4  = d3+3
# d5  1
# d6  1..8
# d7  9
# d8  = d7-8
# d9  = d6+1
# d10 1..7
# d11 = d10+2
# d12 = d5+8
# d13 = d2-6
# d14 = d1-1
#
# At this point the maximum valid model number can simply be read off.

print(99691891979938)

# --- Part Two ---
#
# As the submarine starts booting up things like the Retro
# Encabulator, you realize that maybe you don't need all these
# submarine features after all.
#
# What is the smallest model number accepted by MONAD?

print(27141191213911)

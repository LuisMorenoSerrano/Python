# Scenario:
#
# Listen to this story: a boy and his father, a computer programmer, are playing
# with wooden blocks. They are building a pyramid.
#
# Their pyramid is a bit weird, as it is actually a pyramid-shaped wall - it's flat.
# The pyramid is stacked according to one simple principle: each lower layer contains
# one block more than the layer above.
#
# The figure illustrates the rule used by the builders:
#
#     +---+
#     |   |
#     +---+
#   +---+---+
#   |   |   |
#   +---+---+
# +---+---+---+
# |   |   |   |
# +---+---+---+
#
# Your task is to write a program which reads the number of blocks the builders have,
# and outputs the height of the pyramid that can be built using these blocks.
#
# Note: the height is measured by the number of fully completed layers - if the
# builders don't have a sufficient number of blocks and cannot complete the next layer,
# they finish their work immediately.
#
blocks        = int(input("Enter the number of blocks: "))
blocks_remain = blocks
height        = 0

while blocks_remain > 0 and blocks_remain - (height + 1) >= 0:
    height        += 1
    blocks_remain -= height

print("The height of the pyramid:", height)

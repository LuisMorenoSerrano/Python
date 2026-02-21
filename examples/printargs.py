#
# Print arguments data
#

import sys

print("SHOW COMMAND ARGUMENTS")
print("======================")
print("Program Name.......:", sys.argv[0])
print("Number of Arguments:", len(sys.argv) - 1)
print("Argument Values....:", str(sys.argv[1:]))

for argn, argv in enumerate(sys.argv[1:]):
    print(" " * 18, str(argn + 1), ": '", argv, "'", sep="")

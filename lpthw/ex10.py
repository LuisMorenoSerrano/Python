# pylint: disable=invalid-name
#
tabby_cat = "\tI'm tabbed in."
persian_cat = "I'm split\non a line."
backslash_cat = "I'm \\ a \\ cat."

fat_cat = """
I'll do a list:
\t* Cat food
\t* Fishies
\t* Catnip\n\t* Grass
"""

print(tabby_cat)
print(persian_cat)
print(backslash_cat)
print(fat_cat)

print("BS example: Radiola\bhola")  # BS example
print("FF example: Radiola\fhola")  # FF example
print("LF example: Radiola\nhola")  # LF example
print("CR example: Radiola\rhola")  # CR example
print("HT example: Radiola\thola")  # TAB example
print("VT example: Radiola\vhola")  # VT example

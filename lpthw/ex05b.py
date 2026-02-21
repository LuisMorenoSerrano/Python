# pylint: disable=invalid-name
#
name = 'Zed A. Shaw'
age = 35 # not a lie
height_in = 74 # inches
height_cm = height_in * 2.54
weight_lb = 180 # lbs
weight_kg = weight_lb * 0.453592
eyes = 'Blue'
teeth = 'White'
hair = 'Brown'

print(f"Let's talk about {name}.")
print(f"He's {height_in} inches ({height_cm:.0f} cm) tall.")
print(f"He's {weight_lb} pounds ({weight_kg:.0f} kg) heavy.")
print("Actually that's not too heavy.")
print(f"He's got {eyes} eyes and {hair} hair.")
print(f"His teeth are usually {teeth} depending on the coffee.")

# this line is tricky, try to get it exactly right
total = age + height_in + weight_lb
print(f"If I add {age}, {height_in}, and {weight_lb} I get {total}.")

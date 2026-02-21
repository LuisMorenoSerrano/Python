#
# Program: waning_moon.py
# Purpose: Indicate if a point with coordinates (x,y) is visible
#          according to the circles that define the waning moon (outer
#          and inner) and the horizon line
# Author: Luis Moreno Serrano
# Date: 23/10/2020 (updated 01/05/2023)
#

# Module imports
from itertools import cycle

import sys
import re
import getchlib
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Rectangle

# Constants declaration (diagram characteristics)
WIDTH  =  6.5  # Width (inches)
HEIGHT = 10.5  # Height (inches)
X_FROM = -2.5  # Lower limit X-axis
Y_FROM = -5.0  # Lower limit Y-axis
X_TO   = 10.0  # Upper limit X-axis
Y_TO   = 15.0  # Upper limit Y-axis

# Constants declaration (circle characteristics)
OCE_X  =  9.0  # Outer Circle Edge: Center (X Coordinate)
OCE_Y  =  6.0  # Outer Circle Edge: Center (Y Coordinate)
OCE_R  =  7.5  # Outer Circle Edge: Radius
ICE_X  = 13.0  # Inner Circle Edge: Center (X Coordinate)
ICE_Y  =  7.3  # Inner Circle Edge: Center (Y Coordinate)
ICE_R  = 10.0  # Inner Circle Edge: Radius

CYCOL  = cycle("bgrcmy")  # List of colors for points

# Draw waning moon
def draw_waning_moon():
    # Build circles
    oce = Circle((OCE_X, OCE_Y), OCE_R, color="whitesmoke", fill=True)
    ice = Circle((ICE_X, ICE_Y), ICE_R, color="black", fill=True)

    # Build translucent area below the horizon line
    ground = Rectangle(
        (X_FROM, Y_FROM), X_TO - X_FROM, 0 - Y_FROM,
        fill=True, color="grey", alpha=0.95)

    # Draw diagram elements
    figure, axes = plt.subplots()

    figure.set_figwidth(WIDTH)
    figure.set_figheight(HEIGHT)

    axes.set_aspect(1)
    axes.set_facecolor("black")

    axes.add_artist(oce)
    axes.add_artist(ice)
    axes.add_artist(ground)

    plt.xlim(X_FROM, X_TO)
    plt.ylim(Y_FROM, Y_TO)
    plt.grid(linestyle="--", zorder=1)

    plt.plot([X_FROM, X_TO], [0.0, 0.0], color="cyan")

    # Check if the figure manager exists before setting the title
    fig_manager = plt.get_current_fig_manager()

    if fig_manager is not None:
        fig_manager.set_window_title("Waning Moon")

    plt.title("Waning Moon")
    plt.ion()
    plt.show()

# Draw point on the image
def draw_point(x, y):
    plt.plot(x, y, "o", color=next(CYCOL), clip_on=False)

    # Check if the figure manager exists before setting the title
    fig_manager = plt.get_current_fig_manager()

    if fig_manager is not None and hasattr(fig_manager, 'canvas'):
        canvas = fig_manager.canvas
        canvas.draw()
        canvas.flush_events()

# Detect point visibility:
#   - NOT inside the inner circle edge
#   - IS inside the outer circle edge
#   - IS above the horizon line
#
# If the distance from the point to the center of the circle is less than or equal
# to its radius, the point is inside the circle (outside otherwise)
#
# For the inner circle, it is assumed that the point is visible if it is on the
# edge itself ("<" condition when detecting membership excludes the edge)
def detect_visibility(x, y):
    in_inner_circle = ((x - ICE_X) ** 2.0 + (y - ICE_Y) ** 2.0)  < (ICE_R ** 2.0)
    in_outer_circle = ((x - OCE_X) ** 2.0 + (y - OCE_Y) ** 2.0) <= (OCE_R ** 2.0)

    return not in_inner_circle and in_outer_circle and y > 0.0

# Request a pair of data separated by a comma (includes error control)
def ask_float_pair(msg):
    while True:
        try:
            val_x, val_y = [float(v) for v in re.split(",[ ]*", input(msg))]
        except ValueError:
            print("Please enter 2 real values separated by a comma!")
        else:
            break

    return val_x, val_y

# Display message to exit if [Esc] is pressed (Chr(27))
# Clear message and position at the beginning of the line after waiting for key press
def ask_exit(msg):
    print("\n" + msg, end="")

    char = getchlib.getkey()

    sys.stdout.write("\x1b[1K")
    print("\r", end="")

    return ord(char) == 27

# Main function
def main():
    draw_waning_moon()

    print(
        "WANING MOON", \
        "===========", \
        "", sep="\n")

    while True:
        x, y       = ask_float_pair("Point coordinates (x, y): ")
        is_visible = detect_visibility(x, y)

        print(f"> Point ({x}, {y}) {'IS' if is_visible else 'IS NOT'} visible")

        draw_point(x, y)

        if ask_exit("[Esc] Exit. Press any key to continue: "):
            break

    return 0

# Define entry point
if __name__ == "__main__":
    sys.exit(main())

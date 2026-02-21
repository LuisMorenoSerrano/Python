import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 20, 1000)   # Create a list of evenly-spaced number over the range
plt.plot(x, np.sin(x))         # Plot the sine of each x point
plt.show()                     # Display the plot

import arcoscubicos as p1
import MoC as p2
import matplotlib.pyplot as plt

plt.figure(7, figsize=(10, 5))
plt.xlim([0,6.5])
plt.ylim([-1.5,1.5])

plt.plot(p1.px, p1.r1, color = 'blue')
plt.plot(p1.px, p1.r2, color = 'blue')
plt.plot(1.6 + p2.xWallPoints, p2.yWallPoints, color = 'blue')
plt.plot(1.6 + p2.xWallPoints, -1 * p2.yWallPoints, color = 'blue')
plt.show()

# import math
from scipy.spatial import Rectangle
# from matplotlib.patches import Rectangle as drawRect
# import matplotlib.pyplot as plt
# import spline
# import detobst
import evoalg
import time

starttime = time.time()
interpol = 100
start = [0, 5]
stop = [10, 5]
points = [[0, 5], [10, 5]]
obst = Rectangle(maxes=[5,8], mins=[4,-300])
obstMov = Rectangle(maxes=[6.5, 1.5], mins=[3.5, -1.5])
obstMov2 = Rectangle(maxes=[9.5, 11.5], mins=[6.5, 8.5])
obst2 = Rectangle(maxes=[2,6], mins=[-300,4])
obsts = [obst, obst2]
movObsts = [[obstMov, 0, 1], [obstMov2, 0, -0.5]]

obsts = []
# movObsts = []

evoalg.start = start
evoalg.stop = stop
evoalg.obsts = obsts
evoalg.movObsts = movObsts
x,y = evoalg.evolutionAlgorithm(obsts.__len__() + movObsts.__len__())
print(time.time()-starttime)
# drawObst = drawRect([4,-300], 1, 308)
# drawObst2 = drawRect([-300,4], 302, 2)
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111, aspect='equal')
# plt.plot(x, y, '-og')
# ax1.add_patch(drawObst)
# ax1.add_patch(drawObst2)
# plt.xlim([0, 10])
# plt.ylim([0, 10])
# plt.show()

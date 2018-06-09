# import math
import math

from scipy import signal
from scipy.spatial import Rectangle
# from matplotlib.patches import Rectangle as drawRect
import matplotlib.pyplot as plt

import PID
import spline
from scipy.spatial import distance
# import detobst
import time
import numpy as np


def vectorToComplex(v):
    return v[0]+1.0j*v[1]

def angle_between(v1, v2):
    v1_u = vectorToComplex(v1)
    v2_u = vectorToComplex(v2)
    return np.angle(v1_u)-np.angle(v2_u)

def getDesiredAngle(pos, pt):
    dx = pt[0]-pos[0]
    dy = pt[1]-pos[1]
    v1 = [dx, dy]
    V1 = vectorToComplex(v1)
    angle = np.angle(V1)
    return angle

m=10
d = 1
w = 1
Iz = 1/12*m*(w**2+d**2)
xg = 0.05
yg = 0.4
start = [5, 0]
points = [[5, 0], [5, 5], [10, 5],[5,0]]
points = spline.spline_pts(points, 10)
Fl = 0
Fr = 0
u = 0.1
Fmax = 1
# Yvk = -5
# Yv = -1
# Yrk = 0.5
# Yr = 0.1
# Nrk = 0.01
# Nr = 0.001
# Nv = 0.01
Yvk = 0
Yv = 0
Yrk = 0
Yr = 0
Nrk = 0
Nr = 0
Nv = 0

A1 = [[m-Yvk, xg*m-Yrk], [xg*m, Iz-Nrk]]
A2 = [[-Yv, m*u-Yr], [-Nv, m*xg*u-Nr]]
A1 = np.array(A1)
A2 = np.array(A2)
# A = -(np.matmul(np.linalg.inv(A1), A2))
# A = np.insert(A, 2, [0,0], axis=1)
# A = np.insert(A, 2, [0,1,0], axis=0)
A = np.array([[0, 0], [1, 0]])
print(A)
# B = np.linalg.inv(A1)
# B = np.insert(B, 2, [0,0], axis=0)
B = np.array([0, Iz])
C = np.array([0, 1])
alfa = math.pi/2
# B[1,1]-=0.3
print(A,B,C)
myPt = [points[0][1], points[1][1]]
t = 0.01
x = 5
y = 0
X = np.array([[0], [alfa]])
thresh = 0.5
i = 1
myPos = [x, y]
zadane = getDesiredAngle(myPos, myPt)
xpos = [x]
ypos = [y]
pid = PID.PID(1, 0.001, 0.01)
pid.SetPoint = zadane
pid.setSampleTime(t)
feedback = alfa
alfas = []
j=0

while i < len(points[0])-1:
    pid.update(feedback)
    output = pid.output
    wejscie = output
    if wejscie > math.pi/2:
        wejscie = math.pi/2
    if wejscie < -math.pi/2:
        wejscie = -math.pi/2

    if wejscie > 0:
        Fl = Fmax-wejscie*Fmax/math.pi
        Fr = Fmax
    if wejscie <= 0:
        Fr = Fmax+wejscie*Fmax/math.pi
        Fl = Fmax
    U = np.array([[0], [yg*(Fr-Fl)]])
    Xp = np.add(np.matmul(A,X), np.matmul(B,U))
    X = X + Xp*t
    alfa = np.matmul(C, X)
    if(alfa>2 or alfa<1.4):
        a =1
    if(abs(zadane-alfa)>1):
        a=2
    x = x+math.cos(alfa)*u*t#+math.sin(alfa)*X[0]*t
    y = y+math.sin(alfa)*u*t#+math.cos(alfa)*X[0]*t
    xpos.append(x)
    ypos.append(y)
    myPos = [x, y]
    if distance.euclidean(myPos, myPt) < thresh:
        i = i+1
        myPt = [points[0][i], points[1][i]]
    zadane = getDesiredAngle(myPos, myPt)
    feedback = alfa
    pid.SetPoint=zadane
    j+=1
    if(j>100):
        print(x, y, alfa[0], zadane, X[0])
        j=0
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
plt.plot(xpos, ypos, '-og')
plt.xlim([0, 10])
plt.ylim([0, 10])
plt.show()

#mozliwy sposob na scinanie zakretow
import numpy as np
import scipy.interpolate as si
import fileHandler
import json
def ptsToLine(pts):
    points = []
    lne = {"line" : []}
    if pts["points"].__len__() > 1:
        for pt in pts["points"]:
            points.append([pt["lng"], pt["lat"]])
        line = spline_pts(points)
        for i in range(line[0].__len__()):
            x = float(line[0][i])
            y = float(line[1][i])
            lnpt = "{\"x\": "+str(x)+", \"y\": "+str(y)+", \"id\": "+str(i)+"}"
            lne["line"].append(json.loads(lnpt))
    fileHandler.saveLineToFile(lne)
    return lne

def spline_pts(points, grain=10):
    r = 0.00003
    ptsNum = len(points)
    pts2 = [ points[0] ]
    for pt in points[1:]:
        pt1 = pts2[-1]
        pt2 = pt
        dx = pt2[0]-pt1[0]
        dy = pt2[1]-pt1[1]
        D = (dx**2+dy**2)**0.5
        try:
            rx = dx/D * r
            ry = dy/D * r
        except:
            rx = 0
            ry = 0
        x1 = pt2[0]-rx
        y1 = pt2[1]-ry
        x2 = pt1[0]+rx
        y2 = pt1[1]+ry
        pts2.append([x2,y2])
        pts2.append([x1,y1])
        pts2.append(pt)


    points = np.array(pts2)
    x = points[:,0]
    y = points[:,1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, ptsNum*grain)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)
    return [x_i, y_i]

#==============================================================================
# Plot
#==============================================================================
#
# points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
# t = range(len(points))
# x = np.array(points)[:,0]
# y = np.array(points)[:,1]
# x_i, y_i = spline_pts(points)
# print(t)
# fig = plt.figure()
# plt.plot(x, y, '-og')
# plt.plot(x_i, y_i, '-or')
# plt.xlim([min(x) - 0.3, max(x) + 0.3])
# plt.ylim([min(y) - 0.3, max(y) + 0.3])
# plt.title('Splined f(x(t), y(t))')
#
# plt.xlim([0.0, max(x_i)])
# plt.title('Basis splines')
# plt.show()
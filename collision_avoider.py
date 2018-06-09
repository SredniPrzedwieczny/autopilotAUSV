import math
import evoalg
import fileHandler
from scipy.spatial import Rectangle
import numpy as np

dMin = 0.5
dX = 0.1
dY = 0.1
dR = 0.1
dE = 0.01

def line():
    lne = fileHandler.loadJsonFromFile('line.json')
    pts = []
    for pt in lne["line"]:
        pts.append([float(pt['x']), float(pt['y'])])
    pts = np.array(pts)
    return pts

def waypoints():
    lne = fileHandler.loadJsonFromFile('points.json')
    pts = []
    for pt in lne["points"]:
        pts.append([float(pt['lng']), float(pt['lat'])])
    pts = np.array(pts)
    return pts

def detectCol():
    stt = fileHandler.loadJsonFromFile('state.json')
    sps = fileHandler.loadJsonFromFile('ships.json')

    mX = float(stt["lng"])
    mY = float(stt["lat"])
    mvX = float(stt["vx"])
    mvY = float(stt["vy"])

    colShips = []

    for ship in sps["ships"]:
        x = float(ship["lon"])
        y = float(ship["lat"])
        hed = float(ship["hed"])*math.pi/180
        V = float(ship["sog"])
        vx = V * math.cos(hed)
        vy = V * math.sin(hed)

        rx = x - mX
        ry = y - mY
        rvx = vx - mvX
        rvy = vy - mvY
        a = rvy/rvx
        b = ry - a*rx
        d = abs(b)/(a**2 + 1)**0.5

        if d==dMin:
            obst = Rectangle(maxes=[x+dX,y+dY], mins=[x-dX,y-dY])
            colShips.append([obst, vx, vy])

    return colShips


def colAvoid(colShips, Wi, i):
    stt = fileHandler.loadJsonFromFile('state.json')
    pts = fileHandler.loadJsonFromFile('points.json')
    W = [pts["points"][Wi]["x"], pts["points"][Wi]["y"]]

    mX = float(stt["lng"])
    mY = float(stt["lat"])

    pt1 = [mX, mY]
    pt2 = W
    dx = pt2[0]-pt1[0]
    dy = pt2[1]-pt1[1]
    D = (dx**2+dy**2)**0.5
    try:
        rx = dx/D * dR
        ry = dy/D * dR
    except:
        rx = 0
        ry = 0
    x1 = pt2[0]-rx
    y1 = pt2[1]-ry
    stop = [x1, y1]

    evoalg.start = pt1
    evoalg.stop = stop
    evoalg.obsts = []
    evoalg.movObsts = colShips
    x,y = evoalg.evolutionAlgorithm(colShips.__len__())
    stop = np.array(stop)
    lne = line()
    lne = lne[i:]
    end = len(lne)-1
    for pt in list(reversed(lne)):
        npt = np.array(pt)
        dist = np.linalg.norm(stop-npt)
        if dist < dE:
            break
        else:
            end -= 1
    if end < i+1:
        end = i+1
    lne = line()
    lne = np.array(lne)
    nlne = np.stack((x, y), axis=-1)
    l1 = lne[0:i+1]
    l2 = lne[end:]
    fline = np.concatenate((l1, nlne, l2), axis=0)
    fileHandler.saveLineToFile(fline)





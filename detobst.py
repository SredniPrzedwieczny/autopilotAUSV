from scipy.spatial import Rectangle
from scipy.spatial import distance

def det_obst(x,y,obsts):
    enter = -1
    exit = -1
    for i in range(x.__len__()):
        pt = [x[i], y[i]]
        for obst in obsts:
            dist = obst.min_distance_point(pt)
            print(dist)
            if dist <= 0.1 and enter == -1:
                enter = i
                break
            if dist > 0.1 and enter != -1 and exit == -1:
                exit = i
                return [enter, exit]

    return [enter, exit]

def det_valid(pts,obsts,movObsts,spd):
    lastPt = pts[0]
    MO = []
    for o, spdX, spdY in movObsts:
        obst = Rectangle(maxes=o.maxes, mins=o.mins)
        MO.append([obst, spdX, spdY])
    for pt in pts:
        for obst in obsts:
            dist = obst.min_distance_point(pt)
            if dist <= 0.2:
                midPT = [(obst.maxes[0]+obst.mins[0])/2, (obst.maxes[1]+obst.mins[1])/2]
                dist = distance.euclidean(midPT, pt)
                return -(dist*4)+999
        time = distance.euclidean(lastPt, pt)/spd
        lastPt = pt
        for obst, spdX, spdY in MO:
            obst.maxes[0] += spdX*time
            obst.mins[0] += spdX*time
            obst.maxes[1] += spdY*time
            obst.mins[1] += spdY*time
            dist = obst.min_distance_point(pt)
            if dist <= 0.5:
                # print(time.__str__())
                midPT = [(obst.maxes[0]+obst.mins[0])/2, (obst.maxes[1]+obst.mins[1])/2]
                dist = distance.euclidean(midPT, pt)
                return -(dist*4)+999
    return 0


def dist_obst(x,y,obsts):
    minDist = 10e15
    for obst in obsts:
        dist = obst.min_distance_point([x,y])
        if dist <= minDist:
            minDist = dist

    return minDist
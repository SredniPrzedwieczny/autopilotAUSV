import dronekit
import math

import time
from pymavlink import mavutil
from scipy.spatial import distance
import numpy as np
import PID
import fileHandler

class mavlink:

    def __init__(self):
        self.vehicle = dronekit.connect('/dev/ttyS0', baud=57600)
        self.pid = PID.PID(1, 0.001, 0.01)
        self.i = 0
        self.Wi = 0
        self.pos = [0, 0]
        self.points = []
        self.waypoints = []
        self.myPt = [0, 0]
        self.myWP = [0, 0]
        self.thresh = 0.05
        self.Wthresh = 0.05


    def getDesiredAngle(self, pos, pt):
        dx = pt[0]-pos[0]
        dy = pt[1]-pos[1]
        v1 = [dx, dy]
        V1 = self.vectorToComplex(v1)
        angle = np.angle(V1)
        return angle

    def vectorToComplex(self, v):
        return v[0]+1.0j*v[1]

    def controlUpdate(self, hdg, lat, lon):
        self.myPos = [lat, lon]
        if distance.euclidean(self.myPos, self.myPt) < self.thresh:
            self.i = self.i+1
            if self.i < self.points[0].__len__():
                self.myPt = [self.points[0][self.i], self.points[1][self.i]]
            else:
                stt = fileHandler.loadJsonFromFile('state.json')
                stt["go"] = str(0)
                self.setServos(1000, 1000)
                return
        if distance.euclidean(self.myPos, self.myWP) < self.Wthresh:
            self.Wi = self.Wi+1
            self.myWP = [self.waypoints[0][self.Wi], self.waypoints[1][self.Wi]]
        zadane = self.getDesiredAngle(self.myPos, self.myPt)
        self.pid.SetPoint = zadane
        self.pid.update(hdg)
        output = self.pid.output
        wejscie = output
        if wejscie > math.pi/2:
            wejscie = math.pi/2
        if wejscie < -math.pi/2:
            wejscie = -math.pi/2

        if wejscie > 0:
            Fl = 2000-wejscie*1000/math.pi
            Fr = 2000
        else:
            Fr = 2000+wejscie*1000/math.pi
            Fl = 2000
        self.setServos(Fl, Fr)


    def setServos(self, LS, RS):
        # Lewy silnik
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,    # target_system, target_component
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
            0, #confirmation
            1,    # servo number
            LS,          # servo position between 1000 and 2000
            0, 0, 0, 0, 0)
        self.vehicle.send_mavlink(msg)
        # Prawy silnik
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,    # target_system, target_component
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
            0, #confirmation
            1,    # servo number
            RS,          # servo position between 1000 and 2000
            0, 0, 0, 0, 0)
        self.vehicle.send_mavlink(msg)

    def arm(self):
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = dronekit.VehicleMode("GUIDED")
        self.vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)


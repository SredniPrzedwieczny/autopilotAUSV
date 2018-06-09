import fileHandler
import server, mavlink, evoalg
from http.server import BaseHTTPRequestHandler, HTTPServer
import ais
import time
import numpy as np
from threading import Thread
import collision_avoider

T = 0.05

class autopilot(Thread):
    def __init__(self):
        super().__init__()

        self.server = server.server()
        self.server.start()
        print("SERVER OK")
        self.aiser = ais.AIS()
        self.aiser.start()
        print("AISER OK")
        mv = mavlink.mavlink()
        self.mavlinker = mv
        self.mavlinker.pid.setSampleTime(T)
        @mv.vehicle.on_message('RANGEFINDER')
        def listener(self, name, message):
            stt = fileHandler.loadJsonFromFile('state.json')
            stt["dph"] = message.distance
            fileHandler.saveStateToFile(stt)

        @mv.vehicle.vehicle.on_message('GLOBAL_POSITION_INT')
        def listener(self, name, message):
            stt = fileHandler.loadJsonFromFile('state.json')
            stt["lng"] = message.lon
            stt["lat"] = message.lat
            stt["heading"] = message.hdg
            stt["vx"] = message.vx
            stt["vy"] = message.vy
            fileHandler.saveStateToFile(stt)

        self.mavlinker.arm()
        print("MAVLINKER OK")
        self.itercnt = 0

    def run(self):
        while True:
            self.itercnt += 1
            stt = fileHandler.loadJsonFromFile('state.json')
            go = int(stt["go"])
            if go == 1:
                if self.mavlinker.myPt == [0, 0]:
                    pts = collision_avoider.line()
                    Wpts = collision_avoider.waypoints()
                    self.mavlinker.points = pts
                    self.mavlinker.waypoints = Wpts
                    self.mavlinker.myPt = [self.mavlinker.points[0][0], self.mavlinker.points[1][0]]
                    self.mavlinker.myWP = [self.mavlinker.points[0][0], self.mavlinker.points[1][0]]
                    self.mavlinker.i = 0
                    self.mavlinker.Wi = 0
                self.mavlinker.controlUpdate(float(stt["hdg"]), float(stt['lat']), float(stt["lng"]))
            else:
                if not self.mavlinker.myPt == [0, 0]:
                    self.mavlinker.myPt = [0, 0]
                    self.mavlinker.myWP = [0, 0]
                    self.mavlinker.points = []
                    self.mavlinker.waypoints = []

            if self.itercnt > 10:
                obst = collision_avoider.detectCol()
                if obst:
                    self.mavlinker.setServos(1000, 1000)
                    collision_avoider.colAvoid(obst, self.mavlinker.Wi, self.mavlinker.i)
            time.sleep(T)




AT = autopilot()
AT.start()
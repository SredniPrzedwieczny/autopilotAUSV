from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
import fileHandler
from spline import ptsToLine
from threading import Thread

class S(BaseHTTPRequestHandler):
    points = []
    line = []
    lne = {"line": []}
    sps = {"ships": []}
    stt = {"dph": 0.1, "lng": 20, "go": 0, "lat": 50, "vx": 0, "vy": 0, "hed": 80}
    pts = {"points": []}

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        self._set_headers()
        if 'points' in path:
            self.pts = fileHandler.loadJsonFromFile('points.json')
            dataToWrite = json.dumps(self.pts).encode('ascii')
        elif 'line' in path:
            self.lne = fileHandler.loadJsonFromFile('line.json')
            dataToWrite = json.dumps(self.lne).encode('ascii')
        elif 'ships' in path:
            self.sps = fileHandler.loadJsonFromFile('ships.json')
            dataToWrite = json.dumps(self.sps).encode('ascii')
        elif 'state' in path:
            self.stt = fileHandler.loadJsonFromFile('state.json')
            dataToWrite = json.dumps(self.stt).encode('ascii')
        else:
            dataToWrite = "{}".encode('ascii')
        self.wfile.write(dataToWrite)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        if 'operator' in path:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            command = json.loads(post_data.decode('utf-8'))
            if command["command"] == "add":
                point = command["data"]
                self.pts["points"].append(point)
            if command["command"] == "delete":
                point = command["data"]
                for el in self.pts["points"]:
                    if el["id"] == int(point):
                        del self.pts["points"][self.pts["points"].index(el)]
            if command["command"] == "update":
                point = json.loads(command["data"])
                for el in self.pts["points"]:
                    if el["id"] == int(point["id"]):
                        self.pts["points"][self.pts["points"].index(el)] = point
            fileHandler.savePtsToFile(self.pts)
            self.lne = ptsToLine(self.pts)
            self._set_headers()
            dataToWrite = json.dumps(self.lne).encode('ascii')
            self.wfile.write(dataToWrite)
        if 'ais' in path:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            command = json.loads(post_data.decode('utf-8'))
            if command["command"] == "add":
                ship = json.loads(command["data"])
                self.sps["ships"].append(ship)
            if command["command"] == "delete":
                ship = command["data"]
                for el in self.sps["ships"]:
                    if el["id"] == int(ship):
                        del self.sps["ships"][self.sps["ships"].index(el)]
            if command["command"] == "update":
                ship = json.loads(command["data"])
                for el in self.sps["ships"]:
                    if el["id"] == int(ship["id"]):
                        self.sps["ships"][self.sps["ships"].index(el)] = ship
            fileHandler.savePtsToFile(self.pts)
            self.lne = ptsToLine(self.pts)
            self._set_headers()
            dataToWrite = json.dumps(self.pts).encode('ascii')
            self.wfile.write(dataToWrite)
        if 'start' in path:
            self.sps = fileHandler.loadJsonFromFile('ships.json')
            self.sps["go"] = 1
            fileHandler.saveStateToFile(self.stt)
            self._set_headers()
            dataToWrite = json.dumps(self.lne).encode('ascii')
            self.wfile.write(dataToWrite)
        if 'stop' in path:
            self.sps = fileHandler.loadJsonFromFile('ships.json')
            self.sps["go"] = 0
            fileHandler.saveStateToFile(self.stt)
            self._set_headers()
            dataToWrite = json.dumps(self.lne).encode('ascii')
            self.wfile.write(dataToWrite)

class server(Thread):
    def __init__(self):
        super().__init__()
        self.server_address = (b'', 1234)
        self.httpd = HTTPServer(self.server_address, S)

    def run(self):
        self.httpd.serve_forever()
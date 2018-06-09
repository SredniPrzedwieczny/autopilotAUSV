import socket
from threading import Thread

import fileHandler

UDP_IP = "0.0.0.0" # = 0.0.0.0 u IPv4
UDP_PORT = 10110

class AIS(Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.data = ""
        self.sps = {"ships" : []}

    def run(self):
        while True:
            character, addr = self.sock.recvfrom(1)
            try:
                character = character.decode('utf-8')
            except:
                pass
            if character == '\n':
                self.data += character
            else:
                sdata = self.data.split(',')
                coded = sdata[5]
                ba = bytearray(coded, 'utf-8')
                binary = ""
                for byte in ba:
                    byte -= 48
                    if byte > 40:
                        byte -= 8
                    toAdd = bin(byte)[2:]
                    binary += toAdd.zfill(6)
                MMSI = binary[8:38]
                MMSI = int(MMSI, 2)
                hed = binary[128:128+9]
                hed = int(hed, 2)
                lat = binary[89:89+27]
                lat = int(lat, 2)/600000
                lon = binary[61:61+28]
                lon = int(lon, 2)/600000
                sog = binary[50:50+10]
                sog = int(lon, 2)/10
                sset = False
                for ship in self.sps["ships"]:
                    if ship["MMSI"] == MMSI:
                        ship["hed"] = hed
                        ship["lon"] = lon
                        ship["lat"] = lat
                        ship["sog"] = sog
                        sset = True
                        break
                if not sset:
                    ship = {"MMSI": MMSI, "hed": hed, "lon": lon, "lat": lat, "sog": sog}
                    self.sps["ships"].append(ship)
                # sptime[MMSI] = datetime.datetime.now()
                fileHandler.saveShipsToFile(self.sps)
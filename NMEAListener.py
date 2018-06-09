import json
import serial
import datetime
serial_name = "COM4"
baud_rate = 9600
shiptimeout = 15
stt = {"lng": 50, "lat": 50, "dph": 0, "spd": 0, "hed": 90, "rud":0}
sps = {"ships" : []}
sptime = {}

def saveStateToFile():
    lneFile = open("state.json", 'w')
    lneFile.truncate()
    lneFile.write(json.dumps(stt))
    lneFile.close()

def saveShipsToFile():
    spsFile = open("ships.json", 'w')
    spsFile.truncate()
    spsFile.write(json.dumps(sps))
    spsFile.close()

def getShipTimeout():
    todel = []
    for ship in sptime:
        timestamp = sptime[ship]
        now = datetime.datetime.now()
        delta = now-timestamp
        if delta.seconds > shiptimeout*60:
            for el in sps["ships"]:
                if el["MMSI"] == ship:
                    del sps["ships"][sps["ships"].index(el)]
            todel.append(ship)
            saveShipsToFile()
    for ship in todel:
        del sptime[ship]

ser = serial.Serial(serial_name, baud_rate, timeout=60)
while True:
    getShipTimeout()
    read_data = ser.readline().decode('utf-8')
    data = read_data.split(',')
    if data[0] == '$HCHDG':
        stt["hed"] = float(data[1])
        saveStateToFile()
    if data[0] == '$SDDBT':
        stt["dph"] = float(data[1])
        saveStateToFile()
    if data[0] == '!AIVDM':
        coded = data[5]
        ba = bytearray(coded, 'utf-8')
        binary = ""
        for byte in ba:
            byte -= 48
            if byte > 40:
                byte -= 8
            toAdd = bin(byte)[2:]
            binary = binary + toAdd.zfill(6)
        MMSI = binary[8:38]
        MMSI = int(MMSI, 2)
        hed = binary[128:128+9]
        hed = int(hed, 2)
        lat = binary[89:89+27]
        lat = int(lat, 2)/600000
        lon = binary[61:61+28]
        lon = int(lon, 2)/600000
        sset = False
        for ship in sps["ships"]:
            if ship["MMSI"] == MMSI:
                ship["hed"] = hed
                ship["lon"] = lon
                ship["lat"] = lat
                sset = True
                break
        if not sset:
            ship = {"MMSI": MMSI, "hed": hed, "lon": lon, "lat": lat}
            sps["ships"].append(ship)
        sptime[MMSI] = datetime.datetime.now()
        saveShipsToFile()

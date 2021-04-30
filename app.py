import firebase_admin
from firebase_admin import firestore, credentials
from time import sleep
import board
from devices import RGBLed, Lightbulb, security_system
from devices import SecuritySystem, WaterLeakSensor
securitySystem = SecuritySystem(state_pin=27,
                                buzzer_pin=24)


SENSORS = {
    # "4BCIpzBWpgLA24mMI7r2":object, # Door Sensor
    "MxRCd6ERRSWzYzyNTE8S": WaterLeakSensor(23),
    # "WbKjbbYIyPmsm5MDO4FE":object, #temperature sensor
    # "k5kHgwoSnXcWESFvPq4B": object, #ambient sensor
}

for sensor_id in SENSORS:
    SENSORS[sensor_id].attach(securitySystem)


DEVICES = {
    "H28mo4GHlyaorwBsOyNu": RGBLed(board.D18, 30),
    "iz277eqT5Mwhgv7XLfyF": Lightbulb(17),
    # "iThlJRyeBSgeslxJwGDz": Lightbulb(27),
    "3rL3QL7Kq2HrQjs53Y7o": securitySystem
}

DEVICE_DATA = {}


def on_device_data(collection_snapshot, changes, read_time):
    print("Snapshot called")
    # print(collection_snapshot)
    for doc in collection_snapshot:

        DEVICE_DATA[doc.id] = doc.to_dict()
        # print(doc.to_dict())
        # print()
        if doc.id in DEVICES:
            print(doc.to_dict()['states'])
            DEVICES[doc.id].set_state(doc.to_dict()['states'], doc.reference)


cred = credentials.Certificate('./serviceAccountCreds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_watch = db.collection('devices').on_snapshot(on_device_data)
while True:
    sleep(1000)

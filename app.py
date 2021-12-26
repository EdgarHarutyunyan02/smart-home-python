import firebase_admin
from firebase_admin import firestore, credentials
from time import sleep
import board
from devices import RGBLed, Lightbulb, Led, Outlet, security_system
from devices import SecuritySystem, WaterLeakSensor,  BME280, TemperatureSensor, AmbientSensor, DoorSensor
from utils.PubSub import PubSub
from utils.MailService import MailService

# This object is for managing intercummunication using Publish/Subscribe model
pub_sub_manager = PubSub()

# Registering Mail service, to notify user about events
mail_service = MailService()

pub_sub_manager.subscribe("SEND_MESSAGE", mail_service.send_message)

securitySystem = SecuritySystem(
    state_pin=27, buzzer_pin=24, event_manager=pub_sub_manager)

bme280 = BME280(event_manager=pub_sub_manager)
bme280.start_monitoring()

SENSORS = {
    # "4BCIpzBWpgLA24mMI7r2":object, # Door Sensor
    "MxRCd6ERRSWzYzyNTE8S": WaterLeakSensor(23),
    # temperature sensor
    "WbKjbbYIyPmsm5MDO4FE": TemperatureSensor(event_manager=pub_sub_manager),
    # ambient sensor
    "k5kHgwoSnXcWESFvPq4B": AmbientSensor(event_manager=pub_sub_manager),
    "4BCIpzBWpgLA24mMI7r2": DoorSensor(16),
}

for sensor_id in SENSORS:
    SENSORS[sensor_id].attach(securitySystem)


DEVICES = {
    "H28mo4GHlyaorwBsOyNu": RGBLed(board.D18, 30),
    "iz277eqT5Mwhgv7XLfyF": Lightbulb(17),
    "iThlJRyeBSgeslxJwGDz": Led(6),
    "9tVH0v423ZD5tZW4l2m6": Led(26),
    "VVvt3h2PPwysDFUZDAE5": Outlet(5),  # Relay
    "3rL3QL7Kq2HrQjs53Y7o": securitySystem
}

DEVICE_DATA = {}


def on_device_data(collection_snapshot, changes, read_time):
    print("Snapshot called")
    for doc in collection_snapshot:
        DEVICE_DATA[doc.id] = doc.to_dict()
        if doc.id in DEVICES:
            print("Device State", doc.to_dict()['states'])
            DEVICES[doc.id].set_state(doc.to_dict()['states'], doc.reference)

        if doc.id in SENSORS:
            print("Sensor State", doc.to_dict()['states'])
            SENSORS[doc.id].set_doc(doc.reference)


cred = credentials.Certificate('./serviceAccountCreds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_watch = db.collection('devices').on_snapshot(on_device_data)
while True:
    sleep(1000)

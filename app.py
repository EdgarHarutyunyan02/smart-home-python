import firebase_admin
from firebase_admin import firestore, credentials
from time import sleep
import board
from devices import RGBLed, Lightbulb

DEVICES = {
    "H28mo4GHlyaorwBsOyNu": RGBLed(board.D18, 30),
    "iz277eqT5Mwhgv7XLfyF": Lightbulb(17),
    "iThlJRyeBSgeslxJwGDz": Lightbulb(27)
}

DEVICE_DATA = {}

def on_device_data(collection_snapshot, changes, read_time):
    print("Snapshot called")
    # print(collection_snapshot)
    for doc in collection_snapshot:
        DEVICE_DATA[doc.id] = doc.to_dict()
        print(doc.to_dict())
        # print()
        if doc.id in DEVICES:
            print(doc.to_dict())
            DEVICES[doc.id].set_state(doc.to_dict()['states'])


cred = credentials.Certificate('./serviceAccountCreds.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_watch = db.collection('devices').on_snapshot(on_device_data)
sleep(1000)

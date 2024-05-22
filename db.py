import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate(r"fsbd_private_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

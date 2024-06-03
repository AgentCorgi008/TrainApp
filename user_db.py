from db import db
import os
import json

CONFIG_FILE_USER = "user_id.json"


class User:
    def __init__(self, name, sec_name, sex, age, height, weight):
        self.name = name
        self.sec_name = sec_name
        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight


class UserDB:
    user_default_data = {
        'name': "Daniel",
        'sec_name': "Yeromenko",
        'sex': "male",
        'age': 23,
        'height': 166,
        'weight': 72
    }

    def get_exist_user(self):
        # Check if user ID file exists
        if os.path.exists(CONFIG_FILE_USER):
            with open(CONFIG_FILE_USER, 'r') as file:
                user_id = json.load(file).get('user_id', False)
                if user_id:
                    # Check if the user document exists in the database
                    print(user_id)
                    doc_ref = db.collection("users").document(user_id)
                    print(doc_ref.id)
                    if doc_ref.get().exists:
                        return doc_ref
        return False

    def _create_user(self, data):
        doc_ref = db.collection("users").document()
        doc_ref.set(data)
        print(doc_ref.id)
        # Save the new user ID to the file
        with open(CONFIG_FILE_USER, 'w') as file:
            json.dump({'user_id': doc_ref.id}, file)
        print(doc_ref.id)
        return doc_ref

    def get_user_data(self, user_id):
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print("No such document!")
            return None

    def create_custom_user(self, data):
        self._create_user(data)

    def create_default_user(self):
        self._create_user(self.user_default_data)

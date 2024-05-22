from db import db


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

    def check_user_exist(self):
        db_coll = db.collection("users")
        return db_coll.get()

    def create_default_user(self):
        doc_ref = db.collection("users").document()
        doc_ref.set(self.user_default_data)

    def create_custom_user(self):
        pass

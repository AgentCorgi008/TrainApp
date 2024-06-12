from db.init import db
import os
import json

CONFIG_FILE_USER = "configs/user_id.json"


class UserDB:
    def __init__(self):
        self.user_id = self.__get_user_id()
        self.user_ref = None
        self.db = db

    def __get_user_id(self):
        # Check if user ID file exists
        if os.path.exists(CONFIG_FILE_USER):
            with open(CONFIG_FILE_USER, 'r') as file:
                user_id = json.load(file).get('user_id', False)
                if user_id:
                    doc_ref = db.collection("users").document(user_id)
                    if doc_ref.get().exists:
                        return user_id
                return user_id

    def get_exist_user(self):
        if self.user_id:
            # Check if the user document exists in the database
            doc_ref = db.collection("users").document(self.user_id)
            if doc_ref.get().exists:
                return doc_ref
        return False

    def _create_user(self, data):
        doc_ref = db.collection("users").document()
        doc_ref.set(data)
        self.user_id = doc_ref.id
        print(doc_ref.id)
        # Save the new user ID to the file
        with open(CONFIG_FILE_USER, 'w') as file:
            json.dump({'user_id': doc_ref.id}, file)
        print(doc_ref.id)
        return doc_ref

    def get_user_data(self):
        doc_ref = db.collection("users").document(self.user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print("No such document!")
            return None

    def create_custom_user(self, data):
        self._create_user(data)

    def get_workout_calendar(self, day):
        user_ref = self.get_exist_user()
        return user_ref.collection('workout_calendar').document(day).get()

    def get_workout_programs(self):
        user_ref = self.get_exist_user()
        return user_ref.collection('workout_programs').get()

    def get_exercise_info(self, group_id, exercise_id):
        exercise_group_ref = self.db.collection('exercises').document(group_id)
        exercise_data = exercise_group_ref.collection('exercises').document(exercise_id).get().to_dict()
        return exercise_data

    def create_workout_program(self, program_data):
        user_ref = self.get_exist_user()
        program_ref = user_ref.collection('workout_programs').document()
        program_ref.set(program_data)
        return program_ref

    def update_workout_calendar(self, day, program_refs):
        user_ref = self.get_exist_user()
        calendar_ref = user_ref.collection('workout_calendar').document(day)
        calendar_ref.set({'programs': program_refs})

    def save_completed_workout(self, program_name, completed_exercises, date):
        user_ref = self.get_exist_user()
        workout_done_ref = user_ref.collection('workout_done_dates').document()
        workout_done_ref.set({
            'program_name': program_name,
            'exercises': completed_exercises,
            'date': date
        })

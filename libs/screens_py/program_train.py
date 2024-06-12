from datetime import datetime

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, TwoLineRightIconListItem, IconRightWidget, MDList

from libs.other.info_more import MUSCLE_GROUP_NAME

Builder.load_file('libs/screens_kivy/program_train.kv')


class WorkoutProgramsScreen(Screen):
    def on_pre_enter(self):
        self.load_workout_programs()
        self.load_completed_workouts()

    def load_workout_programs(self, *args):
        self.ids.programs_list.clear_widgets()
        user_db = MDApp.get_running_app().user_db
        workout_programs = user_db.get_workout_programs()
        for program in workout_programs:
            program_data = program.to_dict()
            item = OneLineListItem(
                text=program_data['name'],
                on_release= lambda x, program=program_data: self.show_program_descr(program)
            )
            self.ids.programs_list.add_widget(item)

    def load_completed_workouts(self):
        app = MDApp.get_running_app()
        db = app.user_db.db
        today_date = app.nav_exrcs_manager.date_obj.strftime("%d-%m-%Y")
        completed_workouts = db.collection('users').document(app.user_db.user_id).collection(
            'workout_done_dates').where('date', '==', today_date).stream()
        if completed_workouts:
            if "completed_workouts_list" in self.ids:
                self.ids.completed_workouts_list.clear_widgets()
            else:
                scroll_view = ScrollView()
                completed_workouts_list = MDList(id="completed_workouts_list")
                scroll_view.add_widget(completed_workouts_list)
                self.ids.box_programs_workouts.add_widget(MDSeparator())
                self.ids.box_programs_workouts.add_widget(scroll_view)
                self.ids.completed_workouts_list = completed_workouts_list

            for workout in completed_workouts:
                workout_data = workout.to_dict()
                item = OneLineListItem(text=workout_data['program_name'])
                self.ids.completed_workouts_list.add_widget(item)

    def show_completed_workout(self, workout_data):
        completed_workout_screen = self.manager.get_screen('completed_workout')
        completed_workout_screen.set_workout_data(workout_data)
        self.manager.push('completed_workout', 'Виконане тренування')

    def show_program_descr(self, program_data):
        print(program_data['name'])
        app = MDApp.get_running_app()
        descr_screen = app.nav_exrcs_manager.get_screen('workout_program_train')
        descr_screen.set_program_data(program_data)
        app.nav_exrcs_manager.push('workout_program_train', program_data['name'])


class CompletedWorkoutScreen(Screen):
    workout_data = None

    def set_workout_data(self, workout_data):
        self.workout_data = workout_data
        self.load_exercises()

    def load_exercises(self):
        self.ids.exercises_list.clear_widgets()
        exercises = self.workout_data.get('exercises', {})
        for group_id, exercise_ids in exercises.items():
            for exercise_id, sets in exercise_ids.items():
                exercise_info = MDApp.get_running_app().user_db.get_exercise_info(group_id, exercise_id)
                exercise_item = TwoLineRightIconListItem(
                    text=exercise_info[1].get('name'),
                    secondary_text=f"Рівень складності - {exercise_info[1].get('difficulty')}"
                )
                exercise_item.group_id = group_id
                exercise_item.exercise_id = exercise_id
                exercise_item.completed_sets = sets
                icon = IconRightWidget(icon="information-outline")
                icon.on_release = lambda x=exercise_info[1]: self.show_exercise_description(x)
                exercise_item.add_widget(icon)
                self.ids.exercises_list.add_widget(exercise_item)

    def show_exercise_description(self, exercise_data):
        description_screen = self.manager.get_screen('exercise_description')
        description_screen.show(exercise_data)
        self.manager.push('exercise_description', 'Опис вправи')


class WorkoutProgramTrainScreen(Screen):
    program_data = None
    exercise_data = None

    def set_program_data(self, program_data):
        self.load_exercises(program_data)
        self.program_data = program_data

    def load_exercises(self, program_data):
        self.ids.exercise_list.clear_widgets()
        user_db = MDApp.get_running_app().user_db
        exercises = program_data.get('exercises', {})
        for group_id, exercise_ids in exercises.items():
            for exercise_id in exercise_ids:
                exercise_data = user_db.get_exercise_info(group_id, exercise_id)
                exercise_item = TwoLineRightIconListItem(
                    text=exercise_data.get('name'),
                    secondary_text=f"Рівень складності - {exercise_data.get('difficulty')}"
                )
                exercise_item.completed = False
                exercise_item.group_id = group_id
                exercise_item.exercise_id = exercise_id
                icon = IconRightWidget(icon="information-outline")
                exercise_data['muscle_group_name'] = MUSCLE_GROUP_NAME[group_id]
                self.exercise_data = exercise_data
                icon.on_release = lambda x=exercise_data: self.show_exercise_description(x)
                exercise_item.add_widget(icon)
                self.ids.exercise_list.add_widget(exercise_item)

    def load_train_exercise_show(self):
        for item in self.ids.exercise_list.children:
            item.bind(on_release=lambda x=item: self.start_exercise(x))

    def start_workout(self):
        self.dialog.dismiss()
        self.load_train_exercise_show()
        self.ids.start_workout_btn.parent.remove_widget(self.ids.start_workout_btn)
        new_button = MDRaisedButton(
            text="Зберегти тренування",
            pos_hint={"center_x": 0.5},
            on_release=self.complete_workout
        )
        # Додаємо нову кнопку на місце старої
        self.ids.start_workout_btn = new_button
        self.ids.workout_box.add_widget(new_button)

    def start_exercise(self, item):
        self.manager.get_screen('workout_exercise').set_exercise_data(item, self.exercise_data)
        self.manager.push('workout_exercise', 'Виконання вправи')

    def confirm_start_workout(self, *args):
        self.dialog = MDDialog(
            text="Ви дійсно хочете почати тренування?",
            buttons=[
                MDRaisedButton(text="Скасувати", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Почати", on_release=lambda x: self.start_workout())
            ],
        )
        self.dialog.open()

    def complete_workout(self, *args):
        completed_exercises = [item for item in self.ids.exercise_list.children if item.completed]
        if not completed_exercises:
            self.show_error("Має бути виконана хоча б одна вправа.")
            return
        # Додайте логіку збереження завершеного тренування
        self.save_workout_training()
        self.show_success("Тренування успішно завершено!")

    def save_workout_training(self):
        completed_exercises = {}
        for item in self.ids.exercise_list.children:
            if item.completed:
                group_id = item.group_id
                exercise_id = item.exercise_id
                sets = item.sets
                if group_id not in completed_exercises:
                    completed_exercises[group_id] = {}
                completed_exercises[group_id][exercise_id] = sets

        date = datetime.now().strftime("%d-%m-%Y")
        user_db = MDApp.get_running_app().user_db
        user_db.save_completed_workout(self.program_data['name'], completed_exercises, date)

        # Видаляємо стару кнопку
        self.ids.start_workout_btn.parent.remove_widget(self.ids.start_workout_btn)

        # Створюємо нову кнопку з функцією збереження тренування
        new_button = MDRaisedButton(
            text="Почати тренування",
            pos_hint={"center_x": 0.5},
            on_release=self.confirm_start_workout
        )

        # Додаємо нову кнопку на місце старої
        self.ids.start_workout_btn = new_button
        self.ids.workout_box.add_widget(new_button)

        self.show_success("Тренування успішно завершено!")
        self.manager.pop()

    def show_error(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def show_success(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def show_exercise_description(self, exercise_data):
        description_screen = self.manager.get_screen('exercise_description')
        return description_screen.show(exercise_data)


class WorkoutProgramExerciseScreen(Screen):
    exercise_data = ObjectProperty(None)
    exercise_name = StringProperty("")
    data_dict = None

    def on_enter(self, *args):
        # Очистити список перед додаванням нових віджетів
        self.ids.set_list.clear_widgets()

        # Додати 4 віджети WorkoutSetWidget
        for i in range(4):
            set_widget = WorkoutSetWidget()
            set_widget.ids.set_num.text = str(i + 1) + "."
            self.ids.set_list.add_widget(set_widget)

        self.ids.set_list.add_widget(MDRaisedButton(
            text="Інформація про вправу",
            on_release=lambda x: self.show_exercise_description(self.data_dict))
        )

    def set_exercise_data(self, item, exercise_data_dict):
        self.exercise_data = item
        self.exercise_name = item.text
        self.data_dict = exercise_data_dict
        self.ids.exercise_name.text = item.text

    def mark_as_completed(self):
        app = MDApp.get_running_app()
        primary_color = app.theme_cls.primary_color
        self.exercise_data.bg_color = (primary_color[0], primary_color[1], primary_color[2], 0.1)
        self.exercise_data.completed = True
        self.save_exercise_data()
        self.manager.pop()  # Повертаємося до екрану опису програми

    def save_exercise_data(self):
        set_data = {}
        for num, widget in enumerate(self.ids.set_list.children):
            if isinstance(widget, WorkoutSetWidget):
                reps = widget.ids.reps.text
                weight = widget.ids.weight.text
                set_data[str(num)] = {"reps": int(reps), "weight": int(weight)}
        self.exercise_data.sets = set_data
        print(self.exercise_data.sets)

    def show_exercise_description(self, exercise_data):
        description_screen = self.manager.get_screen('exercise_description')
        return description_screen.show(exercise_data)


class WorkoutSetWidget(BoxLayout):
    pass

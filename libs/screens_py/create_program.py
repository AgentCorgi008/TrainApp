from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import MDList, TwoLineRightIconListItem, IconRightWidget


Builder.load_file('libs/screens_kivy/create_program.kv')


class CreateProgramScreen(Screen):
    selected_exercises = {}
    data_loaded = False

    group_muscles_images = (
        'abs.png', 'arms.png',
        'back.png', 'chest.png',
        'legs.png', 'shoulders.png'
    )

    def on_pre_enter(self):
        if not self.data_loaded:
            Clock.schedule_once(self.load_muscle_groups, 0.1)
            self.data_loaded = True

    def load_muscle_groups(self, *args):
        self.ids.muscle_groups_list.clear_widgets()
        app = MDApp.get_running_app()
        path_to_source = "source/images/"
        if app.theme_cls.theme_style == "Dark":
            path_to_source += "dark/"
        else:
            path_to_source += "light/"
        db = app.user_db.db
        muscle_groups = db.collection('exercises').stream()
        for img_num, group in enumerate(muscle_groups):
            group_data = group.to_dict()
            group_item = MDExpansionPanel(
                icon=f'{path_to_source}{self.group_muscles_images[img_num]}',
                content=MDList(),
                panel_cls=MDExpansionPanelOneLine(text=group_data['name'])
            )
            group_item.bind(
                on_open=lambda panel=group_item,
                group_id=group.id:
                self.load_exercises_for_group(panel, group_id)
            )
            self.ids.muscle_groups_list.add_widget(group_item)

    def load_exercises_for_group(self, panel, group_id):
        if not panel.content.children:
            db = MDApp.get_running_app().user_db.db
            exercises_group = db.collection('exercises').document(group_id).get()
            exercises_group_name = exercises_group.to_dict()['name']
            exercises = db.collection('exercises').document(group_id).collection('exercises').stream()
            for exercise in exercises:
                exercise_data = exercise.to_dict()
                exercise_item = TwoLineRightIconListItem(
                    text=exercise_data['name'],
                    secondary_text=f"Рівень складності - {exercise_data['difficulty']}"
                )
                exercise_item.selected = False  # Додаємо прапор вибору
                exercise_item.group_id = group_id  # Додаємо групу м'язів як атрибут елемента
                exercise_item.exercise_id = exercise.id  # Додаємо id вправи як атрибут елемента
                exercise_item.bind(on_release=lambda item=exercise_item, ex_item=exercise_item: self.toggle_selection(ex_item))
                icon = IconRightWidget(icon="information-outline")
                exercise_data['muscle_group_name'] = exercises_group_name
                icon.on_release = lambda x=exercise_data: self.show_exercise_description(exercise_data)
                exercise_item.add_widget(icon)
                panel.content.add_widget(exercise_item)

    def toggle_selection(self, exercise_item):
        app = MDApp.get_running_app()
        group_id = exercise_item.group_id
        exercise_id = exercise_item.exercise_id
        if exercise_item.selected:
            exercise_item.bg_color = app.theme_cls.bg_normal
            self.exercise_item_add_to_selected(group_id, exercise_id)
        else:
            primary_color = app.theme_cls.primary_color
            exercise_item.bg_color = (primary_color[0], primary_color[1], primary_color[2], 0.1)
            self.exercise_item_remove_from_selected(group_id, exercise_id)
        exercise_item.selected = not exercise_item.selected
        print(self.selected_exercises)

    def exercise_item_add_to_selected(self, group_id, exercise_id):
        if group_id in self.selected_exercises:
            if exercise_id in self.selected_exercises[group_id]:
                self.selected_exercises[group_id].remove(exercise_id)
                if not self.selected_exercises[group_id]:
                    del self.selected_exercises[group_id]

    def exercise_item_remove_from_selected(self, group_id, exercise_id):
        if group_id not in self.selected_exercises:
            self.selected_exercises[group_id] = []
        self.selected_exercises[group_id].append(exercise_id)

    def show_exercise_description(self, exercise_data):
        description_screen = self.manager.get_screen('exercise_description')
        return description_screen.show(exercise_data)

    def save_program(self):
        program_name = self.ids.program_name.text
        if not program_name:
            self.show_alert_dialog("Будь ласка, введіть назву програми тренувань.")
            return

        app = MDApp.get_running_app()
        user_db = app.user_db

        day_of_week = str(self.manager.date_obj.weekday())

        # Створюємо програму тренувань
        program_data = {
            'name': program_name,
            'exercises': self.selected_exercises, # Зберігаємо обрані вправи з поділом на групи м'язів
            'day_of_week': day_of_week  # Додаємо день тижня, коли виконується програма
        }

        # Зберігаємо програму в колекцію програм тренувань
        program_ref = user_db.create_workout_program(program_data)

        # Оновлюємо календар тренувань
        workout_calendar = user_db.get_workout_calendar(day_of_week)
        if workout_calendar.exists:
            program_refs = workout_calendar.to_dict().get('programs', [])
        else:
            program_refs = []
        program_refs.append(program_ref)
        user_db.update_workout_calendar(day_of_week, program_refs)

        self.selected_exercises.clear()

        app.nav_exrcs_manager.set_to_default_top_bar()

        # Перемикаємося назад на головний екран тренувань
        self.manager.current = 'main_exercise'

    def show_alert_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

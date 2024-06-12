from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

Builder.load_file('libs/screens_kivy/exercise_descr.kv')


class ExerciseDescrScreen(Screen):

    def show(self, exercise_data):

        self.ids.exercise_name.text = exercise_data.get('name', 'Невідомо')

        # Оновлення групи м'язів
        self.ids.muscle_group.text = f"Група м'язів: {exercise_data.get('muscle_group_name')}"

        muscle_category = exercise_data.get('muscles', {})

        self.ids.muscles_info.clear_widgets()

        app = MDApp.get_running_app()

        # Оновлення основних м'язів
        primary_muscles = [muscle_category.get('main', [])]
        if primary_muscles:
            for muscle in primary_muscles:
                chip = MDRaisedButton(text=muscle,
                                      md_bg_color=app.theme_cls.primary_color)  # Зелений колір для основних м'язів
                self.ids.muscles_info.add_widget(chip)

        # Оновлення другорядних м'язів
        additional_muscles = muscle_category.get('additional', [])
        if additional_muscles:
            for muscle in additional_muscles:
                chip = MDRaisedButton(text=muscle, md_bg_color=[30 / 255, 144 / 255,
                                                                255 / 255])  # Синій колір для другорядних м'язів
                self.ids.muscles_info.add_widget(chip)

        # Оновлення опису вправи
        self.ids.exercise_description.text = exercise_data.get('description', 'Опис відсутній')
        self.ids.exercise_description.height = self.ids.exercise_description.texture_size[1]

        # Оновлення рівня складності
        difficulty_level = exercise_data.get('difficulty', 0)
        for i in range(1, 4):
            star_id = f'star_{i}'
            icon_name = 'star' if i <= difficulty_level else 'star-outline'
            self.ids[star_id].icon = icon_name

        self.manager.push("exercise_description", "Вправа")

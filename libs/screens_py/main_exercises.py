from datetime import datetime, timedelta

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('libs/screens_kivy/main_exercises.kv')


class ExercisesScreen(Screen):
    pass


class MainExerciseScreen(Screen):
    current_date = StringProperty("")

    def on_enter(self, *args):
        Clock.schedule_once(self._init_date, 0.1)

    def _init_date(self, *args):
        self.manager.date_obj = datetime.now()
        self.update_date()

    def update_date(self):
        self.current_date = self.manager.date_obj.strftime("%a, %d %b")

    def next_day(self):
        self.manager.date_obj += timedelta(days=1)
        self.update_date()

    def prev_day(self):
        self.manager.date_obj -= timedelta(days=1)
        self.update_date()

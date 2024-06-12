from kivy.uix.screenmanager import ScreenManager, FadeTransition, NoTransition
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem


class NavigationScreenManager(ScreenManager):
    screen_stack = []
    top_bar_name_stack = ["Головна"]
    last_pop = None

    def push(self, screen_name, name):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.top_bar_name_stack.append(name)
            self.current = screen_name
            manager = MDApp.get_running_app().manager
            manager.ids.main_menu.bar_name = name
            app_bar = manager.get_top_app_bar()
            back_button = [["arrow-left", lambda x: self.pop()]]
            self.last_pop = back_button
            app_bar.left_action_items = back_button
            print(self.top_bar_name_stack)

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack.pop()
            self.current = screen_name
            top_bar_name = self.top_bar_name_stack.pop()
            main_menu = MDApp.get_running_app().manager.ids.main_menu
            main_menu.bar_name = top_bar_name
            if not self.screen_stack:
                self.top_bar_name_stack = ["Головна"]
                main_menu.bar_name = "Головна"
                app_bar = MDApp.get_running_app().manager.get_top_app_bar()
                app_bar.left_action_items = []
            else:
                next_top_bar_name = self.top_bar_name_stack[-1]
                main_menu.bar_name = next_top_bar_name

            print(self.top_bar_name_stack)

    def set_to_default_top_bar(self):
        self.screen_stack = []
        self.top_bar_name_stack = ["Головна"]
        self.last_pop = []
        app = MDApp.get_running_app()
        main_menu = app.manager.ids.main_menu
        main_menu.bar_name = "Головна"
        app.manager.get_top_app_bar().left_action_items = []


class NavigationExerciseManager(NavigationScreenManager):
    date_obj = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app = MDApp.get_running_app()
        app.nav_exrcs_manager = self
        if app.theme_cls.theme_style == "Dark":
            self.transition = FadeTransition(duration=0.1)
        else:
            self.transition = NoTransition()

    def start_workout(self):
        day_of_week = str(self.date_obj.weekday())
        user_db = MDApp.get_running_app().user_db
        workout_calendar = user_db.get_workout_calendar(day_of_week)
        if workout_calendar.exists:
            program_refs = workout_calendar.to_dict().get('programs', [])
            if program_refs:
                self.show_workout_programs(program_refs)
                return
        self.push("program_not_found", "Програми тренувань")

    def show_workout_programs(self, program_refs):
        self.push('workout_programs', "Програми тренувань")

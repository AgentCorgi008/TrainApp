from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition, NoTransition
from kivymd.app import MDApp

Builder.load_file('libs/screens_kivy/main_navigation.kv')


class MainAppPage(Screen):
    bar_name = StringProperty("Головна")
    top_bar_main_last_pop = None

    def change_tab_screen(self, widget, name):
        self.change_main_screen_app_bar(name)
        manager = self.get_main_exercise_manager()
        screen_stack = manager.screen_stack
        if not (name == "main_exercise" and screen_stack):
            self.bar_name = widget.text
        self.ids.main_nav_bar_manager.current = name

    def get_main_exercise_manager(self):
        return self.ids.main_nav_bar_manager.get_screen("main_exercise").ids.exerc_manager

    def change_main_screen_app_bar(self, screen):
        top_bar = self.ids.top_bar
        manager = self.get_main_exercise_manager()
        screen_stack = manager.screen_stack
        if screen == "main_exercise" and not screen_stack:
            top_bar.left_action_items = []
        elif screen == "main_exercise" and screen_stack:
            top_bar.left_action_items = manager.last_pop
        else:
            top_bar.left_action_items = [["arrow-left", lambda x: self.to_main_screen()]]

    def to_main_screen(self):
        manager = self.get_main_exercise_manager()
        screen_stack = manager.screen_stack
        self.ids.bottom_nav.switch_tab('main_tab')
        if not screen_stack:
            self.bar_name = "Головна"
            self.ids.top_bar.left_action_items = []
        else:
            self.bar_name = manager.top_bar_name_stack[-1]
            self.ids.top_bar.left_action_items = manager.last_pop
        self.ids.main_nav_bar_manager.current = "main_exercise"


class MainAppNavigationBarManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app = MDApp.get_running_app()
        app.nav_bottom_bar_manager = self
        if MDApp.get_running_app().theme_cls.theme_style == "Dark":
            self.transition = FadeTransition(duration=0.1)
        else:
            self.transition = NoTransition()

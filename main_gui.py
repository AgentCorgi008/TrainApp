import os

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRoundFlatIconButton
import re
import json

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

Builder.load_file("main.kv")
Window.size = (500, 600)
CONFIG_FILE = "theme_config.json"


class ScreenNewUser(Screen):
    pass


class MainToolBars(Screen):
    pass


class MainMenu(ScreenManager):
    pass


class MDTextFieldLetters(MDTextField):
    pat = re.compile('[^a-zA-Zа-яА-ЯіІїЇєЄґҐ]')

    def insert_filter(self, substring, from_undo=False):
        if len(self.text) >= self.max_text_length:
            return
        s = re.sub(self.pat, '', substring)
        return s


class CustomUser(Screen):
    pass


class PhysicalUserData(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = None
        self.age = None
        self.user_height = None
        self.user_weight = None

    def validate_fields(self):
        return self.age and self.user_height and self.user_weight

    def update_name(self, widget):
        self.age = widget.text

    def update_sec_name(self, widget):
        self.user_height = widget.text

    def update_gender(self, widget):
        self.user_weight = widget.text

    def open_menu(self, widget, rng):
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_widget_value(widget, x),
            } for i in range(*rng)]
        self.menu = MDDropdownMenu(
            caller=widget,
            items=menu_items,
            position="bottom",
        )
        self.menu.open()

    def set_widget_value(self, widget, value):
        widget.text = value
        self.menu.dismiss()

    def process_data(self):
        if self.validate_fields():
            app = MDApp.get_running_app()
            app.user_data.update({
                'age': self.age,
                'height': self.user_height,
                'weight': self.user_weight
            })
            app.manager.transition = FadeTransition()
            app.manager.current = "main_app_menu"
            print(app.user_data)
        else:
            print("pass")


class GeneralUserData(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender = None
        self.first_name = None
        self.sec_name = None

    def validate_fields(self):
        return self.first_name and self.sec_name and self.gender

    def update_name(self, widget):
        self.first_name = widget.text

    def update_sec_name(self, widget):
        self.sec_name = widget.text

    def update_gender(self, gender):
        self.gender = gender

    def process_data(self):
        if self.validate_fields():
            app = MDApp.get_running_app()
            app.user_data = {
                'name': self.first_name,
                'sec_name': self.sec_name,
                'gender': self.gender
            }
            self.manager.next_page()
        else:
            pass


class SexUserToggleButton(MDRoundFlatIconButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color


class NewUserScreenManager(ScreenManager):

    def next_page(self):
        self.current = "physic_data"
        self.transition = SlideTransition(direction="left")


class NavigationScreenManager(ScreenManager):
    screen_stack = []

    def push(self, screen_name):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.transition.direction = "left"
            self.current = screen_name

    def pop(self):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = "right"
            self.current = screen_name


class TrainApp(MDApp):
    manager = ObjectProperty(None)

    def build(self) -> ObjectProperty:
        self.load_theme()
        self.manager = NavigationScreenManager()
        return self.manager

    def switch_theme(self) -> None:
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Green"
        self.save_theme()

    def save_theme(self) -> None:
        theme_settings = {
            "theme_style": self.theme_cls.theme_style,
            "primary_palette": self.theme_cls.primary_palette,
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(theme_settings, f)

    def load_theme(self) -> None:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                theme_settings = json.load(f)
                self.theme_cls.theme_style = theme_settings.get("theme_style", "Light")
                self.theme_cls.primary_palette = theme_settings.get("primary_palette", "Green")
        else:
            # Set default theme settings if config file does not exist
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Green"

    def on_start(self):
        return

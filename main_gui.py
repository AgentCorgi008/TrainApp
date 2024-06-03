from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition, NoTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRoundFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from user_db import UserDB, CONFIG_FILE_USER
from info_more import IMT_INFO, BRM_INFO
import re
import os
import json

Builder.load_file("main.kv")
Window.size = (500, 600)
CONFIG_FILE = "theme_config.json"


class ScreenNewUser(Screen):
    pass


class MainExerciseScreen(Screen):
    pass


class InfoScreen(Screen):
    def on_pre_enter(self, *args):
        with open(CONFIG_FILE_USER, 'r') as file:
            user_config = json.load(file)
        user_id = user_config.get('user_id')
        if user_id:
            app = MDApp.get_running_app()
            user_data = app.user_db.get_user_data(user_id)
            if user_data:
                self.calculate_imt(user_data)
                self.calculate_brm(user_data)

    def calculate_imt(self, user_data):
        weight = user_data.get('weight', 0)
        height_cm = user_data.get('height', 0)
        height_m = height_cm / 100
        imt = weight / (height_m ** 2)
        self.ids.imt_value.text = f"{imt:.1f}"
        self.update_imt_category(imt)

    def update_imt_category(self, imt):
        if imt < 18.5:
            category = "Недостатня вага"
            color = (1, 1, 0, 1)  # Yellow
        elif 18.5 <= imt < 25:
            category = "Норма"
            color = (0, 1, 0, 1)  # Green
        elif 25 <= imt < 30:
            category = "Надмірна вага"
            color = (1, 0.65, 0, 1)  # Orange
        elif 30 <= imt < 34.9:
            category = "Ожиріння I ступеню"
            color = (1, 0, 0, 1)  # Red
        elif 35 <= imt < 39.9:
            category = "Ожиріння II ступеню"
            color = (1, 0, 0.5, 1)  # Dark Red
        else:
            category = "Ожиріння III ступеню"
            color = (0.5, 0, 0, 1)  # Darker Red
        self.ids.imt_category.text = category
        self.ids.imt_value.color = color
        self.ids.imt_category.color = color

    def calculate_brm(self, user_data):
        weight = user_data.get('weight')
        height_cm = user_data.get('height')
        age = user_data.get('age')
        sex = user_data.get('gender')

        if sex == 'Чоловік':
            brm = 88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age)
        else:
            brm = 447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age)

        self.ids.brm_value.text = f"{brm:.0f} ккал"

    def show_imt_info(self):
        self.dialog = MDDialog(
            title="БРМ",
            text=IMT_INFO,
            buttons=[
                MDRaisedButton(
                    text="ЗАКРИТИ",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()

    def show_brm_info(self):
        self.dialog = MDDialog(
            title="БРМ",
            text=BRM_INFO,
            buttons=[
                MDRaisedButton(
                    text="ЗАКРИТИ",
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()


class IMTBarWidget(BoxLayout):
    imt_value = NumericProperty(26.1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(imt_value=self.update_thumb_position, size=self.update_thumb_position)

    def update_thumb_position(self, *args):
        bar_width = self.ids.imt_bar.width
        thumb_x = bar_width * (self.imt_value - 16) / (40 - 16)
        self.ids.thumb_label.center_x = self.x + thumb_x


class MainAppPage(Screen):
    bar_name = StringProperty("Головна")

    def change_tab_screen(self, widget, name):
        self.change_main_screen_app_bar(name)
        self.bar_name = widget.text
        self.ids.main_nav_bar_manager.current = name

    def change_main_screen_app_bar(self, screen):
        top_bar = self.ids.top_bar
        if screen == "main":
            top_bar.left_action_items = []
        else:
            top_bar.left_action_items = [["arrow-left", lambda x: self.to_main_screen()]]

    def to_main_screen(self):
        self.ids.bottom_nav.switch_tab('main_tab')
        self.bar_name = "Головна"
        self.change_main_screen_app_bar("main")
        self.ids.main_nav_bar_manager.current = "main"


class MainAppNavigationBarManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transition = NoTransition()


class ProfileScreen(Screen):
    name_field = StringProperty()
    sec_name_field = StringProperty()
    sex_field = StringProperty()
    age_field = StringProperty()
    height_field = StringProperty()
    weight_field = StringProperty()

    def on_pre_enter(self):
        with open(CONFIG_FILE_USER, 'r') as file:
            user_config = json.load(file)
        user_id = user_config.get('user_id')
        if user_id:
            app = MDApp.get_running_app()
            user_data = app.user_db.get_user_data(user_id)
            if user_data:
                self.name_field = user_data.get('name', '')
                self.sec_name_field = user_data.get('sec_name', '')
                self.sex_field = user_data.get('gender', '')
                self.age_field = str(user_data.get('age', ''))
                self.height_field = str(user_data.get('height', ''))
                self.weight_field = str(user_data.get('weight', ''))


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
                'age': int(self.age),
                'height': int(self.user_height),
                'weight': int(self.user_weight)
            })
            app.manager.transition = FadeTransition()
            app.manager.current = "main_app_menu"
            app.user_db.create_custom_user(app.user_data)
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_db = UserDB()

    def build(self) -> ObjectProperty:
        self.load_theme()
        self.manager = NavigationScreenManager()
        user_doc = self.user_db.get_exist_user()
        if user_doc:
            self.manager.current = "main_app_menu"
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
        pass

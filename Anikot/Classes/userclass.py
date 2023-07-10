import copy
import ctypes

from Classes.loginclass import LoginScreen
from Classes.premade import original_buttons, get_anime_logger
from Classes.homeclass import HomeScreen

from Classes.animelogger import AnimeLogger
from Classes.animerunner import AnimeRunner

from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.slider import Slider


class UserScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get("wm")
        kwargs.pop("wm")

        super(UserScreen, self).__init__(**kwargs)

        original_buttons(self)


    def widgets(self):
        self.clear_widgets()
        original_buttons(self)

        al = get_anime_logger(self)

        if al is not None:

            user = al.user['data']['User']
            name = user['name']
            avatar = user['avatar']['large']

            avatarImage = AsyncImage(source=avatar, size_hint=(0.25, 0.25), pos_hint={"x": 0, "top": 1})
            nameLabel = Label(text=name, size_hint=(0.25, 0.1), pos_hint={"x": 0.25, "top": 1}, halign='center', font_size=40, color=(1, 1, 1, 1), outline_width= 1, outline_color= (0, 0, 0, 1))

            self.add_widget(avatarImage)
            self.add_widget(nameLabel)
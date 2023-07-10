import copy
import ctypes

from Classes.premade import original_buttons

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


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get('wm')
        kwargs.pop('wm')
        super(HomeScreen, self).__init__(**kwargs)



        VerticalSlider = Slider(min=0, max=100, value=0, size_hint=(0.1, 0.95), pos_hint={"x": 0.93, "top": 1.025},
               orientation='vertical')
        VerticalSlider.bind(value=self.new_value)
        original_buttons(self)
        self.add_widget(VerticalSlider)

    def new_value(self, instance, value):
        print(value)

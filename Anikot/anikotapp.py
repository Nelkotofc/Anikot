import copy
import ctypes
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.slider import Slider

from Classes.loginclass import LoginScreen
from Classes.premade import original_buttons
from Classes.homeclass import HomeScreen
from Classes.userclass import UserScreen
from Classes.medialistclass import MediaListScreen
from Classes.settingsclass import SettingsScreen
from Classes.animeclass import AnimeScreen

from Classes.animelogger import AnimeLogger
from Classes.animerunner import AnimeRunner




# LOGIN, USER, HOME, MEDIA LISTS, SETTINGS

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

        self.animerunner = None
        self.preusername = None

        Window.size = (Window.size[1]*2, Window.size[1])
        self.last_size = copy.copy(Window.size)

        self.settings_screen = SettingsScreen(name='settings', wm=self)
        self.anime_screen = AnimeScreen(name='anime', wm=self)
        self.login_screen = LoginScreen(name='login', wm=self)
        self.home_screen = HomeScreen(name='home', wm=self)
        self.media_list_screen = MediaListScreen(name='media_list', wm=self)
        self.user_screen = UserScreen(name='user', wm=self)

        self.add_widget(self.anime_screen)
        self.add_widget(self.login_screen)
        self.add_widget(self.home_screen)
        self.add_widget(self.media_list_screen)
        self.add_widget(self.settings_screen)
        self.add_widget(self.user_screen)

        Window.bind(size=self.new_window_size)

        if self.preusername is not None:
            self.login_screen.login(self.preusername)
            self.login(self.preusername)

    def new_window_size(self, *args):

        if Window.size[0] == self.last_size[0]:
            Window.size = (Window.size[1]*2, Window.size[1])
        else:
            Window.size = (Window.size[0], Window.size[0]/2)

        self.last_size = copy.copy(Window.size)


    def login(self, username):

        self.animerunner = AnimeRunner(
            pseudo=username,
            logs_file_path='Texts/logs.txt',
            export_file=True,
            export_file_path="Texts/anime.txt",
            export_category_file=True,
            export_category_file_path="Texts/categories.txt",

        )

        self.user_screen.widgets()
        self.media_list_screen.load_animes({})
        self.media_list_screen.widgets()

        self.switch_to('media_list', 'right')

    def switch_to(self, name, direction=None, class_widgets=None):
        self.current = name

        if direction is not None:
            self.transition = SlideTransition(direction=direction)

        if class_widgets is not None:
            try:
                class_widgets.widgets()
            except:
                pass

class Anikot(App):
    def build(self):
        return WindowManager()

    def on_start(self):
        self.title = 'Anikot'
        self.root.current = 'home'
        self.icon = 'Images/logo.jpg'

if __name__ == '__main__':
    Anikot().run()
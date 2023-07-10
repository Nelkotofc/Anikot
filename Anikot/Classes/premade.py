import copy
import ctypes

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

def get_anime_logger(self):
    try:
        return self.wm.animerunner.anime_logger
    except:
        return None

def get_settings(self):
    return self.wm.settings_screen

def get_title(self, anime):
    return get_settings(self).get_title_text(anime["media"]["titles"])

def get_anime(anime_id, screen_class):
    return screen_class.wm.animerunner.anime_logger.anime_list.get(anime_id)

def original_buttons(self, settings_window=False):
    size_hint = (1 / 5, 0.1)

    def switch_to_login(instance):
        self.wm.switch_to('login', direction='right', class_widgets=self.wm.login_screen)

    def switch_to_user(instance):
        if self.wm.current == 'login':
            self.wm.transition = SlideTransition(direction='left')
        else:
            self.wm.transition = SlideTransition(direction='right')

        self.wm.switch_to('user', class_widgets=self.wm.user_screen)

    def switch_to_home(instance):


        if self.wm.current in ['login', 'user']:
            self.wm.transition = SlideTransition(direction='left')
        else:
            self.wm.transition = SlideTransition(direction='right')

        self.wm.switch_to('home', class_widgets=self.wm.home_screen)

    def switch_to_media_list(instance):

        if self.wm.current == 'settings':
            self.wm.transition = SlideTransition(direction='right')
        else:
            self.wm.transition = SlideTransition(direction='left')

        self.wm.switch_to('media_list', class_widgets=self.wm.media_list_screen)


    def switch_to_settings(instance):
        self.wm.switch_to('settings', direction="left", class_widgets=self.wm.settings_screen)

    new_size_hint = (size_hint[0], size_hint[1])

    translation = get_settings(self).translate if not settings_window else self.translate

    login_name = translation("Login")
    user_name = translation("User")
    home_name = translation("Home")
    media_name = translation("Media")
    settings_name = translation("Settings")

    login_button_color = (0, 0, 0, 1) if self.wm.current != 'login' else (1, 1, 1, 1)
    user_button_color = (0, 0, 0, 1) if self.wm.current!= 'user' else (1, 1, 1, 1)
    home_button_color = (0, 0, 0, 1) if self.wm.current!= 'home' else (1, 1, 1, 1)
    media_button_color = (0, 0, 0, 1) if self.wm.current!='media_list' else (1, 1, 1, 1)
    settings_button_color = (0, 0, 0, 1) if self.wm.current!='settings' else (1, 1, 1, 1)

    background_button = Button(size_hint= (1.01, size_hint[1]+0.01), pos_hint={"x": -0.01, "top": 0.1}, background_color = (0, 0, 0, 1))

    login_button = Button(text=login_name, size_hint= new_size_hint , pos_hint={"x": size_hint[0] * 0, "top": 0.1}, background_color=login_button_color)  # LEFT
    user_button = Button(text=user_name, size_hint= new_size_hint , pos_hint={"x": size_hint[0] * 1, "top": 0.1}, background_color=user_button_color)  # MIDDLE LEFT
    home_button = Button(text=home_name, size_hint= new_size_hint , pos_hint={"x": size_hint[0] * 2, "top": 0.1}, background_color=home_button_color)  # MIDDLE
    media_button = Button(text=media_name, size_hint= new_size_hint ,
                          pos_hint={"x": size_hint[0] * 3, "top": 0.1}, background_color=media_button_color)  # MIDDLE RIGHT
    settings_button = Button(text=settings_name, size_hint= new_size_hint ,
                             pos_hint={"x": size_hint[0] * 4, "top": 0.1}, background_color=settings_button_color)  # RIGHT


    login_button.bind(on_press=switch_to_login)
    user_button.bind(on_press=switch_to_user)
    home_button.bind(on_press=switch_to_home)
    settings_button.bind(on_press=switch_to_settings)
    media_button.bind(on_press=switch_to_media_list)

    self.add_widget(background_button)
    self.add_widget(login_button)
    self.add_widget(user_button)
    self.add_widget(home_button)
    self.add_widget(media_button)
    self.add_widget(settings_button)

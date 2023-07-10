import copy
import ctypes

from Classes.loginclass import LoginScreen
from Classes.premade import original_buttons, get_anime, get_settings
from Classes.homeclass import HomeScreen
from Classes.userclass import UserScreen
from Classes.medialistclass import MediaListScreen
from Classes.settingsclass import SettingsScreen

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

class AnimeScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get('wm')
        kwargs.pop('wm')

        super(AnimeScreen, self).__init__(**kwargs)

        self.anime = None
        self.animes = {}
        self.widgets()

    def reload(self):
        self.anime_changed(self.anime)

    def anime_changed(self, animeid):
        image_quality = get_settings(self).image_quality
        if animeid in self.animes:
            datas = self.animes[animeid]["datas"]
            if self.animes[animeid]["imageQuality"] != image_quality:
                self.animes[animeid]["animeImage"].source = datas['media']["extra"]['coverImage'][image_quality]
        else:
            datas = get_anime(animeid, self)
            # SOURCES

            titles = datas["media"]["titles"]
            title_text = get_settings(self).get_title_text(titles)
            title_size = (0.75, 0.1)
            title_pos = {"x": 0.5, "top": 1}

            image_source = datas['media']["extra"]['coverImage'][image_quality]
            image_size = [1 / 7 - 0.01 * 7, 1 / 4 - 0.01 * 4]
            image_pos = {"x": 0, "top": 1}


            # ADJUST
            image_size[0] *= 4
            image_size[1] *= 4

            # WIDGETS
            titleLabel = Label(text=title_text, size_hint=title_size, pos_hint=title_pos)
            animeImage = AsyncImage(source=image_source, size_hint=image_size, pos_hint=image_pos, allow_stretch=True, keep_ratio=False)

            self.animes[animeid] = {"datas": datas, "titleLabel": titleLabel, "animeImage": animeImage, "imageQuality": image_quality}
        self.anime = animeid

        self.widgets()

    def widgets(self):
        self.clear_widgets()
        original_buttons(self)
        if self.anime is not None:
            self.add_widget(self.animes[self.anime]["animeImage"])
            self.add_widget(self.animes[self.anime]["titleLabel"])




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

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get('wm')
        kwargs.pop('wm')

        super(SettingsScreen, self).__init__(**kwargs)

        self.image_quality = "large"
        self.title_text = "english"
        self.language = "english"
        self.display = "grid"
        self.anime_sort = "Trending"
        self.adult = False # if False (create new media list for it) else put in original media list
        self.text_size = 15

        self.available_display = ["list", "grid"]
        self.available_image_qualities = ["large", "medium", "extraLarge"]
        self.available_title_texts = ["english", "romaji"]
        self.available_languages = ["english", "french"]
        self.available_anime_sorts = ["Trending", "Popularity", "AverageScore", "UserScore", "Favorites", "StartDate", "EndDate", "MeanScore", "Aired", "AiredEpisodes", "Duration", "IsFavourite", "NextAiring", "Status", "AiredEpisodesLeft", "TotalEpisodes", "Category", "TotalEpisodesLeft", "Country"]

        self.translations = {
            "french": {
                "list": "liste",
                "grid": "grille",
                "large": "large",
                "medium": "medium",
                "extraLarge": "extraLarge",
                "english": "anglais",
                "romaji": "romaji",
                "french": "français",

                "trending": "tendance",
                "popularity": "popularité",
                "averagescore": "score moyen (1)",
                "userscore": "score de l'utilisateur",
                "favorites": "favoris",
                "startdate": "date de début",
                "enddate": "date de fin",
                "meanscore": "score moyen (2)",
                "aired": "diffusé",
                "airedepisodes": "épisodes diffusés",
                "duration": "durée",
                "isfavourite": "est préféré",
                "nextairing": "prochaine diffusion",
                "status": "statut",
                "airedepisodesleft": "épisodes diffusés restants",
                "totalepisodes": "nombre total d'épisodes",
                "category": "catégorie",
                "totalepisodesleft": "total d'épisodes restants",
                "country": "pays",

                "home": "accueil",
                "login": "connexion",
                "user": "profil",
                "media": "lists",
                "settings": "paramètres",
                "all": "tous",
                "inside": "lists",
                "watching": "regarder",
                "completed": "terminé",
                "paused": "attente",
                "dropped": "arrêter",
                "planning": "planifier",
                "relations": "relations",
                "true": "vrai",
                "false": "faux",

                "image quality": "qualité d'image",
                "title text": "text de titre",
                "language": "langue",
                "display": "affichage",
                "anime sort": "ordre d'affichage",
                "adult": "adulte"
            }
        }

        self.image_quality_button = None
        self.title_text_button = None
        self.language_button = None
        self.display_button = None
        self.anime_sort_button = None
        self.anime_18_plus_button = None

        self.widgets()

    def ImageQualityButtonPressed(self, instance):
        index = self.available_image_qualities.index(self.image_quality)
        index += 1
        if index >= len(self.available_image_qualities):
            index = 0

        self.image_quality = self.available_image_qualities[index]
        self.reload()
        self.widgets()
    def AdultButtonPressed(self, instance):
        self.adult = not self.adult
        self.reload()
    def TitleTextButtonPressed(self, instance):
        index = self.available_title_texts.index(self.title_text)
        index += 1
        if index >= len(self.available_title_texts):
            index = 0

        self.title_text = self.available_title_texts[index]
        self.reload()
    def LanguageButtonPressed(self, instance):
        index = self.available_languages.index(self.language)
        index += 1
        if index >= len(self.available_languages):
            index = 0

        self.language = self.available_languages[index]
        self.reload()
    def DisplayButtonPressed(self, instance):
        index = self.available_display.index(self.display)
        index += 1
        if index >= len(self.available_display):
            index = 0

        self.display = self.available_display[index]
        self.reload()
    def AnimeSortButtonPressed(self, instance):
        index = self.available_anime_sorts.index(self.anime_sort)
        index += 1
        if index >= len(self.available_anime_sorts):
            index = 0

        self.anime_sort = self.available_anime_sorts[index]
        self.wm.media_list_screen.widgets()
        self.reload()
    def load_buttons(self, *args):

        image_quality_prefix = self.translate("Image Quality").capitalize()
        title_text_prefix = self.translate("Title Text").capitalize()
        language_prefix = self.translate("Language").capitalize()
        display_prefix = self.translate("Display").capitalize()
        anime_sort_prefix = self.translate("Anime Sort").capitalize()
        adult_prefix = self.translate("Adult").capitalize()

        image_quality_name = self.translate(self.image_quality).capitalize()
        title_text_name = self.translate(self.title_text).capitalize()
        language_name = self.translate(self.language).capitalize()
        display_name = self.translate(self.display).capitalize()
        anime_sort_name = self.translate(self.anime_sort)
        adult_name = str(self.translate(self.adult)).capitalize()

        image_quality_text = f"{image_quality_prefix}: {image_quality_name}"
        title_text_text = f"{title_text_prefix}: {title_text_name}"
        language_text = f"{language_prefix}: {language_name}"
        display_text = f"{display_prefix}: {display_name}"
        anime_sort_text = f"{anime_sort_prefix}: {anime_sort_name}"
        adult_text = f"{adult_prefix}: {adult_name}"


        self.image_quality_button = Button(text=image_quality_text, size_hint=(0.25, 0.25),
                                           pos_hint={"x": 0, "top": 1}, background_color=(1, 1, 1, 1), font_size=self.text_size)
        self.title_text_button = Button(text=title_text_text, size_hint=(0.25, 0.25), pos_hint={"x": 0.25, "top": 1},
                                        background_color=(1, 1, 1, 1), font_size=self.text_size)
        self.language_button = Button(text=language_text, size_hint=(0.25, 0.25), pos_hint={"x": 0.5, "top": 1},
                                      background_color=(1, 1, 1, 1), font_size=self.text_size)
        self.display_button = Button(text=display_text, size_hint=(0.25, 0.25), pos_hint={"x": 0.75, "top": 1},
                                     background_color=(1, 1, 1, 1), font_size=self.text_size)
        self.anime_sort_button = Button(text=anime_sort_text, size_hint=(0.25, 0.25), pos_hint={"x": 0, "top": 0.75},
                                        background_color=(1, 1, 1, 1), font_size=self.text_size)
        self.adult_button = Button(text=adult_text, size_hint=(0.25, 0.25), pos_hint={"x": 0.25, "top": 0.75},
                                           background_color=(1, 1, 1, 1), font_size=self.text_size)

        self.image_quality_button.bind(on_press=self.ImageQualityButtonPressed)
        self.title_text_button.bind(on_press=self.TitleTextButtonPressed)
        self.language_button.bind(on_press=self.LanguageButtonPressed)
        self.display_button.bind(on_press=self.DisplayButtonPressed)
        self.anime_sort_button.bind(on_press=self.AnimeSortButtonPressed)
        self.adult_button.bind(on_press=self.AdultButtonPressed)

        self.add_widget(self.image_quality_button)
        self.add_widget(self.title_text_button)
        self.add_widget(self.language_button)
        self.add_widget(self.display_button)
        self.add_widget(self.anime_sort_button)
        self.add_widget(self.adult_button)

    def translate_back(self, text):

        if self.language == "english":
            return text

        for key in list(self.translations.get(self.language).keys()):
            result = self.translations.get(self.language).get(key).lower()
            if result == text.lower():
                return key.capitalize()

        print(f"Return None : {text}")
        return None

    def translate(self, text):
        if self.language == "english":
            return text
        else:
            tt = self.translations.get(self.language).get(str(text).lower())
            if tt is None:
                return text
            else:
                return tt.capitalize()


    def get_title_text(self, titles):

        if self.title_text == "english" and titles.get("english") is not None:
            return titles.get("english")

        return titles.get("romaji")

    def reload(self):
        #self.wm.home_screen.widgets()

        self.wm.media_list_screen.load_animes()

        self.wm.login_screen.widgets()
        self.wm.user_screen.widgets()
        self.wm.media_list_screen.widgets()

        self.widgets()

    def widgets(self, *args):
        self.clear_widgets()
        original_buttons(self, settings_window=True)
        self.load_buttons()

        """
        # Easy Code
        # X Image Quality (Button Change When Pressed, Button Text is Image Quality)
        # X Title Text (Button Change When Pressed, Button Text is Title Text, if Text is null than Romaji)

        # Medium Code
        # X Language
        # +18 Option
        # Anime Display (Button Change When Pressed, Button Text is Anime Display)
            - Aired Episodes
            - Total Episodes
            - Watched Episodes
            - Next Airing
            - Category (if All or Inside)
            - Country
        

        # Difficult Code
        # Notifications
        """


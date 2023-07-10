import copy
import ctypes

from Classes.premade import original_buttons, get_anime, get_title, get_anime_logger, get_settings

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
class MediaListScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get("wm")
        kwargs.pop("wm")
        super(MediaListScreen, self).__init__(**kwargs)

        self.animes = []
        self.coverImages = {}
        self.verticalSlider = None

        self.added_categories = ["All", "Inside", "Relations"]
        self.categories = copy.copy(self.added_categories)
        self.selected_category = "All"

        self.last_kwargs = None

        self.load_slider()
        self.widgets()




    def load_slider(self):

        anime_per_row = 19.4 if self.wm.settings_screen.display == "grid" else 1.5

        max_value = round(len(self.animes) / anime_per_row / 2.5)

        self.verticalSlider = Slider(min=0, max=max_value, value=max_value, size_hint=(0.1, 0.84), pos_hint={"x": 0.93, "top": 0.92},
               orientation='vertical')
        self.verticalSlider.bind(value=self.widgets)

    def load_animes(self, kwargs=None):
        self.animes = []

        if kwargs is None:
            kwargs = self.last_kwargs

            if kwargs is None:
                kwargs = {}
        else:
            self.last_kwargs = kwargs

        if self.wm is not None and self.wm.animerunner is not None:

            self.animes = self.wm.animerunner.filtering(
                export_filters="Texts/filters.txt",  # None : No exportation, "path" : exportation to the file
                export_reasons="Texts/reasons.txt",  # None : No exportation, "path" : exportation to the file

                whitelists=kwargs.get("whitelists"),
                # Watching/Completed/Paused/Dropped/Planning/None(Relations) : as a list of strings (except for "None" which is boolean)
                blacklists=kwargs.get("blacklists"),  # same as whitelists
                aired=kwargs.get("aired"),  # False : (NOT_YET_RELEASED), True: (episode_aired > 0)
                status=kwargs.get("status"),  # FINISHED/NOT_YET_RELEASED/RELEASING : as a list of strings
                format=["TV", "TV_SHORT", "MOVIE", "SPECIAL", "OVA", "ONA"],

                whitelist_any_genres=kwargs.get("whitelist_any_genres"),  # False/None (Anime needs every genres), True (Anime needs at least one genre)
                whitelist_genres=kwargs.get("whitelist_genres"),  # as a list of strings
                blacklist_genres=kwargs.get("blacklist_genres"),  # as a list of strings

                whitelist_countries=kwargs.get("whitelist_countries"),  # JP (Japon), CN (China), KR (South Korean) : Countries as a list of strings
                blacklist_countries=kwargs.get("blacklist_countries"),  # same as blacklist_countries
                adult=get_settings(self).adult,

                reverse=kwargs.get("reverse"),  # True : reversed | False/None : not reversed
                sort=get_settings(self).anime_sort,  # Popularity/Trending/AverageScore/UserScore/Favorites/
                # StartDate/EndDate/MeanScore/Aired/AiredEpisodes/Duration/IsFavourite/
                # NextAiring/Status/AiredEpisodesLeft/TotalEpisodes/Category/TotalEpisodesLeft/Country
            )

        self.load_slider()

    def load_categories(self):
        x = 0
        top = 1

        gal = get_anime_logger(self)

        keys = list(gal.category_list.keys()) if gal is not None else []

        self.categories = self.added_categories + keys

        width = 1/len(self.categories)
        height = 0.1

        for category in self.categories:

            background_color = (0, 0, 0, 1)

            if category == self.selected_category:
                background_color = (1, 1, 1, 1)


            CategoryButton = Button(text=self.wm.settings_screen.translate(category), size_hint=(width, height), pos_hint={"x": x, "top": top}, background_color=background_color)
            CategoryButton.bind(on_press=self.CategoryPressed)
            self.add_widget(CategoryButton)
            x += width

    def CategoryPressed(self, instance):


        self.selected_category =self.wm.settings_screen.translate_back(instance.text)

        print("CategoryPressed : ", self.selected_category)

        if get_anime_logger(self) is not None:

            kwargs = {}

            cats = get_anime_logger(self).category_list

            if self.selected_category not in cats:
                match self.selected_category:
                    case "Relations":
                        kwargs["whitelists"] = [None]
                    case "Inside":
                        kwargs["blacklists"] = [None]
                    case "All":
                        kwargs["whitelists"] = None
                        kwargs["blacklists"] = None

            else:
                for category in list(cats.keys()):
                    if category == self.selected_category:
                        kwargs["whitelists"] = [category]

            self.load_animes(kwargs)
        self.widgets()

    def AnimePressed(self, instance):
        print(f"AnimePressed : {instance.text}")
        self.wm.anime_screen.anime_changed(int(instance.text))
        self.wm.transition = SlideTransition(direction='down')
        self.wm.current = 'anime'


    def widgets(self, *args):
        self.clear_widgets()

        x = 0
        top = self.verticalSlider.max - self.verticalSlider.value-(len(self.animes)/500)
        size_hint = (1/7 - 0.01*7, 1/4 - 0.01*4)

        index = 0

        if top < 1:
            top = 1

        top -= 0.1

        if self.wm is None or self.wm.animerunner is None or self.wm.settings_screen.display == "grid":

            while index < len(self.animes) and index >= 0:
                anime = self.animes[index]
                coverImageSource = anime['media']["extra"]['coverImage'][self.wm.settings_screen.image_quality]

                if self.coverImages.get(coverImageSource) is None:
                    coverImage = AsyncImage(source=coverImageSource, size_hint=size_hint, pos_hint={"x": x, "top": top}, allow_stretch=True, keep_ratio=False)
                    self.coverImages[coverImageSource] = coverImage

                if top >= 0:
                    coverImage = self.coverImages[coverImageSource]
                    coverImage.pos_hint = {"x": x, "top": top}

                    AnimeButton = Button(pos_hint={"x": x, "top": top}, size_hint=size_hint, opacity=0,
                                         text=str(anime["media"]["extra"]["id"]))

                    AnimeButton.bind(on_press=self.AnimePressed)

                    self.add_widget(AnimeButton)

                    self.add_widget(coverImage)


                x += size_hint[0] + 0.01

                if x >= 1-size_hint[0]:
                    x = 0
                    top -= size_hint[1] + 0.01

                index += 1

        elif self.wm.settings_screen.display == "list":
            while index < len(self.animes) and index >= 0:
                anime = self.animes[index]
                coverImageSource = anime['media']["extra"]['coverImage'][self.wm.settings_screen.image_quality]

                if self.coverImages.get(coverImageSource) is None:
                    coverImage = AsyncImage(source=coverImageSource, size_hint=size_hint, pos_hint={"x": x, "top": top}, allow_stretch=True, keep_ratio=False)
                    self.coverImages[coverImageSource] = coverImage

                if top >= 0:
                    coverImage = self.coverImages[coverImageSource]
                    coverImage.pos_hint = {"x": x, "top": top}

                    title = get_title(self, anime)
                    titleLabel = Label(text=title, size_hint=(1, 0.1), pos_hint={"x": x + size_hint[0], "top": top},font_size=30)
                    AnimeButton = Button(pos_hint={"x": 0, "top": top}, size_hint=(1, size_hint[1]), opacity=0, text=str(anime["media"]["extra"]["id"]))

                    AnimeButton.bind(on_press=self.AnimePressed)

                    self.add_widget(AnimeButton)
                    self.add_widget(coverImage)
                    self.add_widget(titleLabel)



                top -= size_hint[1] + 0.01
                index += 1

        self.load_categories()
        original_buttons(self)
        self.add_widget(self.verticalSlider)

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

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        self.wm = kwargs.get('wm')
        kwargs.pop('wm')
        super(LoginScreen, self).__init__(**kwargs)


        self.accounts = []
        Window.bind(on_key_down=self._on_keyboard_down)

        self.widgets()
        self.accounts_informations = {}
        self.image_buttons = {}

    def widgets(self):
        self.clear_widgets()
        original_buttons(self)
        self.login_input = TextInput(multiline=False, size_hint=(0.6, 0.1), pos_hint={"x": 0.2, "top": 0.2},
                                     font_size=35, halign='center')
        self.add_widget(self.login_input)

        self.show_accounts()

    def AccountButton(self, instance):
        self.wm.login(self.image_buttons[instance])

    def show_accounts(self):

        size_hint = (0.25, 0.25)
        x, top = 0, 1

        for account in self.accounts:
            AccountPseudo = account['name']
            Async = None
            AccountName = None
            ImageButton = None

            if AccountPseudo not in self.accounts_informations:
                Async = AsyncImage(source=account['avatar']["large"], size_hint=size_hint, pos_hint={"x": x, "top": top})
                AccountName = Label(text=AccountPseudo, size_hint=(0.25, 0.25), pos_hint={"x": x, "top": top}, halign='center', font_size=30, color=(1, 1, 1, 1), outline_width= 1, outline_color= (0, 0, 0, 1))
                ImageButton = Button(size_hint=size_hint, pos_hint={"x": x, "top": top}, background_color=(0, 0, 0, 1))
                self.accounts_informations[AccountPseudo] = [Async, AccountName, ImageButton]
                self.image_buttons[ImageButton] = AccountPseudo
            else:
                Async = self.accounts_informations[AccountPseudo][0]
                AccountName = self.accounts_informations[AccountPseudo][1]
                ImageButton = self.accounts_informations[AccountPseudo][2]

                Async.pos_hint = {"x": x, "top": top}
                AccountName.pos_hint = {"x": x, "top": top}
                ImageButton.pos_hint = {"x": x, "top": top}
                self.image_buttons[ImageButton] = AccountPseudo


            ImageButton.bind(on_press=self.AccountButton)


            x += size_hint[0]

            if x+size_hint[0] >= 1:
                x = 0
                top -= size_hint[1]

            self.add_widget(ImageButton)
            self.add_widget(Async)
            self.add_widget(AccountName)



    def login(self, text=None):

        if text is not None:
            self.login_input.text = text

        correct = False
        al = None

        try:
            al = AnimeLogger(pseudo=self.login_input.text, fonclog=None, usertest=True)
            if al.user['data']['User']['name'] == self.login_input.text:
                if al.user['data']['User'] not in self.accounts:
                    correct = True
                else:
                    correct = False
            else:
                correct = False
        except:
            correct = False

        if correct:

            self.login_input.text = ""
            self.accounts.append(al.user['data']['User'])

            self.widgets()


    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if keycode == 40:
            self.login()
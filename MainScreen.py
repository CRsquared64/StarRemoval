from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

Window.fullscreen = False
Window.clearcolor = (0.49, 0.49, 0.49, 0.49)

class MainScreen(Screen):
    pass
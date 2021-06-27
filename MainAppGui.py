import cv2
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

import ImageStar
from MainScreen import MainScreen
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import ImageStar

Builder.load_file('Kv\MainScreen.kv')


class textinp(Widget):
    pass


class StarRemoval(App):
    def build(self):
        Config.set('graphics', 'resizable', False)
        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800
        return sl()

    def gettext(self, instance, imagename, image):
        print(imagename)
        self.root.get_screen("MainScreen").ids["image"].source = imagename
        self.imagename = imagename

    def process(self):
        imagename = self.imagename
        ImageStar.RemoveStars(imagename)
        self.root.get_screen("MainScreen").ids["jojo"].source = 'finished.jpg'





class sl(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(sl, self).__init__(**kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()

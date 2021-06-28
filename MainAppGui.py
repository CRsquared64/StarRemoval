import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
import ImageStar
from MainScreen import MainScreen

kivy.require('2.0.0')


class StarRemoval(App):
    def build(self):
        Builder.load_file('MainScreen.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800
        return sl()

    def gettext(self, instance, imagename, image):
        print(imagename)
        self.root.get_screen("MainScreen").ids["image"].source = imagename
        self.imagename = imagename

    def threshold(self, instance, thresh, giorno):
        print(thresh)
        self.root.get_screen("MainScreen").ids["giorno"].source = thresh
        self.thresh = thresh

    def process(self):
        imagename = self.imagename
        thresh = self.thresh
        thresh = float(thresh)
        ImageStar.RemoveStars(imagename, thresh)
        self.root.get_screen("MainScreen").ids["jojo"].source = 'finished.jpg'


class sl(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(sl, self).__init__(**kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()

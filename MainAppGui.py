import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
import ImageStar
from MainScreen import MainScreen

kivy.require('2.0.0')


class StarRemoval(App):
    current_image_path: str = ""
    current_threshold: int = 0

    def build(self):
        Builder.load_file('MainScreen.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800
        return sl()

    def gettext(self, path):
        print(path)
        self.current_image_path = path

    def threshold(self, thresh):
        print(thresh)
        self.current_threshold = thresh

    def process(self):
        path = self.current_image_path

        if path == "":
            return

        thresh = self.current_threshold
        thresh = float(thresh)
        ImageStar.RemoveStars(path, thresh)
        self.root.get_screen("MainScreen").ids["jojo"].source = 'finished.jpg'


class sl(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(sl, self).__init__(**kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()

from tkinter import Tk, filedialog

# Have to do this first because kivy breaks tkinter
window = Tk()
window.withdraw()


import os
from threading import Thread

import kivy
from kivy import Logger
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

import starFunctions
from mainScreen import MainScreen

kivy.require('2.0.0')



def mainloop(function):
    def wrapper(*args, **kwargs):
        Clock.schedule_once(lambda _elapsed_time: function(*args, **kwargs), 0)

    return wrapper


class StarRemoval(App):
    current_image_path: str = ""
    current_threshold: int = 0

    def build(self):
        Builder.load_file('MainScreen.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800
        return SM()


    def open_file_explorer(self):
        paths = filedialog.askopenfilenames()
        Logger.debug(f"Paths set to {paths}")
        self.root.get_screen("MainScreen").ids["path_button"].text = str(paths)

        Logger.info(f"Current path set to {paths}")
        if len(paths) > 0:
            self.current_image_path = paths[0]
            self.root.get_screen("MainScreen").ids["before_image"].source = str(paths[0])

    def set_threshold(self, thresh):
        Logger.info(f"Current threshold set to {thresh}")
        self.current_threshold = thresh


    def process(self):
        Logger.info("Starting to process image")

        path = self.current_image_path

        if path == "":
            return

        thresh = self.current_threshold
        thresh = float(thresh)


        thread = Thread(target=starFunctions.remove_stars, args=(path, thresh, self.process_finished,
                                                                self.set_processing_text, self.set_time_taken, self.set_stars_amount))
        thread.start()
        self.root.get_screen("MainScreen").ids["process_button"].disabled = True
        self.root.get_screen("MainScreen").ids["after_image"].source = ""


    @mainloop
    def process_finished(self):
        Logger.info("Finished processing image")
        self.root.get_screen("MainScreen").ids["after_image"].source = str(os.path.splitext(self.current_image_path)[0] + "-no_stars-" + str(self.current_threshold) +
                                                                           os.path.splitext(self.current_image_path)[1])
        self.root.get_screen("MainScreen").ids["after_image"].reload()
        self.root.get_screen("MainScreen").ids["process_button"].disabled = False
        self.root.get_screen("MainScreen").ids["process_label"].text = ""

    @mainloop
    def set_processing_text(self, new_text):
        self.root.get_screen("MainScreen").ids["process_label"].text = new_text

    @mainloop
    def set_time_taken(self, time):
        self.root.get_screen("MainScreen").ids["time"].text = f"Time: {time}"

    @mainloop
    def set_stars_amount(self, stars):
        self.root.get_screen("MainScreen").ids["starcounter"].text = f"Stars Detected: {stars}"




class SM(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()

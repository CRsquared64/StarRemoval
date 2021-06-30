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
import systemInfo
from mainScreen import MainScreen

kivy.require('2.0.0')



def mainloop(function):
    def wrapper(*args, **kwargs):
        Clock.schedule_once(lambda _elapsed_time: function(*args, **kwargs), 0)

    return wrapper


class StarRemoval(App):
    current_image_paths: list[str] = list()

    finished_image_paths: list[str] = list()

    current_threshold: int = 0
    do_switch_image = False

    amount_running = 0

    def build(self):
        Builder.load_file('MainScreen.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800

        Clock.schedule_interval(lambda _elapsed_time: self.switch_image(), 1)

        info_thread = Thread(target=systemInfo.computer_usage, args=(self.set_cpu_percent, self.set_memory_percent))

        info_thread.start()

        return SM()


    def switch_image(self):
        if len(self.current_image_paths) > 0:
            current1 = self.current_image_paths.index(self.root.get_screen("MainScreen").ids["before_image"].source) \
                if self.root.get_screen("MainScreen").ids["before_image"].source in self.current_image_paths else 0
            self.root.get_screen("MainScreen").ids["before_image"].source = \
                str(self.current_image_paths[(current1 + 1) % len(self.current_image_paths)])

        if len(self.finished_image_paths) > 0:
            current2 = self.finished_image_paths.index(self.root.get_screen("MainScreen").ids["after_image"].source) \
                if self.root.get_screen("MainScreen").ids["after_image"].source in self.finished_image_paths else 0
            self.root.get_screen("MainScreen").ids["after_image"].source = \
                str(self.finished_image_paths[(current2 + 1) % len(self.finished_image_paths)])


    def open_file_explorer(self):
        self.do_switch_image = True

        paths = filedialog.askopenfilenames()
        if paths == "":
            Logger.debug("No paths given, ignoring")
            return

        Logger.debug(f"Paths set to {paths}")
        self.root.get_screen("MainScreen").ids["path_button"].text = str(paths)

        Logger.info(f"Current path set to {paths}")
        self.current_image_paths = list(paths)


    def set_threshold(self, thresh):
        Logger.info(f"Current threshold set to {thresh}")
        self.current_threshold = thresh


    def process(self):
        self.finished_image_paths.clear()

        Logger.info("Starting to process image")

        for path in self.current_image_paths:
            self.amount_running += 1

            Logger.info(f"Processing image from {path}")

            thresh = float(self.current_threshold)


            thread = Thread(target=starFunctions.remove_stars, args=(path, thresh, self.process_finished,
                                                                     self.set_stars_amount, self.set_time_taken
                                                                     ))
            thread.start()
            self.root.get_screen("MainScreen").ids["process_button"].disabled = True




    @mainloop
    def process_finished(self, path):
        self.amount_running -= 1

        Logger.info(f"Finished processing image {path}")
        self.finished_image_paths.append(path)

        if self.amount_running == 0:
            self.root.get_screen("MainScreen").ids["process_button"].disabled = False


    @mainloop
    def set_time_taken(self, time):
        self.root.get_screen("MainScreen").ids["time_label"].text = f"Time: {time}"

    @mainloop
    def set_stars_amount(self, stars):
        self.root.get_screen("MainScreen").ids["star_count_label"].text = f"Stars Detected: {stars}"

    @mainloop
    def set_cpu_percent(self, cpu):
        self.root.get_screen("MainScreen").ids["cpu_usage_label"].text = f"CPU percent: {cpu}"

    @mainloop
    def set_memory_percent(self, memory):
        self.root.get_screen("MainScreen").ids["ram_usage_label"].text = f"RAM percent: {memory}"




class SM(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        self.add_widget(MainScreen(name="MainScreen"))


if __name__ == '__main__':
    Star = StarRemoval()
    Star.run()

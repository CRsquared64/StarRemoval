from tkinter import Tk, filedialog

# Have to do this first because kivy breaks tkinter
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

import killableThreads
from killableThreads import KillableThread
from scheduling_declarations import mainloop, next_frame




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
from imageProcessingInfoItem import ImageProcessingInfoItem

kivy.require('2.0.0')





class StarRemoval(App):
    image_paths: list[str] = ListProperty()

    finished_image_paths: list[str] = list()

    current_threshold: int = 0
    do_switch_image = False

    amount_running = 0

    def build(self):
        Builder.load_file('kvLang/MainScreen.kv')
        Builder.load_file('kvLang/ImageProcessingInfoItem.kv')

        Window.size = 850, 800
        Window.minimum_width = 850
        Window.minimum_height = 800

        info_thread = \
            KillableThread(target=systemInfo.computer_usage, args=(self.set_cpu_percent, self.set_memory_percent))

        info_thread.start()

        return SM()


    def add_image_path(self, path):
        layout: TabbedPanel = self.root.get_screen("MainScreen").ids["image_processing_info_layout"]

        tab: ImageProcessingInfoItem
        for tab in layout.tab_list:
            if tab.text == "Warning!":
                layout.remove_widget(tab)

        layout.add_widget(ImageProcessingInfoItem(path=path))
        Clock.schedule_once(lambda _elapsed_time: layout.switch_to(layout.tab_list[0]), 0)


    def open_file_explorer(self):
        self.do_switch_image = True

        paths = filedialog.askopenfilenames()
        if paths == "":
            Logger.debug("No paths given, ignoring")
            return

        Logger.debug(f"Added paths {paths}")
        for path in paths:
            self.add_image_path(path)


    def set_threshold(self, thresh):
        Logger.info(f"Current threshold set to {thresh}")
        self.current_threshold = thresh

    @mainloop
    @next_frame  # Makes @mainloop redundant but it improves understandability because it does need to be both
    def set_cpu_percent(self, cpu):
        self.root.get_screen("MainScreen").ids["cpu_usage_label"].text = f"CPU percent: {cpu}"

    @mainloop
    @next_frame
    def set_memory_percent(self, memory):
        self.root.get_screen("MainScreen").ids["ram_usage_label"].text = f"RAM percent: {memory}"




class SM(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        self.add_widget(MainScreen(name="MainScreen"))




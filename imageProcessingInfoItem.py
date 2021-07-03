import os
import threading
from threading import Thread
from typing import Union

from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty, AliasProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from killableThreads import KillableThread
from scheduling_declarations import next_frame, mainloop
from starFunctions import remove_stars


class ImageProcessingInfoItem(TabbedPanelItem):
    path = StringProperty()
    finished_path = StringProperty()
    thread: Union[KillableThread, None] = None

    def __init__(self, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

    @next_frame
    def on_path(self, _instance, value):
        Logger.debug(f"ImageProcessingInfoItem: Path set to {self.path}")

        self.text = str(os.path.splitext(os.path.basename(value))[0])
        self.ids["before_image"].source = value
        self.ids["path_label"].text = f"Path: {value}"

        self.update_thread()

    def update_thread(self):
        if self.thread is not None:
            raise RuntimeError("Cannot create thread id it is already created")

        if self.thread is not None:
            Logger.debug(f"ImageProcessingInfoItem: Terminating current thread")
            self.thread.terminate()
            self.thread = None

        Logger.debug(f"ImageProcessingInfoItem: Starting new thread")

        self.thread = KillableThread(target=remove_stars, args=(self.path, App.get_running_app().current_threshold,
                                                                {"stars": self.set_stars_amount,
                                                                 "finished_path": self.set_finished_path}))

        self.thread.start()

    @mainloop
    def set_stars_amount(self, amount):
        Logger.debug(f"Stars amount set to {amount}")
        self.ids["star_count_label"].text = f"Stars: {amount}"

    @mainloop
    def set_finished_path(self, path):
        print(threading.current_thread())

        Logger.debug(f"Finished path set to {path}")
        self.finished_path = path

    def on_finished_path(self, _instance, path):
        self.ids["after_image"].source = path

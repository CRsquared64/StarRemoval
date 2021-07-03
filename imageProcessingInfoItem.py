import os
from threading import Thread
from typing import Union

from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from killableThreads import KillableThread
from scheduling_declarations import next_frame
from starFunctions import remove_stars


class ImageProcessingInfoItem(TabbedPanelItem):
    path = StringProperty()
    thread: Union[KillableThread, None] = None

    def __init__(self, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

    @next_frame
    def on_path(self, _instance, value):
        Logger.debug(f"ImageProcessingInfoItem: Path set to {self.path}")

        self.text = str(os.path.splitext(os.path.basename(value))[0])
        self.ids["before_image"].source = value
        self.ids["path_label"].text = f"Path: {value}"

        if self.thread is not None:
            Logger.debug(f"ImageProcessingInfoItem: Terminating old thread")
            self.thread.terminate()
            self.thread = None

        self.create_thread()

    def create_thread(self):
        if self.thread is not None:
            raise RuntimeError("Cannot create thread id it is already created")

        Logger.debug(f"ImageProcessingInfoItem: Starting new thread")

        self.thread = KillableThread(target=remove_stars, args=(self.path, App.get_running_app().current_threshold,
                                                                print))

        self.thread.start()

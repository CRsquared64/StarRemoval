import os
import threading
from multiprocessing import Process, Manager
from threading import Thread
from typing import Union, Callable

from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, AliasProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from threadingFuncs import KillableThread
from scheduling_declarations import next_frame, mainloop
from starFunctions import remove_stars




print(2)

print(__name__)

funcs_from_other_process_that_were_run = Manager().list()
id_to_class_array = {}


def create_multi_process_safe_function(name, cls):
    if id(cls) not in id_to_class_array:
        id_to_class_array[id(cls)] = cls

    def build_array(*args, _name=name, _cls_id=id(cls), **kwargs):
        funcs_from_other_process_that_were_run.append(
            {"name": _name, "cls_id": _cls_id, "args": args, "kwargs": kwargs})

    return build_array


class MultiProcessSafeFunction:
    name: str
    id: int

    def __init__(self, name, cls):
        self.name = name
        self.id = id(cls)

        if self.id not in id_to_class_array:
            id_to_class_array[self.id] = cls

    def __call__(self, *args, **kwargs):
        print({"name": self.name, "cls_id": self.id, "args": args, "kwargs": kwargs})

        funcs_from_other_process_that_were_run.append(
            {"name": self.name, "cls_id": self.id, "args": args, "kwargs": kwargs})



class ImageProcessingInfoItem(TabbedPanelItem):
    path = StringProperty()
    finished_path = StringProperty()
    thread: Union[Process, None] = None



    def __init__(self, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

        Clock.schedule_interval(lambda _elapsed_time: self.check_funcs_from_other_process_that_were_run(), 0)


    def check_funcs_from_other_process_that_were_run(self):
        for func_from_other_process_that_were_run in funcs_from_other_process_that_were_run:
            print(func_from_other_process_that_were_run)
            if func_from_other_process_that_were_run["cls_id"] == id(self):
                print(10, func_from_other_process_that_were_run)



    def restart(self):
        Logger.debug("Restarting")

        self.ids["threshold_label"].text = f"Threshold: {App.get_running_app().current_threshold}"
        self.update_thread()

    @next_frame
    def on_path(self, _instance, value):
        Logger.debug(f"ImageProcessingInfoItem: Path set to {self.path}")

        self.text = str(os.path.splitext(os.path.basename(value))[0])
        self.ids["before_image"].source = value
        self.ids["path_label"].text = f"Path: {value}"
        self.ids["threshold_label"].text = f"Threshold: {App.get_running_app().current_threshold}"

        self.update_thread()

    def update_thread(self):
        if self.thread is not None:
            Logger.debug(f"ImageProcessingInfoItem: Terminating current thread")
            self.thread.terminate()
            self.thread = None

        Logger.debug(f"ImageProcessingInfoItem: Starting new thread")
        print(3)
        self.thread = Process(target=remove_stars, args=(self.path, App.get_running_app().current_threshold,
                                                                {"stars": MultiProcessSafeFunction(
                                                                    "set_stars_amount", self),
                                                                 "finished_path": MultiProcessSafeFunction(
                                                                     "set_finished_path", self),
                                                                 "time": MultiProcessSafeFunction(
                                                                     "set_time_taken", self)}))
        self.thread.start()

    @mainloop
    def set_stars_amount(self, amount):
        Logger.debug(f"Stars amount set to {amount}")
        self.ids["star_count_label"].text = f"Stars: {amount}"

    @mainloop
    def set_time_taken(self, amount):
        Logger.debug(f"Time taken set to {amount}")
        self.ids["time_label"].text = f"Time: {amount}"

    @mainloop
    def set_finished_path(self, path):
        Logger.debug(f"Finished path set to {path}")
        self.finished_path = path

    def on_finished_path(self, _instance, path):
        self.ids["after_image"].source = path

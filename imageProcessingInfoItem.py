import os
import platform
import subprocess
from threading import ThreadError
from typing import Union

from kivy import Logger
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from scheduling_declarations import next_frame, mainloop
from starFunctions import remove_stars
from threadingFuncs import KillableThread


def get_finished_path_from_path(path: str):

    path = str(path)

    path_to_file, file_name = os.path.split(path)
    path_to_file = os.path.join(path_to_file, "NoStarImages")

    file_name, ext = os.path.splitext(file_name)
    final_file_name = file_name + "-" + str(App.get_running_app().current_threshold) + ext

    final_path = os.path.join(path_to_file, final_file_name)
    return final_path


def get_mask_path_from_path(path: str):
    path = str(path)

    path_to_file, file_name = os.path.split(path)
    path_to_file = os.path.join(path_to_file, "NoStarMasks")

    file_name, ext = os.path.splitext(file_name)
    final_file_name = file_name + "-" + str(App.get_running_app().current_threshold) + ext

    final_path = os.path.join(path_to_file, final_file_name)
    return final_path





class ImageProcessingInfoItem(TabbedPanelItem):
    path = StringProperty()
    finished_path = StringProperty()
    mask_path = StringProperty()
    thread: Union[KillableThread, None] = None



    def __init__(self, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)



    def label_clicked(self, label):
        if label.text != "":

            if platform.system() == "Windows":
                os.startfile(label.text)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", label.text])
            else:
                subprocess.Popen(["xdg-open", label.text])



    @next_frame
    def on_path(self, _instance, value):
        Logger.debug(f"ImageProcessingInfoItem: Path set to {self.path}")

        self.text = str(os.path.splitext(os.path.basename(value))[0])
        self.ids["before_image"].source = value
        self.ids["after_image"].source = "fInChat"
        self.ids["path_label"].text = value

        self.finished_path = get_finished_path_from_path(self.path)
        self.mask_path = get_mask_path_from_path(self.path)


    def update_thread(self):
        self.finished_path = get_finished_path_from_path(self.path)
        self.ids["threshold_label"].text = f"Threshold: {App.get_running_app().current_threshold}"

        if self.thread is not None:
            Logger.debug(f"ImageProcessingInfoItem: Terminating current thread")
            try:
                self.thread.terminate()
            except ThreadError:
                pass
            self.thread = None

        Logger.debug(f"ImageProcessingInfoItem: Starting new thread")
        self.thread = KillableThread(target=remove_stars, args=(self.path, App.get_running_app().current_threshold,
                                                                get_finished_path_from_path(self.path), True,
                                                                {"stars": self.set_stars_amount,
                                                                 "finished": self.on_finished,
                                                                 "time": self.set_time_taken}),
                                     kwargs={"mask_path": self.mask_path})
        self.thread.start()

    @mainloop
    def set_stars_amount(self, amount):
        Logger.debug(f"Stars amount set to {amount}")
        self.ids["star_count_label"].text = f"Stars: {amount}"
        self.ids["mask_path_label"].text = self.mask_path

    @mainloop
    def set_time_taken(self, amount):
        Logger.debug(f"Time taken set to {amount}")
        self.ids["time_label"].text = f"Time: {amount}"

    @mainloop
    def on_finished(self):
        Logger.debug(f"Finished")

        self.ids["after_image"].source = self.finished_path

        self.ids["after_path_label"].text = self.finished_path


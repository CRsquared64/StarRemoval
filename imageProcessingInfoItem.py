import os

from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanelItem


class ImageProcessingInfoItem(TabbedPanelItem):
    def __init__(self, path, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

        self.path = path
        self.text = str(os.path.splitext(os.path.basename(path))[0])

        Clock.schedule_once(lambda _elapsed_time: self.update(), 0)

    def update(self):
        self.ids["before_image"].source = self.path
        self.ids["path_label"].text = f"Path: {self.path}"

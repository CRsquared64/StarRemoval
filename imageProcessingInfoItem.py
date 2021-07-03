import os

from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from scheduling_declarations import next_frame


class ImageProcessingInfoItem(TabbedPanelItem):
    path = StringProperty()

    def __init__(self, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

    @next_frame
    def on_path(self, _instance, value):
        self.text = str(os.path.splitext(os.path.basename(value))[0])
        self.ids["before_image"].source = value
        self.ids["path_label"].text = f"Path: {value}"

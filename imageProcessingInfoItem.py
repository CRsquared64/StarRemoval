import os

from kivy.uix.tabbedpanel import TabbedPanelItem


class ImageProcessingInfoItem(TabbedPanelItem):
    def __init__(self, path, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

        self.text = str(os.path.splitext(os.path.basename(path))[0])

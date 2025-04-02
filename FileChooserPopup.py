import os.path
import sys

from kivy.lang import Builder
from kivy.uix.popup import Popup
Builder.load_file(os.path.abspath('filechooserpopup.kv'))


class FileChooserPopup(Popup):
    chosen_callback = None
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "images")

    def on_selection(self, selection):
        self.chosen_callback(selection)
        self.dismiss()
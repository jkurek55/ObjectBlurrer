import os.path

from kivy.lang import Builder
from kivy.uix.popup import Popup
Builder.load_file(os.path.abspath('filechooserpopup.kv'))


class FileChooserPopup(Popup):
    chosen_callback = None
    image_path = os.path.abspath('images')

    def on_selection(self, selection):
        self.chosen_callback(selection)
        self.dismiss()
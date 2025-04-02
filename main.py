import os.path
import time
import win32timezone
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.popup import Popup
import cv2
from ultralytics import YOLO
from FileChooserPopup import *

class ObjectBlurrerScreen(BoxLayout):
    chosen_image_path = None
    yolo_model = YOLO(os.path.abspath('best.pt'))
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_path, 'blurred_images')
    shown_image_path = StringProperty(os.path.abspath('1.png'))
    file_chooser_popup = FileChooserPopup()

    def open_file_chooser(self):
        self.file_chooser_popup.chosen_callback = self.choose_image
        self.file_chooser_popup.open()

    def choose_image(self, selection):
        self.chosen_image_path = selection[0]
        self.shown_image_path = selection[0]

    def blur_objects(self, image, results):

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                roi = image[y1:y2, x1:x2].copy()
                if roi.size > 0:
                    blurred = cv2.GaussianBlur(roi, (45, 45), 50)
                    image[y1:y2, x1:x2] = blurred
        return image


    def blur_image(self, *args):
        image = cv2.imread(self.chosen_image_path)
        yolo_detections = self.yolo_model(image)
        blurred_image = self.blur_objects(image, yolo_detections)
        cv2.imwrite(self.output_path + '\\' + os.path.basename(self.chosen_image_path), blurred_image)
        self.shown_image_path = self.output_path + '\\' + os.path.basename(self.chosen_image_path)

class ObjectBlurrerApp(App):
    def build(self):
        return ObjectBlurrerScreen()

if __name__ == "__main__":
    ObjectBlurrerApp().run()

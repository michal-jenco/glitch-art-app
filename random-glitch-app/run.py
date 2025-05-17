import sys
import os
import json
import random
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
)

CONFIG_FILE = "glitch_config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


# === Glitch Effects === #
def glitch_1(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

def glitch_2(img):
    return img.rotate(180)

def glitch_3(img):
    return ImageOps.invert(img.convert("RGB"))

def glitch_4(img):
    return ImageEnhance.Color(img).enhance(3)

def glitch_5(img):
    return img.filter(ImageFilter.CONTOUR)

def glitch_6(img):
    img = img.convert("RGB")
    pixels = img.load()
    for i in range(0, img.size[0], 5):
        for j in range(0, img.size[1], 5):
            if i+1 < img.size[0] and j+1 < img.size[1]:
                pixels[i, j] = (255 - pixels[i, j][0], pixels[i, j][1], pixels[i, j][2])
    return img

def glitch_7(img):
    return img.transpose(Image.ROTATE_90)

def glitch_8(img):
    return ImageEnhance.Brightness(img).enhance(1.5)

def glitch_9(img):
    r, g, b = img.split()
    return Image.merge("RGB", (g, r, b))

def glitch_10(img):
    img = img.copy()
    w, h = img.size
    for _ in range(20):
        x = random.randint(0, w-10)
        y = random.randint(0, h-10)
        box = (x, y, x + 10, y + 10)
        region = img.crop(box)
        img.paste(region, (x + random.randint(-5, 5), y + random.randint(-5, 5)))
    return img

glitch_functions = [
    glitch_1, glitch_2, glitch_3, glitch_4, glitch_5,
    glitch_6, glitch_7, glitch_8, glitch_9, glitch_10
]


class GlitchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Glitch Image Generator")
        self.resize(400, 200)

        self.config = load_config()
        self.input_folder_path = self.config.get("input_folder", "")

        self.folder_label = QLabel("Folder: Not selected")
        if self.input_folder_path:
            self.folder_label.setText(f"Folder: {self.input_folder_path}")

        self.select_folder_btn = QPushButton("Select Image Folder")
        self.run_btn = QPushButton("Apply Glitch Effects")

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.select_folder_btn)
        layout.addWidget(self.run_btn)
        self.setLayout(layout)

        self.select_folder_btn.clicked.connect(self.select_folder)
        self.run_btn.clicked.connect(self.run_glitch_process)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.input_folder_path = folder
            self.folder_label.setText(f"Folder: {folder}")
            self.config['input_folder'] = folder
            save_config(self.config)

    def run_glitch_process(self):
        if not self.input_folder_path:
            QMessageBox.warning(self, "Error", "Please select an input folder.")
            return

        input_paths = list(Path(self.input_folder_path).glob("*.jpg"))
        if not input_paths:
            QMessageBox.warning(self, "Error", "No JPG images found in folder.")
            return

        output_folder = Path(self.input_folder_path) / "glitched"
        output_folder.mkdir(exist_ok=True)

        for img_path in input_paths:
            img = Image.open(img_path)
            glitch_func = random.choice(glitch_functions)
            glitched = glitch_func(img)
            output_path = output_folder / f"glitched_{img_path.name}"
            glitched.save(output_path)

        QMessageBox.information(self, "Done", f"Images saved to {output_folder}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GlitchApp()
    win.show()
    sys.exit(app.exec_())

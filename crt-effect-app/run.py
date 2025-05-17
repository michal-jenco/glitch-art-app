import sys
import os
import json
from math import cos, sin
from random import choice
from time import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSpinBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PIL import Image, ImagePalette
from helper_functions import generate_palette  # Your logic separated to another module

CONFIG_FILE = "glitch_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def generate_consecutive_palettes(img: Image,
                                  image_count: int,
                                  base_wave_size: int,
                                  palette_size: int | None = None) -> Image:

    palette = generate_palette(size=palette_size)
    x = 0

    funcs = (cos, sin)
    func_r = choice(funcs)
    func_g = choice(funcs)
    func_b = choice(funcs)

    for i in range(2, image_count + 2):
        x += 1
        print(f"making img {x}")
        ############# SWITCH BLOCK 1 and 2 FOR COOL EFFECT ################

        ############# BLOCK 2 ################
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        new_img = img.convert("P", palette=new_palette, colors=palette_size)
        new_img.putpalette(palette)
        ############# BLOCK 2 ################

        ############# BLOCK 1 ################
        new_img = new_img.convert("P",
                                  palette=Image.ADAPTIVE,
                                  colors=i if not palette_size else palette_size
                                  )
        ############# BLOCK 1 ################

        new_img = glitch_pixels(
            new_img,
            base_wave_size = base_wave_size,
            func_r = func_r,
            func_g = func_g,
            func_b = func_b,
            i = i,
        )

        img_save_name = f"pallette-out/veronika-zilinska/{int(time())}-{i}.png"
        new_img.save(img_save_name)


def glitch_pixels(img: Image, func_r, func_g, func_b, base_wave_size: int, i: int) -> Image:
    width, height = img.size

    print(func_r, func_g, func_b)

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            mod = int(h % 25)

            mod_r = int(h % 25)
            mod_g = int(h % 25)
            mod_b = int(h % 25)

            r, g, b = fractally_func_4(r, g ,b, h, w, func_r, func_g, func_b, base_wave_size, mod_r, mod_g, mod_b, i)

            pixels[w, h] = (r, g, b)

    return img


class GlitchPaletteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Glitch Palette Generator")
        self.resize(500, 300)
        self.config = load_config()

        self.image_path_label = QLabel("Image: Not selected")
        self.select_image_btn = QPushButton("Select Image")
        self.generate_btn = QPushButton("Generate")

        self.image_count_spin = QSpinBox()
        self.palette_size_spin = QSpinBox()
        self.wave_size_spin = QSpinBox()

        self.init_ui()
        self.connect_signals()
        self.load_config_state()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.select_image_btn)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Image Count:"))
        form_layout.addWidget(self.image_count_spin)
        form_layout.addWidget(QLabel("Palette Size:"))
        form_layout.addWidget(self.palette_size_spin)
        form_layout.addWidget(QLabel("Base Wave Size:"))
        form_layout.addWidget(self.wave_size_spin)
        layout.addLayout(form_layout)

        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

        self.image_count_spin.setValue(24)
        self.palette_size_spin.setValue(128)
        self.wave_size_spin.setValue(9)

    def connect_signals(self):
        self.select_image_btn.clicked.connect(self.select_image)
        self.generate_btn.clicked.connect(self.generate_images)

    def select_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Source Image", "", "Images (*.png *.jpg *.bmp)")
        if file:
            self.image_path = file
            self.image_path_label.setText(f"Image: {file}")
            self.config['image_path'] = file
            save_config(self.config)

    def generate_images(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Error", "No image selected!")
            return

        try:
            image = Image.open(self.image_path)
            image_count = self.image_count_spin.value()
            palette_size = self.palette_size_spin.value()
            base_wave_size = self.wave_size_spin.value()

            generate_consecutive_palettes(
                image,
                image_count=image_count,
                palette_size=palette_size,
                base_wave_size=base_wave_size
            )
            QMessageBox.information(self, "Done", "Glitched images generated successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_config_state(self):
        if 'image_path' in self.config:
            self.image_path = self.config['image_path']
            self.image_path_label.setText(f"Image: {self.image_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GlitchPaletteApp()
    window.show()
    sys.exit(app.exec_())

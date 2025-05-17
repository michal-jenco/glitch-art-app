import sys
import os
import json
from pathlib import Path
from time import time
from math import sin, cos
from numpy.random import choice
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QSpinBox, QHBoxLayout, QMessageBox
)
from PIL import Image, ImagePalette
from helper_functions import generate_palette

CONFIG_FILE = "config_glitch_ui.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def glitch_pixels(img: Image, func_r, func_g, func_b, base_wave_size: int, i: int, pixels=None) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]
            mod_r = int(h % 25)
            mod_g = int(h % 25)
            mod_b = int(h % 25)
            r, g, b = fractally_func_4(r, g, b, h, w, func_r, func_g, func_b, base_wave_size, mod_r, mod_g, mod_b, i)
            pixels[w, h] = (r, g, b)
    return img

def fractally_func_4(r, g, b, h, w, f1, f2, f3,
                     base_wave_size: int,
                     wave_size_modifier_r: int = 0,
                     wave_size_modifier_g: int = 0,
                     wave_size_modifier_b: int = 0,
                     i: int = 0) -> tuple:
    red_amount, green_amount, blue_amount = 255, 255, 255
    base_wave_size = 9
    new_r = r + .001 * (f1(b)/3 + h - (w * (i + 1))) / (base_wave_size + wave_size_modifier_r) * red_amount
    new_g = g + .001 * (f2(r)/3 + r) / (base_wave_size + wave_size_modifier_g) * green_amount
    new_b = b + .001 * (f3(g)/3 - h + (w / (i + 1))) / (base_wave_size + wave_size_modifier_b) * blue_amount
    return int(new_r), int(new_g), int(new_b)

def generate_consecutive_palettes(img: Image,
                                  image_count: int,
                                  base_wave_size: int,
                                  palette_size: int | None = None,
                                  output_dir: str = "pallette-out",
                                  pixels=None):
    palette = generate_palette(size=palette_size)
    funcs = (cos, sin)
    func_r = choice(funcs)
    func_g = choice(funcs)
    func_b = choice(funcs)

    for i in range(2, image_count + 2):
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        new_img = img.convert("P", palette=new_palette, colors=palette_size)
        new_img.putpalette(palette)
        new_img = new_img.convert("P", palette=Image.ADAPTIVE, colors=i if not palette_size else palette_size)
        new_img = glitch_pixels(new_img, func_r=func_r, func_g=func_g, func_b=func_b, base_wave_size=base_wave_size, i=i, pixels=pixels)
        img_save_name = os.path.join(output_dir, f"{int(time())}-{i}.png")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        new_img.save(img_save_name)

class GlitchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glitch Batch Generator")
        self.resize(400, 300)
        self.config = load_config()

        self.input_label = QLabel("Input Folder: Not selected")
        self.output_label = QLabel("Output Folder: Not selected")

        self.input_btn = QPushButton("Select Input Folder")
        self.output_btn = QPushButton("Select Output Folder")
        self.generate_btn = QPushButton("Generate Glitched Images")

        self.count_spin = QSpinBox()
        self.count_spin.setMaximum(100)
        self.count_spin.setValue(24)
        self.palette_spin = QSpinBox()
        self.palette_spin.setMaximum(256)
        self.palette_spin.setValue(128)
        self.base_wave_spin = QSpinBox()
        self.base_wave_spin.setMaximum(1000)
        self.base_wave_spin.setValue(9)

        self.setup_ui()
        self.connect_signals()
        self.restore_config()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_btn)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_btn)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Glitch Steps:"))
        hlayout.addWidget(self.count_spin)
        hlayout.addWidget(QLabel("Palette Size:"))
        hlayout.addWidget(self.palette_spin)
        hlayout.addWidget(QLabel("Base Wave Size:"))
        hlayout.addWidget(self.base_wave_spin)
        layout.addLayout(hlayout)

        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

    def connect_signals(self):
        self.input_btn.clicked.connect(self.select_input)
        self.output_btn.clicked.connect(self.select_output)
        self.generate_btn.clicked.connect(self.process_images)

    def select_input(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.config['input_folder'] = folder
            self.input_label.setText(f"Input Folder: {folder}")
            save_config(self.config)

    def select_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.config['output_folder'] = folder
            self.output_label.setText(f"Output Folder: {folder}")
            save_config(self.config)

    def restore_config(self):
        if 'input_folder' in self.config:
            self.input_label.setText(f"Input Folder: {self.config['input_folder']}")
        if 'output_folder' in self.config:
            self.output_label.setText(f"Output Folder: {self.config['output_folder']}")

    def process_images(self):
        input_folder = self.config.get('input_folder', '')
        output_folder = self.config.get('output_folder', '')

        if not input_folder or not output_folder:
            QMessageBox.warning(self, "Error", "Please select both input and output folders.")
            return

        paths = list(Path(input_folder).glob("*.jpg"))
        print(paths)
        if not paths:
            QMessageBox.warning(self, "Error", "No JPG files found in the input folder.")
            return

        for img_path in paths:
            try:
                img = Image.open(img_path).convert("RGB")
                pixels = img.load()
                generate_consecutive_palettes(
                    img,
                    image_count=self.count_spin.value(),
                    palette_size=self.palette_spin.value(),
                    base_wave_size=self.base_wave_spin.value(),
                    output_dir=output_folder,
                    pixels=pixels,
                )
            except Exception as e:
                print(f"Error processing {img_path.name}: {e}")

        QMessageBox.information(self, "Done", "Images processed and saved successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GlitchApp()
    window.show()
    sys.exit(app.exec_())

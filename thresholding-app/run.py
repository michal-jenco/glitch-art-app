import sys
import numpy as np
from pathlib import Path
from PIL import Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QSpinBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from time import time

# === Dummy helpers, REPLACE with your real implementations ===
def generate_palette(size=8):
    import random
    palette = []
    for _ in range(size):
        palette.extend([random.randint(0, 255) for _ in range(3)])
    return palette[:size * 3]  # Ensure size

def reduce_palette(palette_size, image, palette):
    new_image = image.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    return new_image

def average_rgb_pixel(r, g, b):
    return (r + g + b) / 3

# === Core glitch function ===
def threshold_pixels(img_orig, img_palette, threshold: int):
    out = []

    for orig_row, palette_row in zip(img_orig, img_palette):
        row = []
        for orig_pixel, palette_pixel in zip(orig_row, palette_row):
            avg_orig = average_rgb_pixel(*orig_pixel)
            row.append(orig_pixel if avg_orig < threshold else palette_pixel)
        out.append(row)

    return np.uint8(out)

# === PyQt GUI App ===
class ThresholdGlitchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threshold Glitch Generator")

        # Paths and settings
        self.input_folder = ""
        self.output_folder = ""

        # Widgets
        self.input_label = QLabel("Input folder: Not selected")
        self.output_label = QLabel("Output folder: Not selected")

        self.select_input_btn = QPushButton("Select Input Folder")
        self.select_output_btn = QPushButton("Select Output Folder")
        self.start_btn = QPushButton("Start Glitching")

        self.palette_spin = QSpinBox()
        self.palette_spin.setMinimum(2)
        self.palette_spin.setMaximum(256)
        self.palette_spin.setValue(8)

        self.variants_spin = QSpinBox()
        self.variants_spin.setMinimum(1)
        self.variants_spin.setMaximum(100)
        self.variants_spin.setValue(10)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.select_input_btn)
        layout.addWidget(self.output_label)
        layout.addWidget(self.select_output_btn)

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(QLabel("Palette Size:"))
        hlayout1.addWidget(self.palette_spin)
        layout.addLayout(hlayout1)

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(QLabel("Variants per Image:"))
        hlayout2.addWidget(self.variants_spin)
        layout.addLayout(hlayout2)

        layout.addWidget(self.start_btn)
        self.setLayout(layout)

        # Connections
        self.select_input_btn.clicked.connect(self.select_input_folder)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.start_btn.clicked.connect(self.run_glitch)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input folder: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_label.setText(f"Output folder: {folder}")

    def run_glitch(self):
        if not self.input_folder or not self.output_folder:
            print("Input/output folder missing!")
            return

        image_paths = list(Path(self.input_folder).glob("*.jpg"))
        palette_size = self.palette_spin.value()
        variants = self.variants_spin.value()

        for idx, img_path in enumerate(image_paths):
            photo = Image.open(img_path)
            np_photo = np.array(photo).astype(float)

            for i in range(variants):
                palette_image = Image.new("P", (1, 1))
                palette = generate_palette(palette_size)
                palette_image.putpalette(palette)

                reduced_img = reduce_palette(palette_size, photo, palette).convert("RGB")
                np_palette = np.array(reduced_img).astype(float)

                threshold = int(i * 10 % 250)
                combined = threshold_pixels(np_photo, np_palette, threshold)
                combined_img = Image.fromarray(np.array(combined).astype("uint8"))

                out_path = Path(self.output_folder) / f"{img_path.stem}_{i}.jpg"
                combined_img.save(out_path)

        print("Done glitching all images!")

# === Run the App ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    glitch_app = ThresholdGlitchApp()
    glitch_app.resize(400, 200)
    glitch_app.show()
    sys.exit(app.exec_())

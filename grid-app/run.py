import sys
import os
import json
from pathlib import Path
from time import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QSpinBox, QHBoxLayout, QCheckBox, QMessageBox
)
from PIL import Image
from helper_functions import create_image_grid, sliding_window_circular

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

class GridGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Grid Generator")
        self.resize(400, 300)

        self.config = load_config()

        self.input_folder = QLabel("Input Folder: Not selected")
        self.output_folder = QLabel("Output Folder: Not selected")

        self.select_input_btn = QPushButton("Select Input Folder")
        self.select_output_btn = QPushButton("Select Output Folder")
        self.generate_btn = QPushButton("Generate Grids")

        self.rows_spin = QSpinBox()
        self.cols_spin = QSpinBox()
        self.padding_spin = QSpinBox()
        self.outer_padding_spin = QSpinBox()
        self.resize_by_spin = QSpinBox()
        self.img_skip = QSpinBox()

        self.populate_ui()
        self.connect_signals()

        if 'input_folder' in self.config:
            self.input_folder_path = self.config['input_folder']
            self.input_folder.setText(f"Input Folder: {self.input_folder_path}")

        if 'output_folder' in self.config:
            self.output_folder_path = self.config['output_folder']
            self.output_folder.setText(f"Output Folder: {self.output_folder_path}")

    def populate_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_folder)
        layout.addWidget(self.select_input_btn)
        layout.addWidget(self.output_folder)
        layout.addWidget(self.select_output_btn)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Rows:"))
        form_layout.addWidget(self.rows_spin)
        form_layout.addWidget(QLabel("Cols:"))
        form_layout.addWidget(self.cols_spin)
        layout.addLayout(form_layout)

        padding_layout = QHBoxLayout()
        padding_layout.addWidget(QLabel("Padding:"))
        padding_layout.addWidget(self.padding_spin)
        padding_layout.addWidget(QLabel("Outer Padding:"))
        padding_layout.addWidget(self.outer_padding_spin)
        layout.addLayout(padding_layout)

        resize_layout = QHBoxLayout()
        resize_layout.addWidget(QLabel("Resize By:"))
        resize_layout.addWidget(self.resize_by_spin)
        layout.addLayout(resize_layout)

        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

        self.rows_spin.setValue(5)
        self.cols_spin.setValue(4)
        self.padding_spin.setValue(50)
        self.outer_padding_spin.setValue(50)
        self.resize_by_spin.setValue(3)

    def connect_signals(self):
        self.select_input_btn.clicked.connect(self.select_input_folder)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.generate_btn.clicked.connect(self.generate_grids)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder_path = folder
            self.input_folder.setText(f"Input Folder: {folder}")
            self.config['input_folder'] = folder
            save_config(self.config)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder_path = folder
            self.output_folder.setText(f"Output Folder: {folder}")
            self.config['output_folder'] = folder
            save_config(self.config)

    def generate_grids(self):
        if not hasattr(self, 'input_folder_path') or not hasattr(self, 'output_folder_path'):
            QMessageBox.warning(self, "Error", "Please select input and output folders.")
            return

        image_paths = list(Path(self.input_folder_path).glob("*.jpg"))
        if not image_paths:
            QMessageBox.warning(self, "Error", "No JPG images found in input folder.")
            return

        input_images = [Image.open(p) for p in image_paths[::3]]
        image_indexes = [i for i in range(len(input_images))] * 1
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        padding = self.padding_spin.value()
        outer_padding = self.outer_padding_spin.value()
        resize_by = self.resize_by_spin.value()

        windows = sliding_window_circular(image_indexes, rows * cols)
        output_folder = Path(self.output_folder_path)
        output_folder.mkdir(parents=True, exist_ok=True)

        for i, window in enumerate(windows):
            iteration_images = [input_images[idx] for idx in window]
            result = create_image_grid(
                images=iteration_images,
                rows=rows,
                cols=cols,
                padding=padding,
                outer_padding=outer_padding,
                resize_by=resize_by,
                direction="vertical")
            output_path = output_folder / f"grid_{int(time())}_{i}.jpg"
            print(f"Saving {output_path}")
            result.save(output_path)

        QMessageBox.information(self, "Done", "Grids generated successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridGeneratorApp()
    window.show()
    sys.exit(app.exec_())

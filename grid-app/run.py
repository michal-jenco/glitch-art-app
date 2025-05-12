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
import imageio.v2 as imageio
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
        self.resize(400, 400)

        self.config = load_config()

        self.input_folder = QLabel("Input Folder: Not selected")
        self.output_folder = QLabel("Output Folder: Not selected")
        self.video_folder = QLabel("Video Output Folder: Not selected")

        self.select_input_btn = QPushButton("Select Input Folder")
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_video_output_btn = QPushButton("Select Video Output Folder")
        self.generate_btn = QPushButton("Generate Grids")

        self.rows_spin = QSpinBox()
        self.cols_spin = QSpinBox()
        self.padding_spin = QSpinBox()
        self.outer_padding_spin = QSpinBox()
        self.resize_by_spin = QSpinBox()

        self.enable_video_checkbox = QCheckBox("Generate MP4 Video")
        self.frames_per_image_spin = QSpinBox()
        self.fps_spin = QSpinBox()

        self.populate_ui()
        self.connect_signals()

        if 'input_folder' in self.config:
            self.input_folder_path = self.config['input_folder']
            self.input_folder.setText(f"Input Folder: {self.input_folder_path}")

        if 'output_folder' in self.config:
            self.output_folder_path = self.config['output_folder']
            self.output_folder.setText(f"Output Folder: {self.output_folder_path}")

        if 'video_output_folder' in self.config:
            self.video_output_folder_path = self.config['video_output_folder']
            self.video_folder.setText(f"Video Output Folder: {self.video_output_folder_path}")

    def populate_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_folder)
        layout.addWidget(self.select_input_btn)
        layout.addWidget(self.output_folder)
        layout.addWidget(self.select_output_btn)
        layout.addWidget(self.video_folder)
        layout.addWidget(self.select_video_output_btn)

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

        layout.addWidget(self.enable_video_checkbox)

        video_opts_layout = QHBoxLayout()
        video_opts_layout.addWidget(QLabel("Frames/Image:"))
        video_opts_layout.addWidget(self.frames_per_image_spin)
        video_opts_layout.addWidget(QLabel("FPS:"))
        video_opts_layout.addWidget(self.fps_spin)
        layout.addLayout(video_opts_layout)

        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

        self.rows_spin.setValue(5)
        self.cols_spin.setValue(4)
        self.padding_spin.setValue(50)
        self.outer_padding_spin.setValue(50)
        self.resize_by_spin.setValue(3)
        self.frames_per_image_spin.setValue(2)
        self.fps_spin.setValue(30)

    def connect_signals(self):
        self.select_input_btn.clicked.connect(self.select_input_folder)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.select_video_output_btn.clicked.connect(self.select_video_output_folder)
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

    def select_video_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Video Output Folder")
        if folder:
            self.video_output_folder_path = folder
            self.video_folder.setText(f"Video Output Folder: {folder}")
            self.config['video_output_folder'] = folder
            save_config(self.config)

    def generate_grids(self):
        if not hasattr(self, 'input_folder_path') or not hasattr(self, 'output_folder_path'):
            QMessageBox.warning(self, "Error", "Please select input and output folders.")
            return

        image_paths = list(Path(self.input_folder_path).glob("*.jpg"))
        if not image_paths:
            QMessageBox.warning(self, "Error", "No JPG images found in input folder.")
            return

        input_images = [Image.open(p) for p in image_paths]
        image_indexes = [i for i in range(len(input_images))] * 1
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        padding = self.padding_spin.value()
        outer_padding = self.outer_padding_spin.value()
        resize_by = self.resize_by_spin.value()

        windows = sliding_window_circular(image_indexes, rows * cols)
        output_folder = Path(self.output_folder_path)
        output_folder.mkdir(parents=True, exist_ok=True)

        generated_files = []
        for i, window in enumerate(windows[::]):
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
            result.save(output_path)
            generated_files.append(output_path)

        if self.enable_video_checkbox.isChecked():
            if not hasattr(self, 'video_output_folder_path'):
                QMessageBox.warning(self, "Error", "Please select video output folder.")
                return

            video_frames = []
            for img_path in generated_files:
                frame = imageio.imread(img_path)
                video_frames.extend([frame] * self.frames_per_image_spin.value())

            video_output_path = Path(self.video_output_folder_path) / f"grid_video_{int(time())}.mp4"
            imageio.mimsave(video_output_path, video_frames, fps=self.fps_spin.value())

        QMessageBox.information(self, "Done", "Grids (and video) generated successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridGeneratorApp()
    window.show()
    sys.exit(app.exec_())

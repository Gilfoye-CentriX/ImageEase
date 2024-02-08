import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QProgressBar, QSlider, QHBoxLayout
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QPixmap
from PIL import Image
from io import BytesIO

class ImageEaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImageEase Compression")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel(self)
        background_image_path = r'C:\Users\Centrix\Documents\Imageasy\background\ImageEase.jpg'
        background_image_path_encoded = background_image_path.encode('utf-8').decode('latin1')
        self.label.setStyleSheet("QLabel { background-image: url('" + background_image_path_encoded + "'); background-repeat: no-repeat; background-position: center; }")
        self.label.setText("<html><div align='center'><font color='blue' size='7'><b>Welcome to ImageEase Compression</b></font></html>")
        self.upload_btn = QPushButton("Upload Image", self)
        self.compress_btn = QPushButton("Compress", self)
        self.exit_btn = QPushButton("Exit", self)
        self.progress_bar = QProgressBar(self)
        # Add labels for displaying file sizes
        self.original_size_label = QLabel("Original Size: ", self)
        self.compressed_size_label = QLabel("Compressed Size: ", self)
        # Add a slider for adjusting compression quality
        self.quality_label = QLabel("Quality:", self)
        self.quality_label.setAlignment(Qt.AlignCenter)
        self.quality_label.setStyleSheet("font-weight: bold;")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(50)  # Default value
        self.quality_slider.setTickInterval(5)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setSingleStep(1)
        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.save_btn = QPushButton("Save", self)

        # Set fixed width for buttons
        self.upload_btn.setFixedWidth(150)
        self.compress_btn.setFixedWidth(150)
        self.exit_btn.setFixedWidth(150)
        self.save_btn.setFixedWidth(150)

        # Layout for quality label and slider
        quality_layout = QVBoxLayout()
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.compress_btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.exit_btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.original_size_label)
        layout.addWidget(self.compressed_size_label)
        layout.addLayout(quality_layout)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.save_btn, alignment=Qt.AlignHCenter)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # Connect signals
        self.upload_btn.clicked.connect(self.upload_image)
        self.compress_btn.clicked.connect(self.compress_image)
        self.exit_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self.save_image)

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path  # Store the selected image path
            self.label.setText("Selected Image: {}".format(file_path))
            self.preview_label.clear()
        
    def compress_image(self):
        if hasattr(self, 'selected_image_path'):
            image_path = self.selected_image_path
            try:
                # Open the selected image
                image = Image.open(image_path)

                # Get the selected quality level from the slider
                quality = self.quality_slider.value()

                # Calculate original file size
                original_size = os.path.getsize(image_path) / 1024

                # Initialize progress bar
                total_bytes = len(image.tobytes())
                self.progress_bar.setMaximum(total_bytes)
                self.progress_bar.setValue(0)

                # Compress and save the image with the same format
                compressed_image = image.copy()
                with BytesIO() as buffer:
                    compressed_image.save(buffer, format=image.format, quality=quality)
                    compressed_image_bytes = buffer.getvalue()
                    buffer_length = len(compressed_image_bytes)

                    # Update progress bar periodically
                    update_interval = 4096
                    for i in range(0, buffer_length, update_interval):
                        bytes_processed = min(buffer_length, i + update_interval)
                        progress_percentage = (bytes_processed / buffer_length) * 100
                        self.progress_bar.setValue(int(progress_percentage))
                        QCoreApplication.processEvents()  # Allow GUI to update
                        time.sleep(0.01)  # Add a small delay

                    # Update progress bar to show completion
                    self.progress_bar.setValue(buffer_length)

                    # Display preview image
                    preview_image = Image.open(BytesIO(compressed_image_bytes))
                    preview_image = preview_image.resize((300, 300))  # Resize preview image for display
                    preview_image_bytes = BytesIO()
                    preview_image.save(preview_image_bytes, format='PNG')  # Convert preview image to PNG format
                    pixmap = QPixmap()
                    pixmap.loadFromData(preview_image_bytes.getvalue())
                    self.preview_label.setPixmap(pixmap)

                    # Display a pop-up window to indicate compression completion
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Compression Completed")
                    msg_box.setText("Completed Successfully.")
                    msg_box.exec()

                    # Update label to indicate compression completion
                    self.label.setText("Image Compression Completed")

                    # Calculate compressed file size
                    compressed_size = len(compressed_image_bytes) / 1024

                    # Display original and compressed file sizes
                    self.original_size_label.setText(f"Original Size: {original_size:.2f} KB")
                    self.compressed_size_label.setText(f"Compressed Size: {compressed_size:.2f} KB")
            except Exception as e:
                print("Error compressing image: {}".format(e))
                self.label.setText("Error compressing image: {}".format(e))
        else:
            self.label.setText("No image selected for compression")

    def save_image(self):
        if hasattr(self, 'selected_image_path'):
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.jpeg)")
            if file_path:
                image_path = self.selected_image_path
                try:
                    image = Image.open(image_path)
                    quality = self.quality_slider.value()

                    compressed_image = image.copy()
                    with BytesIO() as buffer:
                        compressed_image.save(buffer, format=image.format, quality=quality)
                        compressed_image_bytes = buffer.getvalue()

                        with open(file_path, 'wb') as f:
                            f.write(compressed_image_bytes)

                    self.label.setText("Image Saved Successfully")
                except Exception as e:
                    print("Error saving image: {}".format(e))
                    self.label.setText("Error saving image: {}".format(e))
        else:
            self.label.setText("No image selected for saving")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageEaseApp()
    window.show()
    sys.exit(app.exec())

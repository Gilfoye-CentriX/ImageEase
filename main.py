import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QProgressBar, QSlider
from PySide6.QtCore import QCoreApplication, Qt
from PIL import Image
from io import BytesIO

class ImageEaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImageEase Compression")
        self.setGeometry(100, 100, 600, 400)

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
        self.progress_bar = QProgressBar(self)  # Add progress bar
        # Add labels for displaying file sizes
        self.original_size_label = QLabel("Original Size: ", self)
        self.compressed_size_label = QLabel("Compressed Size: ", self)
        # Add a slider for adjusting compression quality
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(50)  # Default value
        self.quality_slider.setTickInterval(5)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setSingleStep(1)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.compress_btn)
        layout.addWidget(self.exit_btn)
        layout.addWidget(self.progress_bar)  # Add progress bar to layout
        layout.addWidget(self.original_size_label)
        layout.addWidget(self.compressed_size_label)
        layout.addWidget(self.quality_slider)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # Connect signals
        self.upload_btn.clicked.connect(self.upload_image)
        self.compress_btn.clicked.connect(self.compress_image)
        self.exit_btn.clicked.connect(self.close)

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path  # Store the selected image path
            self.label.setText("Selected Image: {}".format(file_path))
        
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

                    # Save compressed image
                    with open(image_path, 'wb') as f:
                        f.write(compressed_image_bytes)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageEaseApp()
    window.show()
    sys.exit(app.exec())

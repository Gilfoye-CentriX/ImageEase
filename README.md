ImageEase Compression

ImageEase Compression is a simple Python application built with PySide6 that allows users to compress images while maintaining control over the quality level of compression. The application provides a graphical user interface (GUI) for selecting an image file, adjusting the compression quality, and initiating the compression process.
Features
•	Upload Image: Allows users to select an image file (supported formats: PNG, JPG, JPEG) from their file system.
•	Compress: Initiates the compression process using the selected image and the specified compression quality level.
•	Quality Slider: Provides a slider for adjusting the compression quality level from 0 to 100.
•	Progress Bar: Displays the progress of the compression process.
•	Original and Compressed Size Display: Shows the original and compressed file sizes of the image.

Requirements
•	Python 3.x
•	PySide6
•	Pillow (Python Imaging Library)

Usage
1.	Install the required dependencies using pip:
pip install PySide6 Pillow 
2.	Run the application by executing the main.py file:
python main.py 
3.	Use the GUI to select an image file, adjust the compression quality (if desired), and initiate the compression process.
Important Note
•	The compressed image will overwrite the original image file. Make sure to use this application on copies of your images to avoid accidental loss of data.
Contributors
•	Mani Dlamini – Computer Scientist
License

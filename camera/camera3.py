#camera3.py

import time
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)

picam2.start()

# Wait a moment for the camera to adjust
time.sleep(2)

# Capture an image
picam2.capture_file("test_image.jpg")
print("Image captured as 'test_image.jpg'")

picam2.stop()
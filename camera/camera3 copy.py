#camera3.py

import time
from picamera2 import Picamera2
import cv2;

picam2 = Picamera2()
# config = picam2.create_preview_configuration()
# picam2.configure(config)

# picam2.start()

# # Wait a moment for the camera to adjust
# time.sleep(2)

# # Capture an image
# picam2.capture_file("test_image.jpg")
# print("Image captured as 'test_image.jpg'")

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

while True:
    frame = picam2.capture_array()
    cv2.imshow("Live", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
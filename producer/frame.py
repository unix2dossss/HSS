import numpy as np
import threading
import cv2

class FrameProducer:
    def __init__(self):
        self._frame = None
        self._lock = threading.Lock()

    def start(self):
        threading.Thread(target=self._produce_frame, daemon=True).start()

    def _produce_frame(self):
        cap = cv2.VideoCapture(2)

        while True:
            ret, frame = cap.read()
            with self._lock:
                self._frame = frame

    def get_frame(self):
        with self._lock:
            return self._frame
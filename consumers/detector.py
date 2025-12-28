import numpy as np
import threading
import cv2


class MotionDetector:
    def __init__(self, frame_producer):
        self.frame_producer = frame_producer

    def detect_motion(self):
        while True:
            frame = self.frame_producer.get_frame()
            cv2.imshow('frame', frame)
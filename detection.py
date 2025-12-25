import cv2
import numpy as np
from notification import *
import time
import os
import subprocess

cap = cv2.VideoCapture(2)

CAMERA_FPS = 30.0
SECONDS_TO_RECORD = 60

frame_rec_count = 0
detected_motion = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, CAMERA_FPS, (640, 480))

last_mean = 0
frames = 0
first_frame = True

MOVEMENT_THRESHOLD = 0.5

srt_file = open("output.srt", "w")
current_time_seconds = 0.0
subtitle_index = 1

notification_sent = False

def srt_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

while(True):
    frames += 1
    ret, frame = cap.read()
    # # Doesnt show on server
    # cv2.imshow('frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame', gray)

    current_mean = np.mean(gray)
    result = np.abs(current_mean - last_mean)
    # print(result)

    last_mean = current_mean

    # print frame every second
    if frames == 30:
        start = srt_timestamp(current_time_seconds)
        end = srt_timestamp(current_time_seconds + 1)

        srt_file.write(f"{subtitle_index}\n")
        srt_file.write(f"{start} --> {end}\n")
        srt_file.write(f"Movement: {result:.4f}\n\n")

        subtitle_index += 1
        current_time_seconds += 1.0

        print(result)
        frames = 0

    if first_frame:
        print("first frame")
        first_frame = False
        continue

    # 10 second buffer to avoid false positives on startup
    if result >= MOVEMENT_THRESHOLD and current_time_seconds > 10:
        print("Motion detected!", result)
        detected_motion = True
        if not notification_sent:

            subprocess.Popen([
                "aplay",
                "sounds/siren.wav"
            ])

            snapshot_path = f"snapshots/motion_{int(time.time())}.jpg"
            os.makedirs("snapshots", exist_ok=True)

            cv2.imwrite(snapshot_path, frame)
            send_photo(snapshot_path, caption="📸 Motion detected!")

            # notify("Motion Detected!")
            notification_sent = True

    if detected_motion: 
        out.write(frame)
        frame_rec_count += 1

    if (cv2.waitKey(1) & 0xFF == ord('q')) or frame_rec_count==SECONDS_TO_RECORD*CAMERA_FPS:
        break

    # # HWC: Height Width Color (400, 640, 3)
    # print(frame.shape)
    # # Grayscale = no color (400, 640)
    # print(gray.shape)


cap.release()
srt_file.close()
cv2.destroyAllWindows()
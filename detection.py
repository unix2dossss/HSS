import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frame_rec_count = 0
detected_motion = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640, 480))

last_mean = 0
frames = 0
first_frame = True

MOVEMENT_THRESHOLD = 0.5

while(True):
    frames += 1
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame', gray)

    current_mean = np.mean(gray)
    result = np.abs(current_mean - last_mean)
    # print(result)

    last_mean = current_mean

    # # print frames every 3 seconds
    # if frames == 150:
    #     print(result)
    #     frames = 0

    if first_frame:
        print("first frame")
        first_frame = False
        continue
    if result >= MOVEMENT_THRESHOLD:
        print("Motion detected!", result)
        detected_motion = True

    if detected_motion: 
        out.write(frame)
        frame_rec_count += 1

    if (cv2.waitKey(1) & 0xFF == ord('q')) or frame_rec_count==9000:
        break

    # # HWC: Height Width Color (400, 640, 3)
    # print(frame.shape)
    # # Grayscale = no color (400, 640)
    # print(gray.shape)


cap.release()
cv2.destroyAllWindows()
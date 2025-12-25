import cv2
import threading
import time
from flask import Flask, Response

# ---- config ----
CAM_INDEX = 2          # try 0, 1, 2 depending on your camera
WIDTH = 640
HEIGHT = 480
FPS = 30               # stream fps cap
JPEG_QUALITY = 80      # 0-100 (higher = better quality + more bandwidth)

# ---- camera worker ----
class Camera:
    def __init__(self, index: int):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera index {index}")

        # Try to set resolution (may be ignored by some cameras)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

        self.lock = threading.Lock()
        self.frame = None
        self.running = True

        t = threading.Thread(target=self._reader, daemon=True)
        t.start()

    def _reader(self):
        # Continuously read frames so the camera stays "warm"
        frame_interval = 1.0 / max(FPS, 1)
        while self.running:
            ok, frame = self.cap.read()
            if ok:
                with self.lock:
                    self.frame = frame
            time.sleep(frame_interval / 2)

    def get_jpeg(self) -> bytes | None:
        with self.lock:
            frame = None if self.frame is None else self.frame.copy()

        if frame is None:
            return None

        # Encode as JPEG
        ok, buf = cv2.imencode(
            ".jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY],
        )
        if not ok:
            return None
        return buf.tobytes()

    def close(self):
        self.running = False
        time.sleep(0.2)
        self.cap.release()


app = Flask(__name__)
cam = Camera(CAM_INDEX)

def mjpeg_generator():
    boundary = b"--frame"
    while True:
        jpg = cam.get_jpeg()
        if jpg is None:
            time.sleep(0.05)
            continue

        yield boundary + b"\r\n" + \
              b"Content-Type: image/jpeg\r\n" + \
              f"Content-Length: {len(jpg)}\r\n\r\n".encode() + \
              jpg + b"\r\n"

        time.sleep(1.0 / max(FPS, 1))


@app.get("/")
def index():
    return (
        "<h2>Live Camera</h2>"
        "<p>Open <a href='/video'>/video</a></p>"
    )

@app.get("/video")
def video():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    # host=0.0.0.0 exposes it to your LAN (and Tailscale if applicable)
    app.run(host="0.0.0.0", port=5000, threaded=True)

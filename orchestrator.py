import threading
from producer.frame import FrameProducer
from consumer.detector import MotionDetector

# this should orchestrate everything


# instantiate frame producer
# send frames to lazy_stream
# send frames to motion detector

producer = FrameProducer()
producer.start()

detector = MotionDetector(producer)

threading.Thread(target=detector.detect_motion, daemon=True).start()
import cv2
import numpy as np
from ar_app.objloader_simple import *
from ar_app.marker.detector import pipeline
from ar_app.ar_python3_opencv4 import VideoCapture


SCALE3D = 1  # Scale of the 3D model

def main():
    obj = OBJ("./models/fox/fox.obj", swapyz=True)
    camera_parameters = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
    reference_image = cv2.imread("./img/hiro.png", 0)

    # Init video capture
    cap = VideoCapture(0)
    while True:
        frame = cap.read()

        try:
            frame = pipeline(reference_image, frame, camera_parameters, obj, SCALE3D)
        except Exception as e:
            print(f"Error: {e}")

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    main()

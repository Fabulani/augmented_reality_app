import cv2
import numpy as np
from ar_app.objloader_simple import *
from ar_app.feature.detector import pipeline
from ar_app.ar_python3_opencv4 import VideoCapture


# ----- PARAMETERS
OBJ_PATH = "./models/fox/fox.obj"
REFERENCE_IMG_PATH = "./img/hiro.png"
CAMERA_PARAMETERS = np.array([
    [800, 0, 320], 
    [0, 800, 240], 
    [0, 0, 1]
])
SCALE3D = 1  # Scale of the 3D model
#! Change this to select which method to use: marker-based, or feature-based
PIPELINE_FUNC = pipeline
# TODO: use cmd args to select the pipeline function to import

def main():
    obj = OBJ(OBJ_PATH, swapyz=True)
    camera_parameters = CAMERA_PARAMETERS
    reference_image = cv2.imread(REFERENCE_IMG_PATH, 0)

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

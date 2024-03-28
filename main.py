import cv2
import numpy as np
import sys
from ar_app.objloader_simple import *
from ar_app.ar_python3_opencv4 import VideoCapture


# ----- PARAMETERS
OBJ_PATH = "./models/fox/fox.obj"  # Path to 3D model (.obj file)
REFERENCE_IMG_PATH = "./img/me-marker.png"  # Path to reference image (marker)
CAMERA_PARAMETERS = np.array(
    [[800, 0, 320], [0, 800, 240], [0, 0, 1]]  # Camera intrinsics matrix
)
SCALE3D = 1  # Scale of the 3D model


def main():
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <marker or feature>")
        exit()

    # Get the command line argument
    argument = sys.argv[1]

    # Check if the argument is either 'marker' or 'feature'
    if argument not in ["marker", "feature"]:
        print("Invalid argument. Please enter 'marker' or 'feature'.")
        exit()

    # Use pipeline from selected method
    if argument == "marker":
        from ar_app.marker_detection import pipeline
    else:
        from ar_app.feature_detection import pipeline

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
            print(f"Warning: {e}")

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    main()

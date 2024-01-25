import cv2
import numpy as np
import sys
from ar_app.objloader_simple import *
from ar_app.ar_python3_opencv4 import VideoCapture, projection_matrix, render
from ar_app.feature_detection import find_homography
from ar_app.common import perspective_transformation, draw_polygon
from ar_app.feature_detection import pipeline


# ----- PARAMETERS
OBJ_PATH = "./models/fox/fox.obj"  # Path to 3D model (.obj file)
REFERENCE_IMG_PATH = "./img/hiro.png"  # Path to reference image (marker)
CAMERA_PARAMETERS = np.array(
    [[800, 0, 320], [0, 800, 240], [0, 0, 1]]  # Camera intrinsics matrix
)
SCALE3D = 1  # Scale of the 3D model


def main():
    obj = OBJ(OBJ_PATH, swapyz=True)
    camera_parameters = CAMERA_PARAMETERS
    ref_image = cv2.imread(REFERENCE_IMG_PATH, 0)
    # ----- Feature-based pipeline
    # Minimum number of matches
    MIN_MATCHES = 30

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # Create brute force matcher
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    ref_image_pts, ref_image_dsc = orb.detectAndCompute(ref_image, None)

    # Init video capture
    cap = VideoCapture(0)
    while True:
        frame = cap.read()

        # Compute scene keypoints and its descriptors
        sourceImagePts, sourceImageDsc = orb.detectAndCompute(frame, None)

        # Match frame descriptors with model descriptors
        matches = bf_matcher.match(ref_image_dsc, sourceImageDsc)

        # Sort them in the order of their distance
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) > MIN_MATCHES:
            homography = find_homography(ref_image_pts, sourceImagePts, matches)
            transformed_corners = perspective_transformation(
                homography, ref_image.shape
            )
            frame = draw_polygon(frame, transformed_corners)
            projection = projection_matrix(camera_parameters, homography)
            frame = render(frame, obj, projection, ref_image, SCALE3D, False)

            # frame = pipeline(ref_image, frame, camera_parameters, obj, SCALE3D)
        else:
            print("Not enough matches are found - %d/%d" % (len(matches), MIN_MATCHES))

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    main()

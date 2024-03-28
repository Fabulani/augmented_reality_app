import cv2
import numpy as np
from ar_app.ar_python3_opencv4 import projection_matrix, render
from ar_app.common import perspective_transformation, draw_polygon


def feature_detection(ref_image, src_image, orb):
    # find the keypoints with ORB
    ref_image_pts = orb.detect(ref_image, None)
    src_image_pts = orb.detect(src_image, None)

    # compute the descriptors with ORB
    ref_image_pts, ref_image_dsc = orb.compute(ref_image, ref_image_pts)
    src_image_pts, src_image_dsc = orb.compute(src_image, src_image_pts)

    ref_image_features = cv2.drawKeypoints(
        ref_image, ref_image_pts, ref_image, color=(0, 255, 0), flags=0
    )
    src_image_features = cv2.drawKeypoints(
        src_image, src_image_pts, src_image, color=(0, 255, 0), flags=0
    )

    return ref_image_features, src_image_features


def feature_matching(src_image, ref_image_dsc, orb, matcher):
    # Compute keypoints and descriptors
    src_image_pts, src_image_dsc = orb.detectAndCompute(src_image, None)

    # Match descriptors
    matches = matcher.match(ref_image_dsc, src_image_dsc)

    # Sort in order of distance
    matches = sorted(matches, key=lambda x: x.distance)
    return src_image_pts, matches


def find_homography(ref_image_pts, src_image_pts, matches, min_matches=30):
    # if len(matches) > min_matches:
    # Get the good key points positions
    homography_src_pts = np.float32(
        [ref_image_pts[m.queryIdx].pt for m in matches]
    ).reshape(-1, 1, 2)
    homography_dst_pts = np.float32(
        [src_image_pts[m.trainIdx].pt for m in matches]
    ).reshape(-1, 1, 2)

    # Obtain the homography matrix
    homography, _ = cv2.findHomography(
        homography_src_pts, homography_dst_pts, cv2.RANSAC, 5.0
    )
    return homography


def pipeline(ref_image, frame, camera_parameters, obj, scale3d):
    # Initiate ORB detector
    orb = cv2.ORB_create()
    min_matches = 30

    ref_image_features, src_image_features = feature_detection(ref_image, frame, orb)
    ref_image_pts, src_image_pts, matches = feature_matching(ref_image, frame, orb)
    if len(matches) > min_matches:
        homography = find_homography(
            ref_image_pts, src_image_pts, matches, min_matches=30
        )
        transformed_corners = perspective_transformation(homography, ref_image.shape)
        frame = draw_polygon(
            frame, transformed_corners
        )  # Draw detection on top of image
        projection = projection_matrix(camera_parameters, homography)
        frame = render(frame, obj, projection, ref_image, scale3d, False)
    return frame

import cv2
import numpy as np
from ar_app.objloader_simple import *
from ar_app.ar_python3_opencv4 import projection_matrix, render
from ar_app.common import perspective_transformation, draw_polygon

# Parameters
MIN_INTERSECTION_DISTANCE = 100
CANNY_THRESHOLD1 = 100
CANNY_THRESHOLD2 = 500
HOUGH_THRESHOLD = 2
HOUGH_MIN_LINE_LENGTH = 50
HOUGH_MAX_LINE_GAP = 20


def find_intersections(
    lines,
    image_shape,
    border_threshold=10,
    min_intersection_distance=MIN_INTERSECTION_DISTANCE,
):
    intersections = []

    def distance(pt1, pt2):
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]

            # Check if the lines are not too parallel
            angle_threshold = np.radians(15)
            if (
                np.abs(np.arctan2(y2 - y1, x2 - x1) - np.arctan2(y4 - y3, x4 - x3))
                > angle_threshold
            ):
                # Calculate intersection point
                det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if det != 0:
                    intersection_x = (
                        (x1 * y2 - y1 * x2) * (x3 - x4)
                        - (x1 - x2) * (x3 * y4 - y3 * x4)
                    ) / det
                    intersection_y = (
                        (x1 * y2 - y1 * x2) * (y3 - y4)
                        - (y1 - y2) * (x3 * y4 - y3 * x4)
                    ) / det

                    # Check if the intersection point is within the image bounds
                    if (
                        border_threshold
                        <= intersection_x
                        < image_shape[1] - border_threshold
                        and border_threshold
                        <= intersection_y
                        < image_shape[0] - border_threshold
                    ):
                        new_intersection = (int(intersection_x), int(intersection_y))

                        # Check the minimum distance to existing intersections
                        if all(
                            distance(new_intersection, intersection)
                            >= min_intersection_distance
                            for intersection in intersections
                        ):
                            intersections.append(new_intersection)

    # Check if all 4 corners were detected
    assert len(intersections) == 4, f"{len(intersections)} points detected, must be 4."

    return intersections


def find_homography(intersections: list, reference_image_shape: tuple):
    h, w = reference_image_shape
    REFERENCE_CORNERS = [[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]
    src_points = np.array(REFERENCE_CORNERS, dtype=np.float32)
    dst_points = np.array(intersections, dtype=np.float32)

    homography, _ = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)
    return homography


def pipeline(reference_image, image, camera_parameters, obj, scale3d):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, CANNY_THRESHOLD1, CANNY_THRESHOLD2)
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=HOUGH_THRESHOLD,
        minLineLength=HOUGH_MIN_LINE_LENGTH,
        maxLineGap=HOUGH_MAX_LINE_GAP,
    )
    intersections = find_intersections(lines, image.shape)
    homography = find_homography(intersections, reference_image.shape)
    transformed_corners = perspective_transformation(homography, reference_image.shape)
    frame = draw_polygon(image, transformed_corners)  # Draw detection on top of image
    projection = projection_matrix(camera_parameters, homography)
    frame = render(frame, obj, projection, reference_image, scale3d, False)
    return frame

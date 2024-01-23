import numpy as np
import cv2


def perspective_transformation(homography, reference_image_shape: tuple):
    h, w = reference_image_shape
    corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners, homography)
    return transformed_corners


def draw_polygon(image, transformed_corners):
    return cv2.polylines(image, [np.int32(transformed_corners)], True, 255, 5, cv2.LINE_AA)

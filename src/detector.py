import numpy as np
import cv2

def find_intersections(lines):
    intersections = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            rho1, theta1 = lines[i][0]
            rho2, theta2 = lines[j][0]

            # Solve for intersection point
            A = np.array([
                [np.cos(theta1), np.sin(theta1)],
                [np.cos(theta2), np.sin(theta2)]
            ])
            b = np.array([rho1, rho2])
            intersection = np.linalg.solve(A, b)

            # Check if the intersection point is within the image bounds
            if 0 <= intersection[0] < image.shape[1] and 0 <= intersection[1] < image.shape[0]:
                intersections.append((int(intersection[0]), int(intersection[1])))

    return intersections

def find_squares(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help Canny edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find lines using HoughLinesP
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
    print(lines)

    # Find intersections of lines
    intersections = find_intersections(lines)

    squares = []

    # Find squares based on intersections
    for i in range(len(intersections)):
        for j in range(i+1, len(intersections)):
            for k in range(j+1, len(intersections)):
                for l in range(k+1, len(intersections)):
                    square = np.array([intersections[i], intersections[j], intersections[k], intersections[l]])
                    squares.append(square)

    return squares
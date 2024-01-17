# Augmented Reality App

Marker-based augmented reality app made with Python and OpenCV.

# Problems and solutions

This sections documents the many problems I faced during development of this project, and the solutions I opted for.

1. Lines detected in the border -> extra intersections -> bigger problems.
   - This problems originated from the edge detection section of the pipeline, where the Canny algorithm was detecting the corner pixels of the image as edges. The surface that the marker was put on was also causing edges to show up.
   - Fix: parameter tuning of the Canny algorithm thresholds.

   ![Problem: lines detected in the border](./docs/problem_line-detected-in-the-border.png "Problem: lines detected in the border")

2. Overlapping detected intersections.
   - Some overlapping intersections were being returned, causing a lot of problems down the pipeline, since every intersection is considered when evaluating for rectangles.
   - Fix: apply a check for minimum threshold distance between intersections.

   ![Problem: overlapping intersections](./docs/problem_overlapping-intersections.png "Problem: overlapping intersections")
   ![Fix: overlapping intersections](./docs/fix_overlapping-intersections.png "Fix: overlapping intersections")

3. Polygons instead of rectangles.
   - When detecting rectangles, I was exhautively tracing every intersections and getting all possibilities. This was stored in a variable called `squares`, with each element being a list of 4 points (i.e., intersections). I couldn't figure out the proper conditions and restrictions to only return actual rectangles instead of all kinds of polygons. At first, it'd return around 5k squares, but with each iteration of new conditions and rules being added, it returned less: 4k, then 2k, then 1k, then 53, then 2, then 1, and currently none. The "best" one was with 53 squares, but after plotting them, I noticed that none of the 53 squares fit the marker properly (the big white square and the black square inside it). I basically had to start from scratch for this step of the pipeline.
   - Fix: still trying to fix this...

   ![Problem: polygons instead of rectangles](./docs/problem_polygons-instead-of-rects-2.png "Problem: polygons instead of rectangles")

4. Overlapping lines for rectangle identification
   - After getting the list of "squares" (more like polygons), I'd use its lines to check if they're what I want, i.e. the marker. Many of these would have lines overlapping or crossing eachother, which doesn't make sense for a rectangle. This problem could be related to Problem 3.
   - fix: still trying to fix this... but a partial fix was to only detect 4 lines for the polygon instead of the 6 (originally used 6 lines because those included all possibilities of connections between intersections), although I'm not sure if it did fix it since adding this condition made me find no squares.

   ![Problem: overlapping lines for rectangle identification](./docs/problem_overlapping-lines.png "Problem: overlapping lines for rectangle identification")

# Discussions with ChatGPT

**ME**:

Ok ChatGPT. Let's step back for a second and think about the whole pipeline and the problems we are facing:
- The goal is to take a reference image (AR MARKER) and a source image (picture containing the marker in a random position) as input. The output must be the location of the marker in the source image. This location will later be used to render a 3D model on top of the marker, so keep this in mind.
- So far, we successfully implemented the inputs; converting the source image to gray scale; blurring the source image with gaussian blur; applying Canny edge detection to get the edges; finding the lines from the edges using HoughLinesP algorithm; and finally, finding the intersections of those lines. We also started to implement finding the squares from the found intersections, but it has several problems.
- The problems we are facing include: some intersections are noise (for example, we get some intersections in the border of the image);  the square detection function finds too many squares. Actually, it finds all possible polygons from the given intersections. Many of those polygons are not squares or rectangles, and many of them have intersecting lines, and superposing lines.
- I suspect one issues is in the source image having a line of pixels in its border, which could be causing issues in the edge detection and intersection detection parts of the algorithm. This is a problem that can show up when I implement video feed functionality, so we have to figure out how to avoid this edge case.
- We also have to figure out restrictions, conditions, and what so ever to avoid the weird polygons from intersections. The marker itself consist of two squares and the word Hiro in the center: a rectangular white borders, followed by a black border, and in the center a white square with the word Hiro written in black. I'm thinking of only picking the pairs of rectangles that have a matching center, i.e. the second rectangle must be entirely contained within the first rectangle. What do you think?

If you have any suggestions, I'd love to hear them

**CHATGPT**

Certainly, let's break down the issues and discuss potential solutions:

### 1. [DONE] **Noise in Intersections:**
   - To address noise in intersections, you can consider filtering out intersections that are too close to the image borders. You might set a threshold distance from the image borders and discard intersections that fall within that range.

### 2. **Avoiding Weird Polygons:**
   - You've rightly identified the issue with the current approach that results in various polygons. Restricting the detection to only pairs of rectangles with a matching center is a valid and reasonable approach. Ensuring that the second rectangle is entirely contained within the first one can help filter out unwanted polygons.

### 3. [DISCARDED] **Handling Border Effects in Edge Detection:**
   - To handle potential issues caused by a line of pixels at the image border, you can consider cropping the image before processing. This way, you remove the border that might interfere with edge detection. Ensure that the important content of the image, especially the marker, remains in the cropped region.

### 4. **Improving Square Detection:**
   - Consider refining the square detection algorithm. Instead of a brute-force approach, you might filter out potential rectangles based on certain criteria. For example, rectangles with similar areas or aspect ratios can be considered valid candidates.

### 5. **Verification Using Marker Structure:**
   - Utilize the known structure of the marker to verify the detected rectangles. Since you know the marker consists of two rectangles with a matching center, use this information to filter out false positives.

### 6. [DONE] **Parameter Tuning:**
   - Experiment with parameter tuning in the edge detection and line detection steps. Adjusting parameters like the Canny edge detection thresholds or HoughLinesP parameters might improve the accuracy of the overall pipeline.

### 7. **Post-Processing:**
   - After detecting rectangles, you might perform additional post-processing steps to refine the results. This could include removing overlapping rectangles, merging close rectangles, or applying additional geometric constraints.

### 8. **Testing on Various Scenarios:**
   - Test your pipeline on various scenarios to ensure robustness. This includes different lighting conditions, marker orientations, and distances. It will help you identify and address potential challenges.

### 9. **Implementing Video Feed Functionality:**
   - When implementing video feed functionality, consider incorporating a mechanism to handle potential artifacts or fluctuations. Techniques like temporal filtering or tracking can be beneficial in a video stream.

By combining these strategies and addressing each issue iteratively, you can enhance the robustness and accuracy of your marker detection pipeline. Additionally, continuously testing and refining the pipeline on various scenarios will help uncover potential edge cases and improve overall performance.


# Credits

Code adapted from https://github.com/mafda/augmented_reality_101

"Scrap Auto Turret [Low-poly]" (https://skfb.ly/oCRyJ) by fizikoldun is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
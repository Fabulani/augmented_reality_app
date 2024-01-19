# Augmented Reality App

Marker-based augmented reality app made with Python and OpenCV.

# Problems and solutions

This sections documents the many problems I faced during development of this project, and the solutions I opted for.

1. Lines detected in the border -> extra intersections -> bigger problems.
   - This problem originated from the edge detection section of the pipeline, where the Canny algorithm was detecting the corner pixels of the image as edges. The surface that the marker was put on was also causing edges to show up.
   - Fix: parameter tuning of the Canny algorithm thresholds.

   ![Problem: lines detected in the border](./docs/problem_line-detected-in-the-border.png "Problem: lines detected in the border")

2. Overlapping detected intersections.
   - Some overlapping intersections were being returned, causing a lot of problems down the pipeline, since every intersection is considered when evaluating for rectangles.
   - Fix: apply a check for minimum threshold distance between intersections.

   ![Problem: overlapping intersections](./docs/problem_overlapping-intersections.png "Problem: overlapping intersections")
   ![Fix: overlapping intersections](./docs/fix_overlapping-intersections.png "Fix: overlapping intersections")

3. Polygons instead of rectangles.
   - When detecting rectangles, I was exhautively tracing every intersection and getting all possibilities. This was stored in a variable called `squares`, with each element being a list of 4 points (i.e., intersections). I couldn't figure out the proper conditions and restrictions to only return actual rectangles instead of all kinds of polygons. At first, it'd return around 5k squares, but with each iteration of new conditions and rules being added, it returned less: 4k, then 2k, then 1k, then 53, then 2, then 1, and currently none. The "best" one was with 53 squares, but after plotting them, I noticed that none of the 53 squares fit the marker properly (the big white square and the black square inside it). I basically had to start from scratch for this step of the pipeline.
   - Fix: scratched the rectangle identification. Now I use only the intersections for the marker corner and then apply homography.

   ![Problem: polygons instead of rectangles](./docs/problem_polygons-instead-of-rects-2.png "Problem: polygons instead of rectangles")

4. Overlapping lines for rectangle identification
   - After getting the list of "squares" (more like polygons), I'd use its lines to check if they're what I want, i.e. the marker. Many of these would have lines overlapping or crossing eachother, which doesn't make sense for a rectangle. This problem could be related to Problem 3.
   - fix: scratched the rectangle identification. Now I use only the intersections for the marker corner and then apply homography.

   ![Problem: overlapping lines for rectangle identification](./docs/problem_overlapping-lines.png "Problem: overlapping lines for rectangle identification")

5. Too many intersections (I only want 4: the corners of the marker)
   - I was frequently getting 16 or more intersections. It'd detect both square corners, but also erroneously detect intersections below the corners.
   - Fix: I increased the `min_intersection_distance` from 10 to 150. This works for the current image, but probably will cause problems in the video feed part, plus if the marker gets smaller in the source image. The previous value of 10 was used to fix overlapping intersections.

   ![Problem: too many intersections](./docs/problem_too-many-intersections.png "Problem: too many intersections")
   ![Fix: too many intersections](./docs/fix_too-many-intersections.png "Fix: too many intersections")

6. Homography sligthly wrong
   - The homography calculations were resulting in a slightly wrong position. It seemed like the scale was wrong.
   - Fix: adjusted the coordinates of the source (the 4 marker corners).

   ![Problem: Homography sligthly wrong](./docs/problem_homography-wrong-scale.png "Problem: Homography sligthly wrong")
   ![Fix: Homography sligthly wrong](./docs/fix_homography-wrong-scale.png "Fix: Homography sligthly wrong")



# Credits

Code adapted from https://github.com/mafda/augmented_reality_101

"Scrap Auto Turret [Low-poly]" (https://skfb.ly/oCRyJ) by fizikoldun is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
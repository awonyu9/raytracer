# Python Ray Tracing Engine

## Project description

In a computer graphics course, CS 260, as a class, we built a ray tracing engine from scratch in Python. It is able to ray trace objects, scenes, and meshes of varying complexities, efficiently. It also incorporates features such as reflections, adjustable lighting, shading (Gouraud, Blinn-Phong, Lambert), texture mapping, and a moveable camera.

At the end of the term, with a partner, we improved the base engine:
1. We made it more efficient, using bounding box and bounding volume hierarchy techniques
2. We tweaked it so that it could produce red-blue anaglyphs of any image, suitable for viewing with 3D glasses.

We made a small animation to showcase feature #2 that consists of a camera moving 360° around the center of a red-blue anaglyph scene. This is the animation:

<img src="images/scene-final.gif" width="300px" />

The scene file is `scene3h-behind.py`. In `combine_anaglyph.py`, we produced left and right images of each frame, using `run_rt_left.py` and `run_rt_right.py`, and ran them through the `anaglyph_red_blue()` function (in `ren3d/anaglyph_red_blue.py`), which produced all the frames found in the `rb-final` directory. Then, we used an online tool to combine all the frames into the above animation (in `images/scene-final.gif`).

## Usage

Using pypy is recommended, for increased efficiency.

### Ray trace a scene
***

e.g. Ray trace scene3f to get a 300x200 image.

Run: `pypy run_rt.py scene3f 300 200`

Images get stored in the `images` directory.

### View .ppm files
***

Run `pypy ppmview.py` on any .ppm file.

e.g. `pypy ppmview.py images/scene10-rt-500-500.ppm`

(A Stormtrooper!)

### Generate 90 left and right frames
***

e.g. Generate 90 left 500x400 frames rotating around scene4:

Run: `pypy run_rt_left.py scene4 500 400`

Images get stored in the `rb-left` directory.

### Combine left and right frame sets into a red-blue anaglyph
***

Run: `pypy combine_anaglyph.py [width] [height]`

(Right now, it is hard-coded so that it matches the files for `scene3h-behind.py`.)

Images get stored in the `rb-final` directory.
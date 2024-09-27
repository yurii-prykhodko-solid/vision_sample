# MadVision algo improvements ideas

## Face detection

Currently used algo for face tracking in the video clips is _OpenCV Haar Cascades_.

The upside of this method is that it is highly optimized and computationally cheap compared to other solutions.

There are a few alternatives that could be explored here:

1. Replacing OpenCV with a CNN (convolutional neural network) based model:
   - YOLO model
   - SSD model
2. A combination of a CNN with OpenCV: CNN for object detection, OpenCV for object tracking.

### YOLO

YOLO is a family of R-CNN object detection models.
They are fairly computationally expensive, but provide realtime performance and good accuracy at object detection.

Pros:

- Likely better accuracy compared to Haar.
- Likely faster than Haar and SSD, given it runs on good hardware.
- Able to detect non-frontally oriented faces -- side tilts, front tilts etc.
- There is a range of options for these models. They range from "large" to "small".
  Smaller models run faster and with less resources, but at the expense of accuracy.

Cons:

- Resource-intensive (expensive), run best in CUDA-enabled environments (but we'll likely need to have that for running Whisper already).

### SSD

Another kind of a CNN-based object detector.

Pros:

- Less resource-hungry than YOLO.
- Likely less accurate than YOLO, but likely more accurate compared to Haar.

Cons:

- Still more resource-demanding than OpenCV.
- Slower than YOLO

### NN + OpenCV

In order to reduce operation costs, it is possible to run CNN inference every Nth frame,
and interpolate between these using OpenCV object tracking.

This way we get an expensive, accurate detection from time to time,
and keep track of the detected object using a cheaper method.

We have a project in our portfolio that uses this exact mechanism, using YOLO.
Upon testing, this method yielded much more accurate object detection compared to OpenCV,
while being faster and less resource-intensive than relying purely on a neural network-based solution.

Besides, we were able to run this setup on a mobile device at 25FPS,
so the powerful hardware requirement becomes a bit more lax.

Pros:

- Good accuracy.
- Realtime processing speed (or faster).
- Cheaper to run.

Cons:

- Less accurate than pure CNN inference.

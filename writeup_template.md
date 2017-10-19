## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./writeup_img/ex_undistort.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./writeup_img/filters_trial.png "Binary Example"
[image4]: ./writeup_img/warped_binary.png "Warp Example"
[image5]: ./writeup_img/color_fit_lines.png "Fit Visual"
[image6]: ./writeup_img/example_output.png "Output"
[video1]: ./project_video_output.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the the IPython notebook located in "./P4-CarND-Advanced-Lane-Lines".

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function.

The results can be seen in the notebook.

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image1]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

def combineFilters(img):
    hls_s = hls_select(img,ind=2)
    lab_l = lab_select(img,ind=0)
    lab_b = lab_select(img,ind=2)
    white = white_select(img)
    
    output = (white | (hls_s & lab_b)  )  & lab_l

    return output

I used the following filters
    - S Channel from HLS space
    - L Channel from LAB space
    - B Channel from LAB space
    
When I combined the above three channels, I realized the filters had a difficult time detecting the white channels. Therefore, I added the white color filter to extract the white lane lines. 

Example image is:

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `getReverseBirdsEyeView()`, which appears in the "Helper Function" section in the notebook.  The `getReverseBirdsEyeView()` function takes as inputs an image (`img`). The source and destination vertices were hard coded after many trial and error.

```python
ny,nx = img.shape[:2]
src = np.float32([(575,464),
                  (707,464), 
                  (258,682), 
                  (1049,682)])
dst = np.float32([(450,0),
                  (nx-450,0),
                  (450,ny),
                  (nx-450,ny)])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 575, 464      | 450, 0        | 
| 707, 464      | 830, 0      |
| 258, 682     | 450, 720      |
| 1049, 682      | 830, 720        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I got a histogram for a sliding window to identify which areas had concentrated pixels in the binary warped image that has been filtered to only show the lane lines. Then I identified the non-zero pixels centered at the peak of the histograms. By using these non-zero pixels, I fit a polynomial. The resulting image show the output:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I first identified the pixels where the lane lines were.
Using the conversion factor of pixels/meter, I converted these pixels into meters.
Then, I fit a new polynomial to these pixel values in meter.
Using the formula provided in lecture, I calculated the radius.
I did this with the function 'calculateCurvature_meter()' in my notebook. 


#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I had the most difficulty in cases where the frame was too bright and saturated or too dark (shadow). I've also noticed my pipeline failing during the challenge videos where other cars are blocking the lane lines. 

I think all these issues can be resolved if I allow the current frame to utilize the previous frame's polynomial fit. The rationale behind this approach is that lane curvature does not change dramatically from frame to frame. By initializing with the poly fit from previous frame, I can create more robust lane finding pipeline.

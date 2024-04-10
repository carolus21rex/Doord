import numpy as np
import cv2

# Stereo SGBM (Semi-Global Block Matching) matcher settings
window_size = 5
min_disp = 0
num_disp = 16*6 - min_disp
stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                               numDisparities=num_disp,
                               blockSize=5,
                               P1=8 * 3 * window_size ** 2,
                               P2=32 * 3 * window_size ** 2,
                               disp12MaxDiff=1,
                               uniquenessRatio=10,
                               speckleWindowSize=100,
                               speckleRange=32)

for i in range(6):  # Assuming images are numbered from 000 to 005
    # Format the image file names based on the counter
    left_image_filename = f'left_image_{i:03d}.jpg'
    right_image_filename = f'right_image_{i:03d}.jpg'

    # Load the stereo images in grayscale
    left_image = cv2.imread(left_image_filename, 0)
    right_image = cv2.imread(right_image_filename, 0)

    if left_image is None or right_image is None:
        print(f"Failed to load images {left_image_filename} and/or {right_image_filename}")
        continue

    # Compute disparity map
    disparity = stereo.compute(left_image, right_image).astype(np.float32) / 16.0

    # Normalize the disparity map for display
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # Display the disparity map
    cv2.imshow(f'Disparity Map {i:03d}', disparity_normalized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

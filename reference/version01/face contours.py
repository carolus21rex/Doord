import cv2
import numpy as np
import json

cap = cv2.VideoCapture(0)  # Open the camera
count = 0


while True:
    ret, frame = cap.read()  # Read a frame from the camera
    frame_with_contours = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)  # Apply thresholding

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
    cv2.drawContours(frame_with_contours, contours, -1, (0, 255, 0), 2)

    # Display the frame with contours
    cv2.imshow('Frame with Contours', frame_with_contours)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):  # Check if spacebar is pressed



        # Store the contours in a file
        with open(f'frames\\contours_{count}.json', 'w') as f:
            json.dump([cnt.tolist() for cnt in contours], f)

        count += 1
    if key == ord('q'):  # Press 'q' to quit
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all windows

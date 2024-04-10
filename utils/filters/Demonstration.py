import cv2

def modify_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detector with lower thresholds
    edges = cv2.Canny(blurred, 5, 30)  # Adjust these thresholds as needed

    # Find contours only in the center half of the image
    height, width = edges.shape
    roi = edges[height // 4: 3 * height // 4, width // 4: 3 * width // 4]  # Select the center half of the image
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a red box around the selected area
    result_image = image.copy()
    cv2.rectangle(result_image, (width // 4, height // 4), (3 * width // 4, 3 * height // 4), (0, 0, 255), 2)

    # Draw contours in the selected area
    cv2.drawContours(result_image[height // 4: 3 * height // 4, width // 4: 3 * width // 4], contours, -1, (0, 255, 0), 2)

    return result_image

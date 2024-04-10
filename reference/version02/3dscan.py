import cv2

def capture_images_from_rotation(camera_index=0, num_images=3):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("capture the left half first")
    for i in range(num_images):
        # Assuming manual rotation, wait for a key press to capture each image
        input("Press Enter to capture image...")

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        image_path = f"left_image_{i:03d}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image {image_path} saved.")

    print("capture the right half")
    for i in range(num_images):
        # Assuming manual rotation, wait for a key press to capture each image
        input("Press Enter to capture image...")

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        image_path = f"right_image_{i:03d}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image {image_path} saved.")

    cap.release()

capture_images_from_rotation()

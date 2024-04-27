import os.path
import cv2
import torch


def init_model(cuda):
    """
    Initializes and returns the YOLOv5 model.

    This function checks if CUDA is available for GPU usage and sets the device accordingly.
    It then loads the YOLOv5 model with specified weights from the local drive, and puts model into evaluation mode.

    Returns:
        torch.nn.Module: YOLOv5 model ready for inference
    """
    if cuda:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device('cpu')
    model_path = 'deploy/best.pt'
    model = torch.hub.load(os.path.join(os.getcwd(), 'deploy', 'yolov5'), 'custom', path=model_path, source='local')
    model.to(device).eval()
    return model


def pass_model(model, frame):
    """
    Applies the YOLOv5 model on a frame and returns the frame with object bounding boxes.

    This function takes a frame in BGR format, converts it to RGB format, and passes it through the YOLOv5 model for object detection.
    For detected objects, it draws a rectangle on the original frame at the location specified by the bounding box coordinates.
    If the class ID is 0, it draws a green rectangle, otherwise it draws a red rectangle.

    Args:
        model (torch.nn.Module): YOLOv5 model used for inference
        frame (numpy.ndarray): Original BGR image frame to process

    Returns:
        numpy.ndarray: Original image frame with object bounding boxes
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)  # apply YOLO on image
    print("test")

    # Get box parameters
    for *box, score, class_id in results.xyxy[0].tolist():
        if class_id == 0:
            print("test2")
            return True
    return False


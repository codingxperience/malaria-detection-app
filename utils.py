# import os

# def check_folders():
#     paths = {
#         'uploads_path': 'uploads',
#         'images_path': 'uploads/images',
#     }
#     # Check whether the specified path exists or not
#     not_exist = [path for path in paths.values() if not os.path.exists(path)]
    
#     if not_exist:
#         print(f'Creating missing folders: {not_exist}')
#         for folder in not_exist:
#             os.makedirs(folder)

# def get_detection_folder():
#     '''
#     Returns the latest folder in runs/detect
#     '''
#     return max([os.path.join('runs', 'detect', folder) for folder in os.listdir(os.path.join('runs', 'detect'))], key=os.path.getmtime)

import os
import glob

def check_folders():
    """Ensures required directories exist."""
    folders = ["uploads", "uploads/images", "runs/detect"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def get_detection_folder():
    """Returns the latest YOLO detection folder (predict, predict1, etc.)."""
    detect_path = "runs/detect"
    if not os.path.exists(detect_path) or not os.listdir(detect_path):
        return None  # No detections yet
    
    # Sort predict folders by modification time (newest first)
    predict_folders = sorted(
        [os.path.join(detect_path, folder) for folder in os.listdir(detect_path) if folder.startswith("predict")],
        key=os.path.getmtime,
        reverse=True
    )
    return predict_folders[0] if predict_folders else None

def get_latest_detected_image(uploaded_filename):
    """Finds the most recent detected image in the latest YOLO output folder."""
    detection_folder = get_detection_folder()
    if not detection_folder:
        return None

    # Retrieve the most recent processed image (YOLO saves images as .jpg or .png)
    detected_images = sorted(
        glob.glob(os.path.join(detection_folder, "*")),
        key=os.path.getmtime,
        reverse=True
    )
    return detected_images[0] if detected_images else None


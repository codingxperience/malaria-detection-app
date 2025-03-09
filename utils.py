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

def check_folders():
    """
    Ensures required directories exist
    """
    folders = ["uploads", "uploads/images", "runs/detect"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def get_detection_folder():
    """
    Returns the latest detection folder path
    """
    detect_path = "runs/detect"
    if not os.path.exists(detect_path) or not os.listdir(detect_path):
        return None  # Return None if no detections exist

    return max([os.path.join(detect_path, folder) for folder in os.listdir(detect_path)], key=os.path.getmtime)

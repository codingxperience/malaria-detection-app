import os

def check_folders():
    paths = {
        'uploads_path': 'uploads',
        'images_path': 'uploads/images',
    }
    # Check whether the specified path exists or not
    not_exist = [path for path in paths.values() if not os.path.exists(path)]
    
    if not_exist:
        print(f'Creating missing folders: {not_exist}')
        for folder in not_exist:
            os.makedirs(folder)

def get_detection_folder():
    '''
    Returns the latest folder in runs/detect
    '''
    return max([os.path.join('runs', 'detect', folder) for folder in os.listdir(os.path.join('runs', 'detect'))], key=os.path.getmtime)
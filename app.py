import streamlit as st
from PIL import Image
import subprocess
import os

import utils

def detect_objects(image_path, model_path, output_dir):
    subprocess.run(['yolo', 'task=detect', 'mode=predict', f'model={model_path}', 'conf=0.25', f'source={image_path}'])

def main():
    st.title('Malaria Screener')

    # Check and create necessary folders
    utils.check_folders()

    # Sidebar for uploading files
    uploaded_file = st.sidebar.file_uploader("Load File", type=['png', 'jpeg', 'jpg'])

    if uploaded_file is not None:
        is_valid = True
        with st.spinner(text='Loading...'):
            st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            picture = Image.open(uploaded_file)
            picture.save(f'uploads/images/{uploaded_file.name}')
            source = f'uploads/images/{uploaded_file.name}'
    else:
        is_valid = False

    if is_valid:
        if st.button('Detect Malaria Parasites'):
            with st.spinner('Detecting Parasites...'):
                detect_objects(source, 'models/malariabest.pt', 'runs/detect')

                detected_image_path = os.path.join(utils.get_detection_folder(), os.path.basename(source))

                if os.path.exists(detected_image_path):
                    st.image(detected_image_path, caption="Its a turtle", use_column_width=True)
                else:
                    st.error("No object detected.")

if __name__ == '__main__':
    main()
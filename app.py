# import streamlit as st
# from PIL import Image
# from ultralytics import YOLO
# import os

# import utils

# # def detect_objects(image_path, model_path, output_dir):
# #     subprocess.run(['yolo', 'task=detect', 'mode=predict', f'model={model_path}', 'conf=0.25', f'source={image_path}'])

# def detect_objects(image_path, model_path, output_dir):
#     model = YOLO(model_path)
#     results = model.predict(source=image_path, conf=0.25)

# def main():
#     st.title('Malaria Screener')

#     # Check and create necessary folders
#     utils.check_folders()

#     # Sidebar for uploading files
#     uploaded_file = st.sidebar.file_uploader("Load File", type=['png', 'jpeg', 'jpg'])

#     if uploaded_file is not None:
#         is_valid = True
#         with st.spinner(text='Loading...'):
#             st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
#             picture = Image.open(uploaded_file)
#             picture.save(f'uploads/images/{uploaded_file.name}')
#             source = f'uploads/images/{uploaded_file.name}'
#     else:
#         is_valid = False

#     if is_valid:
#         if st.button('Detect Malaria Parasites'):
#             with st.spinner('Detecting Parasites...'):
#                 detect_objects(source, 'models/malariabest.pt', 'runs/detect')

#                 detected_image_path = os.path.join(utils.get_detection_folder(), os.path.basename(source))

#                 if os.path.exists(detected_image_path):
#                     st.image(detected_image_path, caption="Its a turtle", use_column_width=True)
#                 else:
#                     st.error("No object detected.")

# if __name__ == '__main__':
#     main()


import streamlit as st
from PIL import Image
from ultralytics import YOLO
import os
import utils

# Load the model once to avoid reloading issues
@st.cache_resource
def load_model():
    return YOLO("models/malariabest.pt")  # Ensure this path is correct

# Function to detect objects
def detect_objects(image_path, model):
    results = model.predict(source=image_path, conf=0.25, save=True)
    return results

def main():
    st.title("🦠 Malaria Screener")

    # Ensure necessary folders exist
    utils.check_folders()

    # Sidebar for uploading files
    uploaded_file = st.sidebar.file_uploader("Load File", type=['png', 'jpeg', 'jpg'])

    if uploaded_file:
        with st.spinner("Loading image..."):
            st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            img_path = f'uploads/images/{uploaded_file.name}'
            image = Image.open(uploaded_file)
            image.save(img_path)

        # Load model
        model = load_model()

        if st.button("🔍 Detect Malaria Parasites"):
            with st.spinner("Detecting..."):
                detect_objects(img_path, model)

                # Get latest detection folder
                detected_image_path = os.path.join(utils.get_detection_folder(), os.path.basename(img_path))
                
                if os.path.exists(detected_image_path):
                    st.image(detected_image_path, caption="Detected Malaria Parasites", use_column_width=True)
                else:
                    st.error("No parasites detected.")

if __name__ == "__main__":
    main()

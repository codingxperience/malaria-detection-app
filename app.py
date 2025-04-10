# import streamlit as st
# from PIL import Image
# from ultralytics import YOLO
# import os
# import asyncio
# import time
# import utils

# # Fix asyncio error in Windows
# if not hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# # Load the model once to avoid reloading issues
# @st.cache_resource
# def load_model():
#     return YOLO("models/malariabest.pt")  # Ensure this path is correct

# # Function to detect objects
# def detect_objects(image_path, model):
#     results = model.predict(source=image_path, conf=0.25, save=True)
#     return results

# def main():
#     st.title("🦠 Malaria Screener")

#     # Ensure necessary folders exist
#     utils.check_folders()

#     # Sidebar for uploading files
#     uploaded_file = st.sidebar.file_uploader("Load File", type=['png', 'jpeg', 'jpg'])

#     if uploaded_file:
#         with st.spinner("Loading image..."):
#             st.sidebar.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
#             img_path = f'uploads/images/{uploaded_file.name}'
#             image = Image.open(uploaded_file)
#             image.save(img_path)

#         # Load model
#         model = load_model()

#         if st.button("🔍 Detect Malaria Parasites"):
#             with st.spinner("Detecting..."):
#                 detect_objects(img_path, model)

#                 # Get latest detection folder
#                 detected_image_path = os.path.join(utils.get_detection_folder(), os.path.basename(img_path))
                
#                 if os.path.exists(detected_image_path):
#                     st.image(detected_image_path, caption="Detected Malaria Parasites", use_container_width=True)
#                 else:
#                     st.error("No parasites detected.")

# if __name__ == "__main__":
#     main()


import asyncio
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
import torch
import time
import io
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
from ultralytics import YOLO  
from utils import check_folders, get_latest_detected_image  

st.set_page_config(page_title="Malaria Screener", page_icon="🦠", layout="wide")

# ✅ Fix asyncio error for Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ✅ Ensure required folders exist
check_folders()

# ✅ Load YOLOv8 model
@st.cache_resource()
def load_model():
    return YOLO('models/malariabest.pt')

model = load_model()

# ✅ Sidebar: Upload Image
st.sidebar.header("📂 Upload Image")
uploaded_file = st.sidebar.file_uploader("Drag and drop file here", type=["png", "jpg", "jpeg"])
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.5, 0.05)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)

# ✅ Detection Function
def detect_image(image):
    img_array = np.array(image)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR) 
    results = model.predict(img_array, conf=confidence_threshold, save=True)
    return results

# ✅ Draw Results
def draw_results(image, results):
    draw = ImageDraw.Draw(image)
    detections = results[0].boxes.data.cpu().numpy()  
    parasite_count = 0

    for box in detections:
        x1, y1, x2, y2, conf, cls = box.tolist()
        class_name = model.names[int(cls)]
        
        color = "blue" if class_name.lower() == "wbc" else "red"
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        draw.text((x1, y1), f"{class_name} {conf:.2f}", fill=color)

        if class_name.lower() != "wbc":
            parasite_count += 1

    return image, parasite_count

# ✅ Main UI with Tabs
tabs = st.tabs(["🔍 Detection", "📊 Results & Summary", "ℹ️ About Malaria Detection"])

with tabs[0]:  
    st.markdown("<h1 style='text-align: center;'>🦠 Malaria Screener</h1>", unsafe_allow_html=True)

    if uploaded_file:
        if st.button("🔬 Detect Parasites"):
            with st.spinner("Processing... Please wait"):
                results = detect_image(image)
                time.sleep(2)  
            
            detected_img, parasite_count = draw_results(image.copy(), results)  

            # ✅ Retrieve detected image
            detected_image_path = get_latest_detected_image(uploaded_file.name)

            if detected_image_path and os.path.exists(detected_image_path):
                st.image(detected_image_path, caption="Detected Malaria Parasites", use_container_width=True)
            else:
                st.image(detected_img, caption="Detected Malaria Parasites", use_container_width=True)

            # ✅ Download Button
            img_bytes = io.BytesIO()
            detected_img.save(img_bytes, format='PNG')
            st.download_button("📥 Download Detected Image", img_bytes.getvalue(), file_name="malaria_detected.png", mime="image/png")

with tabs[1]:  
    if uploaded_file and 'parasite_count' in locals():
        st.subheader("📊 Detection Summary")
        st.metric("Total Detected Parasites", parasite_count)

        boxes = results[0].boxes.data.cpu().numpy()  
        conf_values = boxes[:, 4] if len(boxes) > 0 else []  

        if len(conf_values) > 0:
            plt.figure(figsize=(8, 4))
            plt.hist(conf_values, bins=10, color='skyblue', edgecolor='black')
            plt.xlabel("Confidence Score")
            plt.ylabel("Frequency")
            plt.title("Confidence Score Distribution")
            st.pyplot(plt)
        else:
            st.warning("No parasites detected. Try adjusting the confidence level.")
    else:
        st.info("Upload an image and detect parasites in the 'Detection' tab to see results.")

with tabs[2]:  
    st.subheader("ℹ️ About Malaria Detection")
    st.markdown("""
    Malaria detection uses **AI-powered YOLO models** to identify malaria parasites in blood smear images. 
    Early detection aids in timely treatment and improved patient outcomes. 🚑
    
    **How It Works:**
    - Upload a blood smear image.
    - The AI model analyzes the image and highlights parasites.
    - You can adjust detection confidence levels.
    - Download the results for further analysis.
    
    **Why This Matters:**
    - Fast and automated detection.
    - Reduces manual errors in microscopic diagnosis.
    - Supports healthcare professionals in malaria-endemic regions.
    
    Made with ❤️ using **Streamlit & YOLO AI**.
    """, unsafe_allow_html=True)

import streamlit as st
import zipfile
import os
from io import BytesIO

st.title("📦 Extract Images from Folder ZIP")

uploaded_zip = st.file_uploader("Upload a ZIP file containing all your folders with images", type=["zip"])

if uploaded_zip:
    # Extract zip to memory
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        image_files = [f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            st.error("No image files found in the ZIP.")
        else:
            # Create a new ZIP containing just the images
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as image_zip:
                for file in image_files:
                    image_zip.writestr(file, zip_ref.read(file))

            zip_buffer.seek(0)
            st.success(f"Found {len(image_files)} image(s).")
            st.download_button("⬇️ Download All Images Only", data=zip_buffer, file_name="cleaned_images.zip", mime="application/zip")

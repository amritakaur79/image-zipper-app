import streamlit as st
import zipfile
import os
from io import BytesIO
from PIL import Image

# Title
st.title("📂 Zip All Images from Nested Folders")

st.markdown("Upload a folder that contains subfolders with images. This tool will find all image files and let you download them as a single ZIP file.")

# Upload multiple files (simulate folder upload)
uploaded_files = st.file_uploader("Upload your image files (from subfolders too)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    # Create an in-memory zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            # Reconstruct the folder structure from the uploaded file's path
            folder_path = os.path.dirname(file.name)
            filename = os.path.basename(file.name)
            zip_path = os.path.join(folder_path, filename)

            # Write each image to the zip file
            zipf.writestr(zip_path, file.read())

    # Prepare for download
    zip_buffer.seek(0)
    st.download_button(
        label="⬇️ Download All Images as ZIP",
        data=zip_buffer,
        file_name="all_images.zip",
        mime="application/zip"
    )

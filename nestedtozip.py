import streamlit as st
import zipfile
from io import BytesIO
import os

st.title("📁 Flatten Image ZIP Tool")
st.markdown("Upload a ZIP file of folders containing images. This app will extract **all images**, ignore folder structure, and give you a single ZIP to download.")

uploaded_zip = st.file_uploader("Upload ZIP file", type=["zip"])

if uploaded_zip:
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        image_files = [f for f in zip_ref.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            st.error("No image files found in ZIP.")
        else:
            flat_zip = BytesIO()
            with zipfile.ZipFile(flat_zip, "w", zipfile.ZIP_DEFLATED) as out_zip:
                for file_path in image_files:
                    file_data = zip_ref.read(file_path)
                    # Get only filename (no folders)
                    flat_name = os.path.basename(file_path)
                    
                    # Avoid overwriting files with the same name
                    counter = 1
                    original_name = flat_name
                    while flat_name in out_zip.namelist():
                        name, ext = os.path.splitext(original_name)
                        flat_name = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    out_zip.writestr(flat_name, file_data)

            flat_zip.seek(0)
            st.success(f"Flattened {len(image_files)} image(s).")
            st.download_button("⬇️ Download Flattened ZIP", data=flat_zip, file_name="flattened_images.zip", mime="application/zip")

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io
import zipfile

# --- UI Setup ---
st.set_page_config(page_title="Certificate Generator", page_icon="🎓", layout="wide")
st.title("🎓 Bulk Certificate Generator")
st.markdown("Upload your template, font, and names list to instantly generate certificates.")
st.divider()

# --- 1. File Uploaders ---
st.header("1. Upload Your Files")
col1, col2, col3 = st.columns(3)

with col1:
    template_file = st.file_uploader("Template Image (.png, .jpg)", type=["png", "jpg", "jpeg"])
with col2:
    csv_file = st.file_uploader("Names List (.csv)", type=["csv"])
    st.caption("Ensure your CSV has a column header named 'Name'")
with col3:
    font_file = st.file_uploader("Font File (.ttf)", type=["ttf"])

st.divider()

# --- 2. Configuration Settings ---
st.header("2. Adjust Settings")
col4, col5, col6, col7 = st.columns(4)

with col4:
    y_coordinate = st.number_input("Y-Coordinate (Vertical)", value=846)
with col5:
    font_size = st.number_input("Font Size", value=55)
with col6:
    extra_spaces = st.number_input("Extra Space Between Words", value=2, min_value=1)
with col7:
    font_color = st.color_picker("Text Color", "#000000")

st.divider()

# --- Helper Function for Drawing ---
# --- Helper Function for Drawing ---
def create_certificate(template, font_bytes, name_text, y_pos, size, spaces, color):
    # REWIND THE FILES: This fixes the "cannot open resource" error
    template.seek(0)
    font_bytes.seek(0)

    # Apply extra spaces
    space_multiplier = " " * int(spaces)
    spaced_name = name_text.replace(" ", space_multiplier)

    # Open image and setup drawing
    img = Image.open(template)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_bytes, int(size))

    # Calculate centering
    bbox = draw.textbbox((0, 0), spaced_name, font=font)
    text_width = bbox[2] - bbox[0]
    x_coordinate = (img.width - text_width) / 2

    # Draw text
    draw.text((x_coordinate, y_pos), spaced_name, font=font, fill=color)
    return img

# --- 3. Live Preview & Generation ---
if template_file and csv_file and font_file:
    
    # Read the CSV file
    try:
        df = pd.read_csv(csv_file)
        if "Name" not in df.columns:
            st.error("⚠️ Your CSV file must have a column header exactly named 'Name'.")
            st.stop()
        
        names_list = df["Name"].dropna().astype(str).tolist()
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    # --- Live Preview Section ---
    st.header("3. Live Preview")
    st.write(f"Previewing with the first name from your list: **{names_list[0]}**")
    
    try:
        preview_img = create_certificate(
            template_file, font_file, names_list[0], 
            y_coordinate, font_size, extra_spaces, font_color
        )
        # Show the preview image at a smaller width so it fits nicely on screen
        st.image(preview_img, caption="Live Preview", use_container_width=True)
    except Exception as e:
        st.error(f"Error generating preview: {e}")
        st.stop()

    st.divider()

    # --- Generation Section ---
    st.header("4. Generate & Download")
    st.write(f"Ready to generate **{len(names_list)}** certificates.")

    if st.button("Generate All Certificates", type="primary"):
        with st.spinner("Generating your certificates..."):
            try:
                # Create an in-memory ZIP file
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for original_name in names_list:
                        
                        # Generate the image
                        img = create_certificate(
                            template_file, font_file, original_name, 
                            y_coordinate, font_size, extra_spaces, font_color
                        )

                        # Convert image to bytes to save into the ZIP
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format="PNG")
                        
                        # Clean filename
                        clean_filename = "".join([c for c in original_name if c.isalpha() or c.isdigit() or c==' ']).strip()
                        clean_filename = clean_filename.replace(' ', '_') + ".png"
                        
                        # Add to zip
                        zip_file.writestr(clean_filename, img_bytes.getvalue())

                st.success("✅ Generation complete!")
                
                # Download Button
                st.download_button(
                    label="⬇️ Download Certificates (.zip)",
                    data=zip_buffer.getvalue(),
                    file_name="Ready_Certificates.zip",
                    mime="application/zip"
                )

            except Exception as e:
                st.error(f"An error occurred during generation: {e}")

else:
    st.info("👆 Please upload your Template, CSV, and Font file at the top to see the Live Preview.")
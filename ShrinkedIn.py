import streamlit as st #excuse my bhailang style documentation and commenting things out
from PIL import Image
import io

st.set_page_config(page_title="ShrinkedIn", page_icon="1705508817304.ico", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" ShrinkedIn")
st.caption("Compress and resize your images easily without losing much quality.")

uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    original_size = uploaded_file.size / 1024  # in KB
    original_width, original_height = image.size

    st.subheader("Original Image:")
    st.image(image, use_container_width=True)

    st.subheader("⚙️ Settings")

    # resize karne hetu
    resize_option = st.checkbox("🔄 Resize Image?")
    if resize_option:
        new_width = st.slider("New Width (px)", min_value=50, max_value=original_width, value=original_width)
        new_height = st.slider("New Height (px)", min_value=50, max_value=original_height, value=original_height)
    else:
        new_width, new_height = original_width, original_height

    # compress krne hetu
    quality = st.slider("Select Compression Quality (%)", min_value=1, max_value=100, value=70)
    file_format = st.selectbox("Select Output Format", ("JPEG", "PNG"))

    if st.button("🚀 Compress and Resize Image"):
        with st.spinner('Processing...'):
            buffer = io.BytesIO()

            # idhr resize aur compress sath ho rha button click krne pe
            resized_image = image.resize((new_width, new_height))

            if file_format == "PNG":
                resized_image.save(buffer, format="PNG", optimize=True)
            else:
                resized_image = resized_image.convert("RGB")
                resized_image.save(buffer, format="JPEG", quality=quality)

            buffer.seek(0)
            compressed_size = buffer.getbuffer().nbytes / 1024  # in KB

        st.success("✅ Done!")

        st.subheader("Result Image:")
        st.image(buffer, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Size", f"{original_size:.2f} KB")
        with col2:
            st.metric("Compressed Size", f"{compressed_size:.2f} KB")

        st.download_button(
            label="⬇️ Download Image",
            data=buffer,
            file_name=f"processed_image.{file_format.lower()}",
            mime=f"image/{file_format.lower()}"
        )

else:
    st.info("👆 Upload an image file to get started!") #jabtak kuch nhi run hoga ye dikhega

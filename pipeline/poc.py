# pipeline_streamlit.py
import os
import json
import re
import torch
import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
from ocr import run_ocr  # updated to accept file paths
from transformers import AutoTokenizer, LongT5ForConditionalGeneration
from repair import repair_output
from dotenv import load_dotenv
load_dotenv()

# Load API key from environment
MODEL_DIR = os.getenv("MODEL_DIR")
if not MODEL_DIR:
    raise ValueError("Please set the path to the Model Weights.")


# ------------------------------
# Configuration
# ------------------------------
SAVE_DIR = os.getenv("SAVE_DIR")
os.makedirs(SAVE_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ------------------------------
# Load tokenizer + model (once)
# ------------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = LongT5ForConditionalGeneration.from_pretrained(MODEL_DIR).to(device)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("POC: Image → Nutritional Information in code")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)

    # --------------------------
    # Rotation controls
    # --------------------------
    if "rotation" not in st.session_state:
        st.session_state.rotation = 0

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("↺ Rotate Left"):
            st.session_state.rotation = (st.session_state.rotation - 90) % 360
    with col2:
        if st.button("↻ Rotate Right"):
            st.session_state.rotation = (st.session_state.rotation + 90) % 360
    with col3:
        if st.button("⟳ Reset"):
            st.session_state.rotation = 0

    rotated_img = img.rotate(st.session_state.rotation, expand=True)
    # st.image(rotated_img, caption=f"Rotated {st.session_state.rotation}°", width=400)

    # --------------------------
    # Crop after rotation
    # --------------------------
    cropped_img = st_cropper(rotated_img, aspect_ratio=None)
    st.image(cropped_img, caption="Cropped Image", width=400)

    # --------------------------
    # Barcode input
    # --------------------------
    barcode = st.text_input("Enter barcode (digits only, max 13 digits)")

    # --------------------------
    # Run model
    # --------------------------
    if st.button("Run Model"):
        if not barcode.isdigit() or len(barcode) > 13:
            st.error("❌ Invalid barcode: must be ≤13 digits.")
        else:
            # Save cropped image
            filename = f"{barcode}.jpg"
            save_path = os.path.join(SAVE_DIR, filename)
            cropped_img.save(save_path, format="JPEG")

            # Run OCR
            ocr_output = run_ocr(save_path)

            # Model inference
            st.info("🤖 Running model...")
            input_text = json.dumps(ocr_output, separators=(",", ":"))
            inputs = tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=False
            ).to(device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=2048,
                    num_beams=4,
                    early_stopping=True
                )

            decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Repair JSON
            repaired = repair_output(decoded)
            st.subheader("Model Output (v1.0 of training)")
            st.json(repaired)

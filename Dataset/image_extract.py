import pandas as pd
import requests
import os
import numpy as np
from PIL import Image
from io import BytesIO

# Ask for offset and number of images
offset = int(input("Enter the starting index (offset): "))
num_images = int(input("Enter the number of images to extract: "))

# Load the dataset
df = pd.read_parquet(r"D:\Projects\Calories\nutrition_tables.parquet")

save_path = r"D:\Projects\Calories\Dataset\Images"
os.makedirs(save_path, exist_ok=True)

def get_pixel_coordinates(bbox, width, height):
    """Convert normalized bbox coordinates to pixel coordinates"""
    if isinstance(bbox, np.ndarray):
        if bbox.size == 1:
            bbox = bbox[0]
        coords = bbox.astype(float)
    elif isinstance(bbox, list):
        coords = np.array(bbox, dtype=float)
    else:
        raise ValueError(f"Unknown bbox format: {type(bbox)}")

    if len(coords) != 4:
        raise ValueError(f"Expected 4 coordinates, got {len(coords)}")

    y_min, x_min, y_max, x_max = coords
    return (
        int(x_min * width),
        int(y_min * height),
        int(x_max * width),
        int(y_max * height)
    )

for i in range(offset, offset + num_images):
    try:
        # Get data
        url = df['meta'].iloc[i]['image_url']
        barcode = df['meta'].iloc[i]['barcode']
        box = df['objects'].iloc[i]['bbox']
        print(f"Processing index {i}: {url}")

        # Download image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert('RGB')
        width, height = img.size

        # Get pixel coordinates
        left, top, right, bottom = get_pixel_coordinates(box, width, height)

        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)

        # Crop and save
        cropped_img = img.crop((left, top, right, bottom))
        file_path = os.path.join(save_path, f"{barcode}.jpg")
        cropped_img.save(file_path, "JPEG", quality=95)
        print(f"Saved cropped image: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image at index {i}: {e}")
    except Exception as e:
        print(f"Error processing image at index {i}: {e}")
        print(f"Problematic bbox: {box if 'box' in locals() else 'N/A'}")

import os
import json
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Paths
input_dir = r"D:\Projects\Calories\Dataset\Images"          # Path to the input images
output_dir = r"D:\Projects\Calories\OCR\DocTR_Output_CLEAN" # Path to save cleaned OCR results

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Initialize the OCR model
model = ocr_predictor(pretrained=True)

def clean_ocr_result(result_dict):
    """Remove unwanted fields from OCR output."""
    for page in result_dict.get("pages", []):
        page.pop("confidence", None)
        page.pop("geometry", None)
        page.pop("objectness_score", None)
        for block in page.get("blocks", []):
            for line in block.get("lines", []):
                line.pop("confidence", None)
                line.pop("geometry", None)
                line.pop("objectness_score", None)
                for word in line.get("words", []):
                    word.pop("confidence", None)
                    word.pop("geometry", None)
                    word.pop("objectness_score", None)
                    word.pop("crop_orientation", None)
    return result_dict

def save_json(result_dict, json_path):
    """Save OCR result as JSON."""
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)

def process_images(input_dir, output_dir):
    """Run OCR, clean results, and save JSON."""
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    for img_file in image_files:
        img_path = os.path.join(input_dir, img_file)
        json_path = os.path.join(output_dir, f"{os.path.splitext(img_file)[0]}.json")
        
        try:
            # Load and run OCR
            img_doc = DocumentFile.from_images(img_path)
            result = model(img_doc)
            result_dict = result.export()
            
            # Clean unwanted fields
            cleaned_result = clean_ocr_result(result_dict)
            
            # Save cleaned JSON
            save_json(cleaned_result, json_path)
            
            print(f"Processed {img_file} -> JSON saved: {json_path}")
        
        except Exception as e:
            print(f"Error processing {img_file}: {str(e)}")

# Run everything
process_images(input_dir, output_dir)
print("OCR processing + cleaning + JSON saving completed!")

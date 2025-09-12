import json
import gzip
import os
import requests
from tqdm import tqdm

SAVE_DIRECTORY = r"PATH_TO_SAVE_DIRECTORY"

def get_user_limit():
    """Get processing limit from user input."""
    while True:
        try:
            limit = input("Enter maximum number of barcodes to process (or press Enter for no limit): ")
            if not limit.strip():
                return None
            limit = int(limit)
            if limit > 0:
                return limit
            print("Please enter a positive number or press Enter for no limit")
        except ValueError:
            print("Please enter a valid number")

def read_barcodes_from_jsonl(jsonl_path, barcode_key="code", limit=None):
    """Read barcodes from a gzipped JSONL file with optional limit."""
    barcodes = []
    with gzip.open(jsonl_path, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and len(barcodes) >= limit:
                break
            try:
                item = json.loads(line)
                if barcode := item.get(barcode_key):
                    barcodes.append(str(barcode))
            except json.JSONDecodeError:
                continue
    return barcodes

def download_image(url, barcode, save_dir=SAVE_DIRECTORY):
    """Download an image from a URL and save it with the barcode as filename."""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Determine file extension
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            extension = url[url.rfind('.'):]
        else:
            content_type = response.headers.get('content-type')
            if 'image/jpeg' in content_type:
                extension = '.jpg'
            elif 'image/png' in content_type:
                extension = '.png'
            else:
                extension = '.jpg'  # default
        
        filename = f"{save_dir}/{barcode}{extension}"
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        return filename
    except Exception as e:
        print(f"❌ Failed to download image for {barcode}: {e}")
        return None

def process_barcodes(barcodes, max_workers=5):
    """Process barcodes into 3 categories: valid, invalid (no image), dead (no product)."""
    valid_barcodes = []
    invalid_barcodes = []    # Product exists, but no nutrition image
    dead_barcodes = []       # Product does not exist (HTTP 404)
    downloaded_count = 0
    
    for barcode in tqdm(barcodes, desc="Processing barcodes"):
        api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            resp = requests.get(api_url, timeout=10)
            
            # Case 1: Product does not exist (HTTP 404)
            if resp.status_code == 404:
                dead_barcodes.append(barcode)
                print(f"❌ Product does not exist: {barcode}")
                continue
                
            resp.raise_for_status()
            data = resp.json()
            product = data.get("product", {})

            # Case 2: Check for nutrition image
            nutrition_images = (
                product.get("selected_images", {})
                .get("nutrition", {})
                .get("display", {})
            )
            nutrition_url = nutrition_images.get("en") or nutrition_images.get("fr")

            if nutrition_url:
                valid_barcodes.append(barcode)
                # Download the image
                if download_image(nutrition_url, barcode):
                    downloaded_count += 1
            else:
                invalid_barcodes.append(barcode)
                print(f"⚠️ No nutrition image for {barcode}")

        except Exception as e:
            print(f"❌ Error processing {barcode}: {e}")
            dead_barcodes.append(barcode)  # Treat API errors as dead barcodes
    
    return valid_barcodes, invalid_barcodes, dead_barcodes, downloaded_count

def save_barcodes(barcodes, filename):
    """Save barcodes to a text file."""
    with open(filename, 'w') as f:
        for barcode in barcodes:
            f.write(f"{barcode}\n")
    print(f"\n✅ Saved {len(barcodes)} barcodes to {filename}")

def main():
    jsonl_file_path = "openfoodfacts-products.jsonl.gz"
    print("🚀 Starting barcode processing pipeline...")
    
    # Ask user for limit
    limit = get_user_limit()
    
    # Step 1: Read barcodes (with limit)
    barcodes = read_barcodes_from_jsonl(jsonl_file_path, limit=limit)
    print(f"🔢 Found {len(barcodes)} barcodes to process")
    
    # Step 2: Process and categorize barcodes
    valid_barcodes, invalid_barcodes, dead_barcodes, downloaded_count = process_barcodes(barcodes)
    
    # Step 3: Save all three categories
    save_barcodes(valid_barcodes, "Valid_barcodes.txt")
    save_barcodes(invalid_barcodes, "No_nutrition_image.txt")
    save_barcodes(dead_barcodes, "Nonexistent_barcodes.txt")
    
    # Final summary
    print("\n📊 Final Summary:")
    print(f"✅ Valid barcodes (with nutrition images): {len(valid_barcodes)}")
    print(f"   - Successfully downloaded images: {downloaded_count}")
    print(f"⚠️ Invalid barcodes (exists but no image): {len(invalid_barcodes)}")
    print(f"❌ Dead barcodes (product does not exist): {len(dead_barcodes)}")

if __name__ == "__main__":
    main()
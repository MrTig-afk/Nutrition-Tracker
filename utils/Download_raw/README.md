# Nutritional Images Dataset Creator

This folder contains scripts to create your own dataset of nutritional label images sourced from [Open Food Facts](https://world.openfoodfacts.org).

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Required packages: `requests`, `tqdm`

### Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install requests tqdm
   ```

## 📂 Data Preparation
Before running the code:
1. Download the latest `openfoodfacts-products.jsonl.gz` file from:
   [https://world.openfoodfacts.org/data](https://world.openfoodfacts.org/data)
2. Place the file in the project directory

## ⚙️ Configuration
Set your save directory in the script:
```python
SAVE_DIRECTORY = "your/custom/path/here"  # Replace with your desired save path
```

## 🏃 Running the Script
Execute the main script:
```bash
python barcodes.py
```

The script will:
1. Ask how many barcodes to process (or press Enter for all)
2. Categorize barcodes into:
   - ✅ Valid (has nutrition image)
   - ⚠️ Invalid (exists but no image)
   - ❌ Dead (product doesn't exist)
3. Save images and generate three text files:
   - `Valid_barcodes.txt`
   - `No_nutrition_image.txt`
   - `Nonexistent_barcodes.txt`

## 📊 Output Structure
```
project_folder/
├── Valid_barcodes.txt        # Barcodes with nutrition images
├── No_nutrition_image.txt    # Products without nutrition images
└── Nonexistent_barcodes.txt  # Non-existent product barcodes
```

## ⏱️ Performance Notes
- Processing speed depends on your internet connection
- The script includes error handling and retry logic
- Progress is shown with a tqdm progress bar

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
```
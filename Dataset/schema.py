import os
import json
import requests

# CONFIGURATION — update if needed
INPUT_FOLDER = r"D:\Projects\Calories\OCR\OCR_Clean"
OUTPUT_FOLDER = r"D:\Projects\Calories\Dataset\Training_output_schema"
API_PASS_FILE = os.path.join(OUTPUT_FOLDER, "api_pass.txt")
API_FAIL_FILE = os.path.join(OUTPUT_FOLDER, "api_fail.txt")

# Updated OpenRouter API key and free-tier model
API_KEY = "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"
MODEL = "openai/gpt-oss-20b:free"

PROMPT_TEMPLATE = """
You are a nutrition extraction assistant. You are given text from an OCR scan of a nutrition label. Your task is to **populate the following JSON schema** with the correct values extracted from the text.  

- All numeric values for calories must be numbers or null if missing.  
- All other values (protein, fats, carbs, fiber, cholesterol, sodium) should be strings including units as found in the text (e.g., "7g", "0mg").  
- If a value is missing in the text, leave it as "" for strings or null for calories.  
- Do not invent values. Only extract what is in the text.  
- Maintain the JSON structure exactly as shown.

JSON Schema:
{
  "nutritional_information": {
    "serving_size": "",
    "per_serving": {
      "calories": null,
      "protein": "",
      "saturated_fat": "",
      "trans_fat": "",
      "carbohydrate": "",
      "fiber": "",
      "cholesterol": "",
      "sodium": ""
    },
    "per_100g": {
      "calories": null,
      "protein": "",
      "saturated_fat": "",
      "trans_fat": "",
      "carbohydrate": ""
    }
  }
}

OCR Text:
<<<INSERT YOUR OCR TEXT HERE>>>

Return only the populated JSON. Do not add extra commentary.
"""

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def read_passed_files():
    if not os.path.exists(API_PASS_FILE):
        return set()
    with open(API_PASS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def log_result(filename, status):
    log_file = API_PASS_FILE if status == "pass" else API_FAIL_FILE
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(filename + "\n")

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise and strict JSON parser."},
            {"role": "user", "content": PROMPT_TEMPLATE.replace("<<<INSERT YOUR OCR TEXT HERE>>>", file_content)}
        ],
        "max_tokens": 20000
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"], True
    except Exception as e:
        return str(e), False

def main():
    passed_files = read_passed_files()

    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)

        if not os.path.isfile(file_path) or not filename.endswith('.json'):
            continue
        if filename in passed_files:
            print(f"Skipping already processed (passed) file: {filename}")
            continue

        print(f"Processing {filename}...")
        output_text, success = process_file(file_path)

        if success:
            try:
                output_path = os.path.join(
                    OUTPUT_FOLDER,
                    os.path.splitext(filename)[0] + ".json"
                )
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(output_text)
                print(f"Saved: {output_path}")
                log_result(filename, "pass")
            except Exception as e:
                print(f"Failed to save output for {filename}: {e}")
                log_result(filename, "fail")
        else:
            print(f"API call failed for {filename}: {output_text}")
            log_result(filename, "fail")

if __name__ == "__main__":
    main()

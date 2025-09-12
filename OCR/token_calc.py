import os
import json
import tiktoken

folder_path = r"D:\Projects\Calories\Dataset\OCR_Clean"

encoding = tiktoken.get_encoding("cl100k_base")

token_counts = []

for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = json.dumps(data, ensure_ascii=False)
            tokens = encoding.encode(text)
            count = len(tokens)
            token_counts.append(count)
            print(f"{filename}: {count} tokens")

if token_counts:
    avg_tokens = sum(token_counts) / len(token_counts)
    max_tokens = max(token_counts)
    min_tokens = min(token_counts)

    print("\nSummary:")
    print(f"Processed {len(token_counts)} JSON files")
    print(f"Average token count: {avg_tokens:.2f}")
    print(f"Highest token count: {max_tokens}")
    print(f"Lowest token count: {min_tokens}")
else:
    print("No JSON files found in the folder.")

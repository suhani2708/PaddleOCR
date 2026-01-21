# test_data.py
import sys
import os

# 🔥 CRITICAL: Remove current directory from Python path to avoid loading local paddleocr source
if "" in sys.path:
    sys.path.remove("")
if "." in sys.path:
    sys.path.remove(".")
if os.getcwd() in sys.path:
    sys.path.remove(os.getcwd())

# Now import from installed package (not local source)
import logging
logging.getLogger("ppocr").setLevel(logging.ERROR)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PaddleOCR
import csv
from pathlib import Path

img_path = "/workspaces/PaddleOCR/docs/images/Statista-FormF-RKJJ-NA-1929751_d.jpg"

if not os.path.isfile(img_path):
    raise FileNotFoundError(f"Image not found: {img_path}")

# ✅ Only Text + Confidence (2 decimals)
ocr = PaddleOCR(lang='en', use_angle_cls=False, show_log=False)
result = ocr.ocr(img_path, cls=False)

csv_file = f"{Path(img_path).stem}_output.csv"

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Text", "Confidence"])
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            confidence = line[1][1]
            if text.strip():
                writer.writerow([text, f"{confidence:.2f}"])
                print(f"Text: '{text}' | Confidence: {confidence:.2f}")
    else:
        print("No text detected.")
        writer.writerow(["No text detected", ""])

print(f"\n✅ Output saved to: {csv_file}")
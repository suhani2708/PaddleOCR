
import sys
import os
import csv
import logging

# --- Clean sys.path (avoid local import conflicts) ---
for p in ["", ".", os.getcwd()]:
    if p in sys.path:
        sys.path.remove(p)

# --- Environment fixes ---
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

# --- Reduce PaddleOCR logs ---
logging.getLogger("ppocr").setLevel(logging.ERROR)

from paddleocr import PaddleOCR

# --- Image path ---
img_path = "/workspaces/PaddleOCR/docs/images/Statista-FormF-RKJJ-NA-1929751_d.jpg"

if not os.path.isfile(img_path):
    raise FileNotFoundError(f"Image not found: {img_path}")

# --- OCR init ---
ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False,
    show_log=False
)

# --- Run OCR ---
result = ocr.ocr(img_path, cls=False)

# --- Settings ---
csv_file = "output.csv"
CONFIDENCE_THRESHOLD = 1.00  # Highlight below 90%

detections = []

# --- Normalize PaddleOCR output ---
if result:
    if isinstance(result, list) and len(result) == 1 and isinstance(result[0], list):
        items = result[0]
    else:
        items = result

    for item in items:
        if not item or len(item) < 2:
            continue

        text_info = item[1]

        if (
            isinstance(text_info, (list, tuple))
            and len(text_info) >= 2
        ):
            try:
                text = str(text_info[0]).strip()
                confidence = float(text_info[1])

                if text:
                    detections.append((text, confidence))

            except (ValueError, TypeError):
                continue

# --- Write CSV with Low_Confidence flag ---
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Header
    writer.writerow(["Text", "Confidence", "Low_Confidence"])

    if not detections:
        print("❌ No text detected")
        writer.writerow(["No text detected", "", ""])
    else:
        for text, confidence in detections:
            # ✅ Add flag for Excel conditional formatting
            low_flag = "YES" if confidence < CONFIDENCE_THRESHOLD else "NO"
            writer.writerow([text, f"{confidence:.2f}", low_flag])
            print(f"Text: '{text}' | Confidence: {confidence:.2f} | Low: {low_flag}")

print(f"\n✅ CSV saved successfully: {csv_file}")
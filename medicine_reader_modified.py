import argparse
import cv2 as cv
import pytesseract
from rapidfuzz import fuzz
import re

# Where Tesseract is installed.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

medicines = [
    "Paracetamol 500mg",
    "Ibuprofen 200mg",
    "Amoxicillin 250mg",
    "Aspirin 75mg"
]

# Common OCR mistakes mapped to intended medicine tokens.
OCR_TOKEN_CORRECTIONS = {
    "tbuprofen": "ibuprofen",
    "ibuprofenn": "ibuprofen",
    "amoxicilin": "amoxicillin",
    "paracemeter": "paracetamol",
    "asprin": "aspirin",
}


def build_medicine_db(medicine_list):
    """Split each medicine entry into normalized name and optional dosage."""
    db = []
    for item in medicine_list:
        lowered = item.lower().strip()
        dose_match = re.search(r'(\d+\s*mg)', lowered)
        dose = dose_match.group(1).replace(" ", "") if dose_match else ""
        name = re.sub(r'\d+\s*mg', '', lowered).strip()
        db.append({
            "full": lowered,
            "name": name,
            "dose": dose,
            "display": item,
        })
    return db


MEDICINE_DB = build_medicine_db(medicines)


def load_image(image_path):
    image = cv.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        return None

    print("Image loaded successfully")
    return image


def preprocess_variants(image):
    # Generate multiple binarized views; OCR quality varies by image.
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    upscaled = cv.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv.INTER_CUBIC)

    # CLAHE improves local contrast for faded/blurry print.
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrasted = clahe.apply(upscaled)

    blur = cv.GaussianBlur(contrasted, (5, 5), 0)
    _, otsu = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    adaptive = cv.adaptiveThreshold(
        contrasted,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        35,
        9,
    )

    print("Generated OCR variants (OTSU and adaptive)")
    return [
        ("otsu", otsu),
        ("adaptive", adaptive),
    ]


def clean_ocr_text(raw_text):
    # Keep digits too, because dosage like 200mg is useful for final ranking.
    letters_only = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_text)
    return ' '.join(word for word in letters_only.split() if len(word) >= 3)


def normalize_ocr_text(text):
    """Lowercase, normalize spacing, and repair common OCR token errors."""
    normalized = text.lower()
    normalized = re.sub(r'\bmg\b', ' mg ', normalized)
    normalized = normalized.replace('-', ' ')
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    words = normalized.split()
    fixed_words = [OCR_TOKEN_CORRECTIONS.get(w, w) for w in words]
    return ' '.join(fixed_words)


def score_medicine_candidate(normalized_text, medicine):
    """Blend name match + full-text match + dosage bonus into one score."""
    name_score = fuzz.token_set_ratio(normalized_text, medicine['name'])
    partial_name_score = fuzz.partial_ratio(normalized_text, medicine['name'])
    full_score = fuzz.token_set_ratio(normalized_text, medicine['full'])

    compact_text = normalized_text.replace(" ", "")
    dose_bonus = 8.0 if medicine['dose'] and medicine['dose'] in compact_text else 0.0

    # Prefer medicines that appear explicitly and earlier in OCR text.
    contains_name_bonus = 5.0 if medicine['name'] in normalized_text else 0.0
    starts_with_bonus = 10.0 if normalized_text.startswith(medicine['name']) else 0.0

    composite = (
        (0.5 * name_score)
        + (0.35 * partial_name_score)
        + (0.15 * full_score)
        + dose_bonus
        + contains_name_bonus
        + starts_with_bonus
    )
    return min(composite, 100.0)


def rank_medicines(normalized_text, medicine_db):
    """Return medicines ordered by descending confidence score."""
    ranked = []
    for med in medicine_db:
        ranked.append({
            "medicine": med,
            "score": score_medicine_candidate(normalized_text, med),
        })
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked


def extract_best_ocr_text(variants, medicine_db):
    best_result = None
    best_score = -1.0

    for variant_name, variant_img in variants:
        for psm in (6, 7):
            try:
                raw_text = pytesseract.image_to_string(
                    variant_img,
                    config=f'--oem 3 --psm {psm}',
                    timeout=6,
                )
            except RuntimeError:
                # Skip OCR attempts that exceed timeout.
                continue

            cleaned_text = clean_ocr_text(raw_text)

            if not cleaned_text.strip():
                continue

            normalized_text = normalize_ocr_text(cleaned_text)
            ranked = rank_medicines(normalized_text, medicine_db)
            top = ranked[0]
            score = top['score']

            if score > best_score:
                best_score = score
                best_result = {
                    'variant': variant_name,
                    'psm': psm,
                    'raw_text': raw_text,
                    'cleaned_text': cleaned_text,
                    'normalized_text': normalized_text,
                    'ranked': ranked,
                }

    if best_result is None:
        return None

    print(f"Best OCR variant: {best_result['variant']} with PSM {best_result['psm']}")
    print("Raw OCR Output:  ", best_result['raw_text'])
    print("Cleaned Output:  ", best_result['cleaned_text'])
    print("Normalized Text: ", best_result['normalized_text'])
    return best_result


def match_medicine(best_result, threshold=70):
    if best_result is None:
        print("No readable text found from OCR")
        return None

    ranked = best_result['ranked']
    if not ranked:
        print("Medicine not recognized - please try again")
        return None

    top = ranked[0]
    second_score = ranked[1]['score'] if len(ranked) > 1 else 0.0
    margin = top['score'] - second_score

    # Require both minimum score and a minimum gap from runner-up.
    if top['score'] >= threshold and margin >= 1.5:
        print("Medicine Found: ", top['medicine']['display'])
        print("Confidence:    ", round(top['score'], 2), "%")
        return top

    print("Top Suggestions:")
    for item in ranked[:3]:
        print(f"- {item['medicine']['display']}: {item['score']:.2f}%")

    print("Medicine not recognized - please try again")
    return None


def main(image_path='medicine.jpg', threshold=70):
    image = load_image(image_path)
    if image is None:
        return

    variants = preprocess_variants(image)
    best_result = extract_best_ocr_text(variants, MEDICINE_DB)
    match_medicine(best_result, threshold=threshold)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OCR medicine name from an image')
    parser.add_argument(
        'image',
        nargs='?',
        default='medicine.jpg',
        help='Image filename or path (default: medicine.jpg)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=70,
        help='Minimum match confidence (default: 70)'
    )
    args = parser.parse_args()
    main(args.image, threshold=args.threshold)

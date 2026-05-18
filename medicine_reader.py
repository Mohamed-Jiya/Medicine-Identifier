# import cv2 as cv
# import pytesseract
# from rapidfuzz import process, fuzz 
# import re

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Load the medicine image
# image = cv.imread('medi_amox.jpg')

# if image is None:
#     print("Image not found — check the filename!")
# else:
#     print("Image loaded successfully")
    
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     print("Image converted to grayscale")
    
#     blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
#     print("Noise removed")
    
#     _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)
#     print("Image sharpened and ready")
    
#     raw_text = pytesseract.image_to_string(clean, config='--psm 6')
    
#     letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)
#     cleaned_text = ' '.join(word for word in letters_only.split() if len(word) >= 3)
    
#     print("Raw OCR Output:  ", raw_text)
#     print("Cleaned Output:  ", cleaned_text)

#     # medicine database list — now INSIDE else block
#     medicines = [
#         "Paracetamol 500mg",
#         "Ibuprofen 200mg",
#         "Amoxicillin 250mg",
#         "Aspirin 75mg"
#     ]

#     # safety check — if OCR found nothing, stop early
#     if not cleaned_text:
#         print("No text found in image — try a clearer photo!")
#     else:
#         best_match = process.extractOne(cleaned_text, medicines, scorer=fuzz.partial_ratio)

#         if best_match[1] >= 70:
#             print("Medicine Found: ", best_match[0])
#             print("Confidence:     ", round(best_match[1], 2), "%")
#         else:
#             print("Medicine not recognized — please try again")



import cv2 as cv
import pytesseract
from rapidfuzz import process, fuzz
import re

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# =========================================
# OCR FUNCTION
# =========================================

def detect_medicine(image_path):

    # Load image
    image = cv.imread(image_path)

    if image is None:
        return None

    # Convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Remove noise
    blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)

    # Threshold
    _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)

    # OCR Read
    raw_text = pytesseract.image_to_string(
        clean,
        config='--psm 6'
    )

    # Clean text
    letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)

    cleaned_text = ' '.join(
        word for word in letters_only.split()
        if len(word) >= 3
    )

    print("Raw OCR:", raw_text)
    print("Cleaned OCR:", cleaned_text)

    # Medicine list
    medicines = [
        "Paracetamol",
        "Ibuprofen",
        "Amoxicillin",
        "Aspirin",
        "Crocin",
        "Dolo 650",
        "Cetirizine",
        "Azithromycin",
        "Metformin",
        "Pantoprazole"
    ]

    # No text found
    if not cleaned_text:
        return None

    # Fuzzy Match
    best_match = process.extractOne(
        cleaned_text,
        medicines,
        scorer=fuzz.partial_ratio
    )

    print("Best Match:", best_match)

    # Confidence check
    if best_match[1] >= 70:

        medicine_name = best_match[0]

        print("Medicine Found:", medicine_name)

        return medicine_name

    else:

        return None
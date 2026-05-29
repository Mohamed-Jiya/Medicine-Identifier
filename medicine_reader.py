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



# import cv2 as cv
# import pytesseract
# from rapidfuzz import process, fuzz
# import re

# # Tesseract Path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# # =========================================
# # OCR FUNCTION
# # =========================================

# def detect_medicine(image_path):

#     # Load image
#     image = cv.imread(image_path)

#     if image is None:
#         return None

#     # Convert to grayscale
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#     # Remove noise
#     blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)

#     # Threshold
#     _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)

#     # OCR Read
#     raw_text = pytesseract.image_to_string(
#         clean,
#         config='--psm 6'
#     )

#     # Clean text
#     letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)

#     cleaned_text = ' '.join(
#         word for word in letters_only.split()
#         if len(word) >= 3
#     )

#     print("Raw OCR:", raw_text)
#     print("Cleaned OCR:", cleaned_text)

#     # Medicine list
#     medicines = [
#         "Paracetamol",
#         "Ibuprofen",
#         "Amoxicillin",
#         "Aspirin",
#         "Crocin",
#         "Dolo 650",
#         "Cetirizine",
#         "Azithromycin",
#         "Metformin",
#         "Pantoprazole"
#     ]

#     # No text found
#     if not cleaned_text:
#         return None

#     # Fuzzy Match
#     best_match = process.extractOne(
#         cleaned_text,
#         medicines,
#         scorer=fuzz.partial_ratio
#     )

#     print("Best Match:", best_match)

#     # Confidence check
#     if best_match[1] >= 70:

#         medicine_name = best_match[0]

#         print("Medicine Found:", medicine_name)

#         return medicine_name

#     else:

#         return None


import cv2 as cv
import pytesseract
from rapidfuzz import process, fuzz
import re
import sqlite3
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_medicine_names():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def detect_medicine(image_path):

    image = cv.imread(image_path)
    if image is None:
        return None

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    sharpen_kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ])
    sharpened = cv.filter2D(gray, -1, sharpen_kernel)

    blur = cv.GaussianBlur(sharpened, (3, 3), cv.BORDER_DEFAULT)

    _, clean = cv.threshold(
        blur, 0, 255,
        cv.THRESH_BINARY + cv.THRESH_OTSU
    )

    # try multiple OCR modes and pick best result
    raw1 = pytesseract.image_to_string(clean, config='--psm 6')
    raw2 = pytesseract.image_to_string(clean, config='--psm 11')
    raw3 = pytesseract.image_to_string(gray,  config='--psm 6')

    # combine all OCR attempts into one text
    combined_raw = raw1 + " " + raw2 + " " + raw3

    # clean text
    letters_only = re.sub(r'[^a-zA-Z\s]', '', combined_raw)
    cleaned_text = ' '.join(
        word for word in letters_only.split()
        if len(word) >= 3
    )

    print("Cleaned:  ", cleaned_text)

    if not cleaned_text:
        return None

    medicines = get_medicine_names()
    if not medicines:
        return None

    # match each word individually
    words = cleaned_text.split()
    best_overall = None

    for word in words:
        # lowercase both word and medicines for fair comparison
        word_lower = word.lower()
        medicines_lower = [m.lower() for m in medicines]

        m1 = process.extractOne(word_lower, medicines_lower, scorer=fuzz.partial_ratio)
        m2 = process.extractOne(word_lower, medicines_lower, scorer=fuzz.WRatio)
        best_word = max([m1, m2], key=lambda x: x[1])

        if best_overall is None or best_word[1] > best_overall[1]:
            best_overall = best_word
            # keep original medicine name not lowercase version
            best_overall = (medicines[medicines_lower.index(best_word[0])], best_word[1], best_word[2])

    print("Best Match: ", best_overall)

    if best_overall and best_overall[1] >= 60:
        return best_overall[0]
    else:
        return None
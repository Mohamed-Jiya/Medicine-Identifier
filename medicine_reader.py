import cv2 as cv
import pytesseract
from rapidfuzz import process, fuzz 
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the medicine image
image = cv.imread('medi_amox.jpg')

if image is None:
    print("Image not found — check the filename!")
else:
    print("Image loaded successfully")
    
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    print("Image converted to grayscale")
    
    blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
    print("Noise removed")
    
    _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)
    print("Image sharpened and ready")
    
    raw_text = pytesseract.image_to_string(clean, config='--psm 6')
    
    letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)
    cleaned_text = ' '.join(word for word in letters_only.split() if len(word) >= 3)
    
    print("Raw OCR Output:  ", raw_text)
    print("Cleaned Output:  ", cleaned_text)

    # medicine database list — now INSIDE else block
    medicines = [
        "Paracetamol 500mg",
        "Ibuprofen 200mg",
        "Amoxicillin 250mg",
        "Aspirin 75mg"
    ]

    # safety check — if OCR found nothing, stop early
    if not cleaned_text:
        print("No text found in image — try a clearer photo!")
    else:
        best_match = process.extractOne(cleaned_text, medicines, scorer=fuzz.partial_ratio)

        if best_match[1] >= 70:
            print("Medicine Found: ", best_match[0])
            print("Confidence:     ", round(best_match[1], 2), "%")
        else:
            print("Medicine not recognized — please try again")
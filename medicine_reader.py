import cv2 as cv
import pytesseract
from rapidfuzz import process, fuzz 
import re # new import - helps clean text

#where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the medicine image
image = cv.imread('medicine.jpg')

# Check if image was found
if image is None:
    print(" Image not found — check the filename!")
else:
    print("Image loaded successfully")
    
    #remove color
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    print("Image converted to grayscale")
    
    #remove noise
    blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
    print("Noise removed")
    
    # sharpen the text
    _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)
    print("Image sharpened and ready")
    
    # Read text from cleaned image
    raw_text = pytesseract.image_to_string(clean, config='--psm 6')
    
    #     # Remove everything except letters and spaces
    letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)
    
    # Clean up the messy OCR output
    cleaned_text = ' '.join(word for word in letters_only.split() if len(word) >= 3)
    
    print("Raw OCR Output:  ", raw_text)
    print("Cleaned Output:  ", cleaned_text)
    
#medicine database list
medicines = [
    "Paracetamol 500mg",
    "Ibuprofen 200mg",
    "Amoxicillin 250mg",
    #"Paracemeter-500",
    "Aspirin 75mg"
]

# Find the closest match
best_match = process.extractOne(cleaned_text, medicines, scorer=fuzz.partial_ratio)

# Only accept if confidence is 70% or above
if best_match[1] >= 70:
    print("Medicine Found: ", best_match[0])
    print("Confidence:    ", round(best_match[1], 2), "%")
else:
    print("Medicine not recognized — please try again")


    

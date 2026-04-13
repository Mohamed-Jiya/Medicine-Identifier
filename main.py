# ============================================
# MAIN FILE — Connects OCR + Database together
# ============================================

# tools for image reading and cleaning
import cv2 as cv

# tool for reading text from images
import pytesseract

# tool for fuzzy text matching
from rapidfuzz import process, fuzz

# tool for cleaning messy text
import re

# Mazhar's database search function
from database import search_medicine


# ============================================
# SETUP — tell Python where Tesseract is
# ============================================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# ============================================
# STEP 1 — Load the image
# ============================================
image = cv.imread('medi_amox.jpg')

if image is None:
    print("Image not found — check the filename!")

else:
    print("Image loaded successfully")

    # ============================================
    # STEP 2 — Clean the image for better OCR
    # ============================================

    # remove color — black and white is easier to read
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # remove background noise and speckles
    blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)

    # make text pure black and background pure white
    _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)

    print("Image cleaned and ready")


    # ============================================
    # STEP 3 — Read text from the cleaned image
    # psm 6 means: treat image as a block of text
    # ============================================
    raw_text = pytesseract.image_to_string(clean, config='--psm 6')

    # remove everything except letters and spaces
    letters_only = re.sub(r'[^a-zA-Z\s]', '', raw_text)

    # remove short junk words (less than 3 letters)
    cleaned_text = ' '.join(word for word in letters_only.split() if len(word) >= 3)

    print("OCR Read: ", cleaned_text)


    # ============================================
    # STEP 4 — Match OCR text to medicine name
    # only 4 medicines for now — more added later
    # ============================================
    medicines = [
        "Paracetamol",
        "Ibuprofen",
        "Amoxicillin",
        "Aspirin"
    ]

    # safety check — if OCR found nothing, stop early
    if not cleaned_text:
        print("No text found — try a clearer photo!")

    else:
        # partial_ratio checks if medicine name is INSIDE the OCR text
        best_match = process.extractOne(
            cleaned_text,
            medicines,
            scorer=fuzz.partial_ratio
        )

        # only trust matches above 70% confidence
        if best_match[1] >= 70:
            matched_name = best_match[0]
            print("Medicine Matched: ", matched_name)
            print("Confidence:       ", round(best_match[1], 2), "%")


            # ============================================
            # STEP 5 — Search Mazhar's database
            # pass the matched name to get full details
            # ============================================
            result = search_medicine(matched_name)

            # ============================================
            # STEP 6 — Show full medicine information
            # ============================================
            if result:
                print("-----------------------------")
                print("Name:         ", result[1])
                print("Use:          ", result[2])
                print("Side Effect:  ", result[3])
                print("Dosage:       ", result[4])
                print("-----------------------------")
            else:
                print("Medicine matched but not found in database!")
                print("Ask Mazhar to add it to the database!")

        else:
            print("Medicine not recognized — please try again")
import cv2 as cv
import pytesseract

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image
img = cv.imread('medicine.jpg')

# Clean the image (same steps as before)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#_, clean = cv.thresholdcv.blurr, 150, 255, cv.THRESH_BINARY)

# 🔤 Read the text from the image!
text = pytesseract.image_to_string(gray)

print("📋 Text found in image:")
print(text)
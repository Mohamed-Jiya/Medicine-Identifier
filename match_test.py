from rapidfuzz import process, fuzz

# 🔤 This is what OCR gave us (messy)
ocr_result = "Paracetamol."

# 👇 Clean it — remove dots, extra spaces, newlines
cleaned = ocr_result.strip().replace(".", "").replace("\n", " ")


# 💊 This is our medicine database (a simple list for now)
medicines = [
    "Paracetamol 500mg",
    "Ibuprofen 200mg",
    "Amoxicillin 250mg",
    "Paracemeter-500",
    "Aspirin 75mg"
]

# 👇 scorer=fuzz.partial_ratio is the key change!
best_match = process.extractOne(cleaned, medicines, scorer=fuzz.partial_ratio)

# 👇 Only accept if confidence is 70% or above
if best_match and best_match[1] >= 70:
    print("💊 Medicine Found:", best_match[0])
    print("📊 Confidence:    ", round(best_match[1], 2), "%")
else:
        print("❌ Medicine not recognized — please try again")


# print("🔍 OCR Read:     ", ocr_result)
# print("🔍 Cleaned Text: ", cleaned)
# print("💊 Best Match:   ", best_match[0])
# print("📊 Confidence:   ", round(best_match[1], 2), "%")




## Expected Output:

# 🔍 OCR Read:      Paracetamol.
# 💊 Best Match:    Paracetamol 500mg
# 📊 Confidence:    90.0 %
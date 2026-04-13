from database import search_medicine

name = input("Enter medicine name: ")
data = search_medicine(name)

if data:
    print("ID:", data[0])
    print("Name:", data[1])
    print("Use:", data[2])
    print("Side Effect:", data[3])
    print("Dosage:", data[4])
else:
    print("Medicine not found")
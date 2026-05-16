print("GUI Started")
import tkinter as tk
from tkinter import filedialog
from database import search_medicine

# Window
root = tk.Tk()
root.title("Medicine Identifier")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# Title
title_label = tk.Label(
    root,
    text="Medicine Identifier App",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0",
    fg="blue"
)

title_label.pack(pady=20)

# Medicine Name Label
name_label = tk.Label(
    root,
    text="Enter Medicine Name",
    font=("Arial", 14),
    bg="#f0f0f0"
)

name_label.pack()

# Entry Box
entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 14)
)

entry.pack(pady=10)

# Result Label
result_label = tk.Label(
    root,
    text="Result will appear here",
    font=("Arial", 12),
    justify="left",
    bg="white",
    width=50,
    height=10,
    anchor="nw",
    relief="solid",
    padx=10,
    pady=10
)

result_label.pack(pady=20)

# Search Function
def search():

    medicine_name = entry.get()

    print("Searching:", medicine_name)

    data = search_medicine(medicine_name)

    print("Database Result:", data)

    if data:

        result_text = f"""
Medicine Found

Name: {data[1]}

Use:
{data[2]}

Side Effects:
{data[3]}

Dosage:
{data[4]}
"""

        result_label.config(text=result_text)

    else:
        result_label.config(text="Medicine not found")

# Search Button
search_button = tk.Button(
    root,
    text="Search Medicine",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    width=20,
    command=search
)

search_button.pack(pady=10)

# Upload Function
def upload_image():

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:
        result_label.config(text=f"Selected Image:\n\n{file_path}")

# Upload Button
upload_button = tk.Button(
    root,
    text="Upload Medicine Image",
    font=("Arial", 12, "bold"),
    bg="blue",
    fg="white",
    width=25,
    command=upload_image
)

upload_button.pack(pady=10)

# Run App
print("Window Running")
root.mainloop()
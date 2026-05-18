from medicine_reader import detect_medicine
# =========================================
# MEDICINE IDENTIFIER - SOFT GREEN UI
# =========================================

import tkinter as tk
from tkinter import filedialog
from database import search_medicine


# =========================================
# MAIN WINDOW
# =========================================

root = tk.Tk()

root.title("Medicine Identifier")

root.geometry("900x700")

root.configure(bg="#E8F5EE")


# =========================================
# TITLE
# =========================================

title = tk.Label(
    root,
    text="🌿 Medicine Identifier",
    font=("Segoe UI", 26, "bold"),
    bg="#E8F5EE",
    fg="#27500A"
)

title.pack(pady=(25, 5))


# =========================================
# SUBTITLE
# =========================================

subtitle = tk.Label(
    root,
    text="Search by name or upload an image to identify a medicine",
    font=("Segoe UI", 11),
    bg="#E8F5EE",
    fg="#5F5E5A"
)

subtitle.pack(pady=(0, 20))


# =========================================
# MAIN CARD
# =========================================

main_frame = tk.Frame(
    root,
    bg="#F0FAF5",
    bd=1,
    relief="solid"
)

main_frame.pack(padx=30, pady=10)


# =========================================
# SEARCH LABEL
# =========================================

search_label = tk.Label(
    main_frame,
    text="Enter Medicine Name",
    font=("Segoe UI", 12, "bold"),
    bg="#F0FAF5",
    fg="#27500A"
)

search_label.pack(anchor="w", padx=25, pady=(25, 8))


# =========================================
# SEARCH FRAME
# =========================================

search_frame = tk.Frame(
    main_frame,
    bg="#F0FAF5"
)

search_frame.pack(padx=25, pady=(0, 20), fill="x")


# =========================================
# ENTRY BOX
# =========================================

entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 13),
    width=35,
    bg="white",
    fg="#333333",
    relief="solid",
    bd=1
)

entry.pack(side="left", ipady=8, padx=(0, 10))


# =========================================
# SEARCH FUNCTION
# =========================================

def search():

    medicine_name = entry.get()

    data = search_medicine(medicine_name)

    result_label.config(state="normal")

    result_label.delete(1.0, tk.END)

    if data:

        result_text = f"""
✅ Medicine Found

💊 Name:
{data[1]}

📌 Use:
{data[2]}

⚠ Side Effects:
{data[3]}

💉 Dosage:
{data[4]}
"""

        result_label.insert(tk.END, result_text)

        status_label.config(
            text="● Medicine Found",
            fg="#3B6D11"
        )

    else:

        result_label.insert(
            tk.END,
            """
⚠ Medicine Not Uploaded Yet

"""
        )

        status_label.config(
            text="● Medicine Not Uploaded Yet",
            fg="#BA7517"
        )

    result_label.config(state="disabled")


# =========================================
# SEARCH BUTTON
# =========================================

search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Segoe UI", 11, "bold"),
    bg="#639922",
    fg="white",
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2",
    command=search
)

search_button.pack(side="left")


# =========================================
# RESULT TITLE
# =========================================

result_title = tk.Label(
    main_frame,
    text="Result",
    font=("Segoe UI", 12, "bold"),
    bg="#F0FAF5",
    fg="#27500A"
)

result_title.pack(anchor="w", padx=25)


# =========================================
# RESULT BOX FRAME
# =========================================

result_box_frame = tk.Frame(
    main_frame,
    bg="#F0FAF5"
)

result_box_frame.pack(padx=25, pady=(8, 20))


# =========================================
# SCROLLBAR
# =========================================

scrollbar = tk.Scrollbar(result_box_frame)

scrollbar.pack(side="right", fill="y")


# =========================================
# RESULT TEXT BOX
# =========================================

result_label = tk.Text(
    result_box_frame,
    font=("Segoe UI", 11),
    bg="white",
    fg="#333333",
    relief="solid",
    bd=1,
    width=65,
    height=16,
    padx=15,
    pady=12,
    wrap="word",
    yscrollcommand=scrollbar.set
)

result_label.pack(side="left")

scrollbar.config(command=result_label.yview)


# =========================================
# DEFAULT TEXT
# =========================================

result_label.insert(
    tk.END,
    "Results will appear here after searching or uploading an image..."
)

result_label.config(state="disabled")


# =========================================
# BUTTON FRAME
# =========================================

button_frame = tk.Frame(
    main_frame,
    bg="#F0FAF5"
)

button_frame.pack(fill="x", padx=25, pady=(0, 20))

# =========================================
# UPLOAD FUNCTION
# =========================================

def upload_image():

    file_path = filedialog.askopenfilename(
        title="Select Medicine Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:

        # OCR detect
        medicine_name = detect_medicine(file_path)

        result_label.config(state="normal")

        result_label.delete(1.0, tk.END)

        # If OCR found medicine
        if medicine_name:

            # Database search
            data = search_medicine(medicine_name)

            if data:

                result_text = f"""
✅ Medicine Found

💊 Name:
{data[1]}

📌 Use:
{data[2]}

⚠ Side Effects:
{data[3]}

💉 Dosage:
{data[4]}
"""

                result_label.insert(tk.END, result_text)

                status_label.config(
                    text="● Medicine Found",
                    fg="#3B6D11"
                )

            else:

                result_label.insert(
                    tk.END,
                    "⚠ Medicine detected but not uploaded in database yet."
                )

        else:

            result_label.insert(
                tk.END,
                """
⚠ Medicine Not Recognized

Please upload a clearer image.
"""
            )

            status_label.config(
                text="● OCR Failed",
                fg="red"
            )

        result_label.config(state="disabled")


# =========================================
# UPLOAD BUTTON
# =========================================

upload_button = tk.Button(
    button_frame,
    text="📷 Upload Medicine Image",
    font=("Segoe UI", 11, "bold"),
    bg="#3B6D11",
    fg="white",
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2",
    command=upload_image
)

upload_button.pack(side="left")


# =========================================
# CLEAR FUNCTION
# =========================================

def clear_data():

    entry.delete(0, tk.END)

    result_label.config(state="normal")

    result_label.delete(1.0, tk.END)

    result_label.insert(
        tk.END,
        "Results will appear here after searching or uploading an image..."
    )

    result_label.config(state="disabled")

    status_label.config(
        text="● Ready",
        fg="#3B6D11"
    )


# =========================================
# CLEAR BUTTON
# =========================================

clear_button = tk.Button(
    button_frame,
    text="✕ Clear",
    font=("Segoe UI", 11, "bold"),
    bg="#888780",
    fg="white",
    relief="flat",
    padx=18,
    pady=8,
    cursor="hand2",
    command=clear_data
)

clear_button.pack(side="right")


# =========================================
# STATUS BAR
# =========================================

status_label = tk.Label(
    root,
    text="● Ready",
    font=("Segoe UI", 10),
    bg="#EAF3DE",
    fg="#3B6D11",
    anchor="w",
    padx=15,
    pady=6
)

status_label.pack(fill="x", padx=40, pady=(10, 0))


# =========================================
# FOOTER
# =========================================

footer = tk.Label(
    root,
    text="Final Year Project · Medicine Identifier",
    font=("Segoe UI", 9),
    bg="#E8F5EE",
    fg="#5F5E5A"
)

footer.pack(pady=15)


# =========================================
# RUN APP
# =========================================

root.mainloop()
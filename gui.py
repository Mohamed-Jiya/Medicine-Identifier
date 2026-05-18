from medicine_reader import detect_medicine
# # =========================================
# # MEDICINE IDENTIFIER - SOFT GREEN UI
# # =========================================

# import tkinter as tk
# from tkinter import filedialog
# from database import search_medicine


# # =========================================
# # MAIN WINDOW
# # =========================================

# root = tk.Tk()

# root.title("Medicine Identifier")

# root.geometry("900x700")

# root.configure(bg="#E8F5EE")


# # =========================================
# # TITLE
# # =========================================

# title = tk.Label(
#     root,
#     text="🌿 Medicine Identifier",
#     font=("Segoe UI", 26, "bold"),
#     bg="#E8F5EE",
#     fg="#27500A"
# )

# title.pack(pady=(25, 5))


# # =========================================
# # SUBTITLE
# # =========================================

# subtitle = tk.Label(
#     root,
#     text="Search by name or upload an image to identify a medicine",
#     font=("Segoe UI", 11),
#     bg="#E8F5EE",
#     fg="#5F5E5A"
# )

# subtitle.pack(pady=(0, 20))


# # =========================================
# # MAIN CARD
# # =========================================

# main_frame = tk.Frame(
#     root,
#     bg="#F0FAF5",
#     bd=1,
#     relief="solid"
# )

# main_frame.pack(padx=30, pady=10)


# # =========================================
# # SEARCH LABEL
# # =========================================

# search_label = tk.Label(
#     main_frame,
#     text="Enter Medicine Name",
#     font=("Segoe UI", 12, "bold"),
#     bg="#F0FAF5",
#     fg="#27500A"
# )

# search_label.pack(anchor="w", padx=25, pady=(25, 8))


# # =========================================
# # SEARCH FRAME
# # =========================================

# search_frame = tk.Frame(
#     main_frame,
#     bg="#F0FAF5"
# )

# search_frame.pack(padx=25, pady=(0, 20), fill="x")


# # =========================================
# # ENTRY BOX
# # =========================================

# entry = tk.Entry(
#     search_frame,
#     font=("Segoe UI", 13),
#     width=35,
#     bg="white",
#     fg="#333333",
#     relief="solid",
#     bd=1
# )

# entry.pack(side="left", ipady=8, padx=(0, 10))


# # =========================================
# # SEARCH FUNCTION
# # =========================================

# def search():

#     medicine_name = entry.get().strip()

#     data = search_medicine(medicine_name)

#     result_label.config(state="normal")

#     result_label.delete(1.0, tk.END)

#     if data:

#         result_text = f"""
# ✅ Medicine Found

# 💊 Name:
# {data[1]}

# 📌 Use:
# {data[2]}

# ⚠ Side Effects:
# {data[3]}

# 💉 Dosage:
# {data[4]}
# """

#         result_label.insert(tk.END, result_text)

#         status_label.config(
#             text="● Medicine Found",
#             fg="#3B6D11"
#         )

#     else:

#         result_label.insert(
#             tk.END,
#             """
# ⚠ Medicine Not Uploaded Yet

# """
#         )

#         status_label.config(
#             text="● Medicine Not Uploaded Yet",
#             fg="#BA7517"
#         )

#     result_label.config(state="disabled")


# # =========================================
# # SEARCH BUTTON
# # =========================================

# search_button = tk.Button(
#     search_frame,
#     text="🔍 Search",
#     font=("Segoe UI", 11, "bold"),
#     bg="#639922",
#     fg="white",
#     relief="flat",
#     padx=18,
#     pady=8,
#     cursor="hand2",
#     command=search
# )

# search_button.pack(side="left")


# # =========================================
# # RESULT TITLE
# # =========================================

# result_title = tk.Label(
#     main_frame,
#     text="Result",
#     font=("Segoe UI", 12, "bold"),
#     bg="#F0FAF5",
#     fg="#27500A"
# )

# result_title.pack(anchor="w", padx=25)


# # =========================================
# # RESULT BOX FRAME
# # =========================================

# result_box_frame = tk.Frame(
#     main_frame,
#     bg="#F0FAF5"
# )

# result_box_frame.pack(padx=25, pady=(8, 20))


# # =========================================
# # SCROLLBAR
# # =========================================

# scrollbar = tk.Scrollbar(result_box_frame)

# scrollbar.pack(side="right", fill="y")


# # =========================================
# # RESULT TEXT BOX
# # =========================================

# result_label = tk.Text(
#     result_box_frame,
#     font=("Segoe UI", 11),
#     bg="white",
#     fg="#333333",
#     relief="solid",
#     bd=1,
#     width=65,
#     height=16,
#     padx=15,
#     pady=12,
#     wrap="word",
#     yscrollcommand=scrollbar.set
# )

# result_label.pack(side="left")

# scrollbar.config(command=result_label.yview)


# # =========================================
# # DEFAULT TEXT
# # =========================================

# result_label.insert(
#     tk.END,
#     "Results will appear here after searching or uploading an image..."
# )

# result_label.config(state="disabled")


# # =========================================
# # BUTTON FRAME
# # =========================================

# button_frame = tk.Frame(
#     main_frame,
#     bg="#F0FAF5"
# )

# button_frame.pack(fill="x", padx=25, pady=(0, 20))

# # =========================================
# # UPLOAD FUNCTION
# # =========================================

# def upload_image():

#     file_path = filedialog.askopenfilename(
#         title="Select Medicine Image",
#         filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
#     )

#     if file_path:

#         # OCR detect
#         medicine_name = detect_medicine(file_path)

#         if medicine_name:
#          medicine_name = medicine_name.strip()

#         result_label.config(state="normal")

#         result_label.delete(1.0, tk.END)

#         # If OCR found medicine
#         if medicine_name:

#             # Database search
#             data = search_medicine(medicine_name)

#             if data:

#                 result_text = f"""
# ✅ Medicine Found

# 💊 Name:
# {data[1]}

# 📌 Use:
# {data[2]}

# ⚠ Side Effects:
# {data[3]}

# 💉 Dosage:
# {data[4]}
# """

#                 result_label.insert(tk.END, result_text)

#                 status_label.config(
#                     text="● Medicine Found",
#                     fg="#3B6D11"
#                 )

#             else:

#                 result_label.insert(
#                     tk.END,
#                     "⚠ Medicine detected but not uploaded in database yet."
#                 )

#         else:

#             result_label.insert(
#                 tk.END,
#                 """
# ⚠ Medicine Not Recognized

# Please upload a clearer image.
# """
#             )

#             status_label.config(
#                 text="● OCR Failed",
#                 fg="red"
#             )

#         result_label.config(state="disabled")


# # =========================================
# # UPLOAD BUTTON
# # =========================================

# upload_button = tk.Button(
#     button_frame,
#     text="📷 Upload Medicine Image",
#     font=("Segoe UI", 11, "bold"),
#     bg="#3B6D11",
#     fg="white",
#     relief="flat",
#     padx=18,
#     pady=8,
#     cursor="hand2",
#     command=upload_image
# )

# upload_button.pack(side="left")


# # =========================================
# # CLEAR FUNCTION
# # =========================================

# def clear_data():

#     entry.delete(0, tk.END)

#     result_label.config(state="normal")

#     result_label.delete(1.0, tk.END)

#     result_label.insert(
#         tk.END,
#         "Results will appear here after searching or uploading an image..."
#     )

#     result_label.config(state="disabled")

#     status_label.config(
#         text="● Ready",
#         fg="#3B6D11"
#     )


# # =========================================
# # CLEAR BUTTON
# # =========================================

# clear_button = tk.Button(
#     button_frame,
#     text="✕ Clear",
#     font=("Segoe UI", 11, "bold"),
#     bg="#888780",
#     fg="white",
#     relief="flat",
#     padx=18,
#     pady=8,
#     cursor="hand2",
#     command=clear_data
# )

# clear_button.pack(side="right")


# # =========================================
# # STATUS BAR
# # =========================================

# status_label = tk.Label(
#     root,
#     text="● Ready",
#     font=("Segoe UI", 10),
#     bg="#EAF3DE",
#     fg="#3B6D11",
#     anchor="w",
#     padx=15,
#     pady=6
# )

# status_label.pack(fill="x", padx=40, pady=(10, 0))


# # =========================================
# # FOOTER
# # =========================================

# footer = tk.Label(
#     root,
#     text="Final Year Project · Medicine Identifier",
#     font=("Segoe UI", 9),
#     bg="#E8F5EE",
#     fg="#5F5E5A"
# )

# footer.pack(pady=15)


# # =========================================
# # RUN APP
# # =========================================

# root.mainloop()


# =========================================
# COMPACT MODERN MEDICINE IDENTIFIER UI
# =========================================

import tkinter as tk
from tkinter import filedialog
from database import search_medicine
from medicine_reader import detect_medicine


# =========================================
# MAIN WINDOW
# =========================================

root = tk.Tk()

root.title("Medicine Identifier")

root.geometry("860x560")

root.configure(bg="#245D1E")

root.resizable(False, False)


# =========================================
# HOVER EFFECTS
# =========================================

def hover_green(e):
    e.widget['bg'] = '#4E9A06'

def leave_green(e):
    e.widget['bg'] = '#66A61E'

def hover_dark(e):
    e.widget['bg'] = '#245D1E'

def leave_dark(e):
    e.widget['bg'] = '#2E6E12'


# =========================================
# TITLE SECTION
# =========================================

title = tk.Label(
    root,
    text="🌿  Medicine Identifier",
    font=("Segoe UI", 26, "bold"),
    bg="#245D1E",
    fg="white"
)

title.pack(anchor="w", padx=28, pady=(20, 3))


subtitle = tk.Label(
    root,
    text="Search by name or upload an image to identify a medicine",
    font=("Segoe UI", 11),
    bg="#245D1E",
    fg="#D6E4C3"
)

subtitle.pack(anchor="w", padx=30, pady=(0, 12))


# =========================================
# MAIN WHITE CONTAINER
# =========================================

main_frame = tk.Frame(
    root,
    bg="#F3F3F3",
    width=810,
    height=430
)

main_frame.pack(padx=20, pady=10)

main_frame.pack_propagate(False)


# =========================================
# LEFT PANEL
# =========================================

left_panel = tk.Frame(
    main_frame,
    bg="#F3F3F3",
    width=320
)

left_panel.pack(side="left", fill="y", padx=(20, 10), pady=18)

left_panel.pack_propagate(False)


# =========================================
# RIGHT PANEL
# =========================================

right_panel = tk.Frame(
    main_frame,
    bg="#F3F3F3"
)

right_panel.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=18)


# =========================================
# MEDICINE NAME LABEL
# =========================================

name_label = tk.Label(
    left_panel,
    text="Medicine Name",
    font=("Segoe UI", 11),
    bg="#F3F3F3",
    fg="#8A8A8A"
)

name_label.pack(anchor="w", pady=(8, 6))


# =========================================
# ENTRY BOX
# =========================================

entry = tk.Entry(
    left_panel,
    font=("Segoe UI", 13),
    bg="white",
    fg="#333333",
    relief="solid",
    bd=1
)

entry.pack(fill="x", ipady=7)


# =========================================
# BUTTON FRAME
# =========================================

button_frame = tk.Frame(
    left_panel,
    bg="#F3F3F3"
)

button_frame.pack(fill="x", pady=14)


# =========================================
# RESULT UPDATE FUNCTION
# =========================================

def update_result(data):

    result_box.config(state="normal")

    result_box.delete(1.0, tk.END)

    if data:

        result_text = f"""
✅ MEDICINE FOUND

━━━━━━━━━━━━━━━━━━

💊 Name:
{data[1]}

📌 Use:
{data[2]}

⚠ Side Effects:
{data[3]}

💉 Dosage:
{data[4]}

━━━━━━━━━━━━━━━━━━
"""

        result_box.insert(tk.END, result_text)

        status_label.config(
            text="Ready",
            bg="#E7EDD7",
            fg="#6C8B2A"
        )

    else:

        result_box.insert(
            tk.END,
            """
⚠ MEDICINE NOT UPLOADED YET

This medicine is currently not available
in the database.
"""
        )

        status_label.config(
            text="Not Found",
            bg="#FFF1CC",
            fg="#C67C00"
        )

    result_box.config(state="disabled")


# =========================================
# SEARCH FUNCTION
# =========================================

def search():

    medicine_name = entry.get().strip()

    data = search_medicine(medicine_name)

    update_result(data)


# =========================================
# SEARCH BUTTON
# =========================================

search_button = tk.Button(
    button_frame,
    text="🔍 Search",
    font=("Segoe UI", 11, "bold"),
    bg="#66A61E",
    fg="white",
    activebackground="#4E9A06",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=13,
    pady=9,
    command=search
)

search_button.pack(side="left", padx=(0, 6))

search_button.bind("<Enter>", hover_green)
search_button.bind("<Leave>", leave_green)


# =========================================
# UPLOAD FUNCTION
# =========================================

def upload_image():

    file_path = filedialog.askopenfilename(
        title="Select Medicine Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:

        image_preview.config(
            text="✅ Image Uploaded",
            fg="#4E9A06"
        )

        medicine_name = detect_medicine(file_path)

        if medicine_name:
            medicine_name = medicine_name.strip()

        print("Detected Medicine:", medicine_name)

        data = search_medicine(medicine_name)

        update_result(data)


# =========================================
# UPLOAD BUTTON
# =========================================

upload_button = tk.Button(
    button_frame,
    text="💾 Upload",
    font=("Segoe UI", 11, "bold"),
    bg="#2E6E12",
    fg="white",
    activebackground="#245D1E",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=13,
    pady=9,
    command=upload_image
)

upload_button.pack(side="left")

upload_button.bind("<Enter>", hover_dark)
upload_button.bind("<Leave>", leave_dark)


# =========================================
# SEPARATOR
# =========================================

separator = tk.Frame(
    left_panel,
    bg="#D4D4D4",
    height=2
)

separator.pack(fill="x", pady=12)


# =========================================
# IMAGE PREVIEW LABEL
# =========================================

preview_label = tk.Label(
    left_panel,
    text="Image Preview",
    font=("Segoe UI", 11),
    bg="#F3F3F3",
    fg="#8A8A8A"
)

preview_label.pack(anchor="w", pady=(6, 8))


# =========================================
# IMAGE PREVIEW BOX
# =========================================

image_preview = tk.Label(
    left_panel,
    text="No image uploaded",
    font=("Segoe UI", 12),
    bg="white",
    fg="#999999",
    relief="solid",
    bd=1,
    width=30,
    height=5
)

image_preview.pack(fill="x")


# =========================================
# CLEAR FUNCTION
# =========================================

def clear_all():

    entry.delete(0, tk.END)

    image_preview.config(
        text="No image uploaded",
        fg="#999999"
    )

    result_box.config(state="normal")

    result_box.delete(1.0, tk.END)

    result_box.insert(
        tk.END,
        "\n\nResults will appear here\nafter searching or uploading an image..."
    )

    result_box.config(state="disabled")

    status_label.config(
        text="Ready",
        bg="#E7EDD7",
        fg="#6C8B2A"
    )


# =========================================
# CLEAR BUTTON
# =========================================

clear_button = tk.Button(
    left_panel,
    text="✕ Clear All",
    font=("Segoe UI", 11, "bold"),
    bg="#9B9994",
    fg="white",
    relief="flat",
    cursor="hand2",
    pady=9,
    command=clear_all
)

clear_button.pack(fill="x", pady=(14, 0))


# =========================================
# VERTICAL SEPARATOR
# =========================================

vertical_separator = tk.Frame(
    main_frame,
    bg="#D9D9D9",
    width=2
)

vertical_separator.place(x=350, y=18, height=390)


# =========================================
# RESULT HEADER
# =========================================

result_title = tk.Label(
    right_panel,
    text="Result",
    font=("Segoe UI", 14, "bold"),
    bg="#F3F3F3",
    fg="#1E3A16"
)

result_title.pack(anchor="w")


# =========================================
# STATUS LABEL
# =========================================

status_label = tk.Label(
    right_panel,
    text="Ready",
    font=("Segoe UI", 10, "bold"),
    bg="#E7EDD7",
    fg="#6C8B2A",
    padx=12,
    pady=5
)

status_label.pack(anchor="e", pady=(0, 8))


# =========================================
# RESULT BOX
# =========================================

result_box = tk.Text(
    right_panel,
    font=("Segoe UI", 12),
    bg="#FAFAFA",
    fg="#888888",
    relief="solid",
    bd=1,
    wrap="word",
    padx=12,
    pady=12,
    spacing3=6
)

result_box.pack(fill="both", expand=True)

result_box.insert(
    tk.END,
    "\n\nResults will appear here\nafter searching or uploading an image..."
)

result_box.config(state="disabled")


# =========================================
# RUN APP
# =========================================

root.mainloop()
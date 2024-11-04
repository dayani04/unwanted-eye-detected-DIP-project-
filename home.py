import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess

def open_patient_page():
    try:
        subprocess.Popen(["python", "patient.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Patient page: {e}")

def open_doctor_page():
    try:
        subprocess.Popen(["python", "doctor.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Doctor page: {e}")

def open_login_page():
    try:
        subprocess.Popen(["python", "login.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Login page: {e}")

# Main window configuration
root = tk.Tk()
root.title("Home Page")
root.configure(bg='#e2eaf4')  # Light blue background
root.geometry("1600x850")

# Navigation Bar
nav_frame = tk.Frame(root, bg='#4A90E2')  # Dark blue navbar background
nav_frame.pack(fill='x')

# Navigation buttons with light blue color and padding
button_color = '#ADD8E6'  # Light blue color for buttons

tk.Button(nav_frame, text="Home", command=lambda: print("Home clicked"), bg=button_color, fg='black', font=("Arial", 12), padx=15, pady=5).pack(side='left', padx=10, pady=10)
tk.Button(nav_frame, text="Patient", command=open_patient_page, bg=button_color, fg='black', font=("Arial", 12), padx=15, pady=5).pack(side='left', padx=10, pady=10)
tk.Button(nav_frame, text="Login", command=open_login_page, bg=button_color, fg='black', font=("Arial", 12), padx=15, pady=5).pack(side='left', padx=10, pady=10)

# Title and Description
title_label = tk.Label(root, text="VisionCareHub", font=("Arial", 36, "bold"), bg='#e2eaf4')
title_label.pack(pady=20)

welcome_label = tk.Label(
    root, 
    text="Welcome to VisionCareHub, your one-stop solution for comprehensive vision care. We offer a range of services including eye exams, consultations with specialists, and personalized treatment plans.",
    font=("Arial", 18), 
    bg='#e2eaf4', 
    wraplength=1200
)
welcome_label.pack(pady=20)

# Frame for images
content_frame = tk.Frame(root, bg='#e2eaf4')
content_frame.pack(expand=True, fill='both', pady=20)

# Load images
try:
    img_eye = PhotoImage(file="1eye.png")
    img_glaucoma = PhotoImage(file="2eye.png")
    img_diabetic = PhotoImage(file="3eye.png")

    # Create and place images
    img_label_eye = tk.Label(content_frame, image=img_eye, bg='#e2eaf4', borderwidth=2, relief="solid")
    img_label_eye.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    img_label_glaucoma = tk.Label(content_frame, image=img_glaucoma, bg='#e2eaf4', borderwidth=2, relief="solid")
    img_label_glaucoma.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

    img_label_diabetic = tk.Label(content_frame, image=img_diabetic, bg='#e2eaf4', borderwidth=2, relief="solid")
    img_label_diabetic.grid(row=0, column=2, padx=20, pady=20, sticky='nsew')

    # Adjust grid weights to expand images
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

except tk.TclError as e:
    print(f"Error loading image: {e}")

root.mainloop()


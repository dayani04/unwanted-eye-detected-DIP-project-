import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error

# Global variables for images
img = None
segmented_img = None
processed_img = None

# Function to connect to the database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='eye_checkup_system'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to fetch patient IDs
def fetch_patient_ids():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT patient_id FROM patients")
            patient_ids = [str(row[0]) for row in cursor.fetchall()]
            return patient_ids
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

# Function to open an image
def open_image():
    global img, original_img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        display_image(img, original_img_display)

# Function to segment the optic nerve
def segment_optic_nerve():
    global img, segmented_img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    segmented_img = edges
    display_image(edges, segmented_img_display)

# Function to preprocess the image
def preprocess_image():
    global img, processed_img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    preprocessed = cv2.GaussianBlur(img, (5, 5), 0)
    processed_img = preprocessed
    display_image(preprocessed, processed_img_display)

# Function to enhance the image
def enhance_image():
    global img, processed_img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    enhanced = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    processed_img = enhanced
    display_image(enhanced, processed_img_display)

# Function to detect glaucoma
def detect_glaucoma():
    global img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, glaucoma_region = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    display_image(glaucoma_region, processed_img_display)
    
    glaucoma_detected = np.sum(glaucoma_region) > 50000
    if glaucoma_detected:
        result = "Glaucoma detected!"
        result_label.config(text=result, fg="blue")
    else:
        result = "No glaucoma detected."
        result_label.config(text=result, fg="blue")

# Function to display an image in the GUI
def display_image(img_array, display_widget):
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((100, 100))  # Resize the image to 100x100 pixels
    img_tk = ImageTk.PhotoImage(img_pil)
    display_widget.config(image=img_tk)
    display_widget.image = img_tk

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Glaucoma Detection System")

# Fetch and display patient IDs in a combobox
patient_ids = fetch_patient_ids()
patient_id_var = tk.StringVar(value=patient_ids)

tk.Label(root, text="Select Patient ID:").grid(row=0, column=0)
patient_id_checkbox = ttk.Combobox(root, textvariable=patient_id_var, values=patient_ids, state='readonly')
patient_id_checkbox.grid(row=0, column=1, columnspan=3, sticky="w")

# Display areas for images (arranged vertically)
tk.Label(root, text="Original Image").grid(row=1, column=0)
original_img_display = tk.Label(root)
original_img_display.grid(row=2, column=0)

tk.Label(root, text="Segmented Image").grid(row=3, column=0)
segmented_img_display = tk.Label(root)
segmented_img_display.grid(row=4, column=0)

tk.Label(root, text="Processed Image").grid(row=5, column=0)
processed_img_display = tk.Label(root)
processed_img_display.grid(row=6, column=0)

# Label for "Glaucoma detected" message
result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")
result_label.grid(row=7, column=0, columnspan=3, pady=10)

# Buttons for the different steps (arranged horizontally)
tk.Button(root, text="Open Image", command=open_image).grid(row=8, column=0)
tk.Button(root, text="Segment Optic Nerve", command=segment_optic_nerve).grid(row=8, column=1)
tk.Button(root, text="Preprocess Image", command=preprocess_image).grid(row=8, column=2)
tk.Button(root, text="Enhance Image", command=enhance_image).grid(row=9, column=0)
tk.Button(root, text="Detect Glaucoma", command=detect_glaucoma).grid(row=9, column=1)

root.mainloop()
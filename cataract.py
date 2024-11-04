import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error

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
    global img, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((100, 100))  # Resize the image to 100x100 pixels
        img_tk = ImageTk.PhotoImage(img_pil)
        img_display.config(image=img_tk)
        img_display.image = img_tk

# Function to segment the retina
def segment_retina():
    global img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, segmented = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    display_image(segmented)

# Function to preprocess the image
def preprocess_image():
    global img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    preprocessed = cv2.GaussianBlur(img, (5, 5), 0)
    display_image(preprocessed)

# Function to enhance the image
def enhance_image():
    global img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    enhanced = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    display_image(enhanced)

# Function to detect cataracts
def detect_cataract():
    global img
    if img is None:
        result_label.config(text="Please upload an image first.", fg="red")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cataract_region = gray < 100  # Simple thresholding

    # Convert the cataract_region to uint8
    cataract_image = (cataract_region * 255).astype(np.uint8)
    
    display_image(cataract_image)
    
    cataract_detected = np.sum(cataract_region) > 0.15 * cataract_region.size
    
    if cataract_detected:
        result = "Cataract detected!"
        result_label.config(text=result, fg="blue")
        display_after_surgery_image()
    else:
        result = "No cataract detected."
        result_label.config(text=result, fg="blue")

# Function to simulate an "after surgery" image
def simulate_after_surgery_image():
    global img
    if img is None:
        return None
    
    # Simulate the "after surgery" image by removing cataract effects (simple color inversion)
    after_surgery_img = cv2.bitwise_not(img)
    return after_surgery_img

# Function to display an image after cataract surgery
def display_after_surgery_image():
    after_surgery_img = simulate_after_surgery_image()
    if after_surgery_img is not None:
        img_rgb = cv2.cvtColor(after_surgery_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((100, 100))  # Resize the image to 100x100 pixels
        img_tk = ImageTk.PhotoImage(img_pil)
        after_surgery_display.config(image=img_tk)
        after_surgery_display.image = img_tk
        after_surgery_label.config(text="After Surgery:")

# Function to display an image in the GUI
def display_image(img_array):
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((100, 100))  # Resize the image to 100x100 pixels
    img_tk = ImageTk.PhotoImage(img_pil)
    img_display.config(image=img_tk)
    img_display.image = img_tk

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Cataract Detection System")

# Fetch and display patient IDs in a combobox
patient_ids = fetch_patient_ids()
patient_id_var = tk.StringVar(value=patient_ids)

tk.Label(root, text="Select Patient ID:").grid(row=0, column=0)
patient_id_checkbox = ttk.Combobox(root, textvariable=patient_id_var, values=patient_ids, state='readonly')
patient_id_checkbox.grid(row=0, column=1, columnspan=3, sticky="w")

# Label for "Normal Eye"
tk.Label(root, text="Normal Eye:").grid(row=1, column=0, columnspan=4)

# Display a hardcoded normal eye image
normal_eye_path = r"C:\Users\DELL\Desktop\Screenshot 2024-10-31 225646.png"  # Make sure to have this image in the correct path
normal_eye_img = Image.open(normal_eye_path)
normal_eye_img = normal_eye_img.resize((100, 100))  # Resize the image to 100x100 pixels
normal_eye_tk = ImageTk.PhotoImage(normal_eye_img)

normal_eye_display = tk.Label(root, image=normal_eye_tk)
normal_eye_display.image = normal_eye_tk
normal_eye_display.grid(row=2, column=0, columnspan=4)

# Image display area for uploaded images
img_display = tk.Label(root)
img_display.grid(row=3, column=0, columnspan=4)

# Label for "Cataract detected" message
result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")
result_label.grid(row=4, column=0, columnspan=4, pady=10)

# Display area for the "after surgery" image
after_surgery_display = tk.Label(root)
after_surgery_display.grid(row=6, column=0, columnspan=4)

# Label for "After Surgery" message
after_surgery_label = tk.Label(root, text="", font=("Helvetica", 12))
after_surgery_label.grid(row=5, column=0, columnspan=4, pady=10)

# Buttons for the different steps
tk.Button(root, text="Open Image", command=open_image).grid(row=7, column=0)
tk.Button(root, text="Segment Retina", command=segment_retina).grid(row=7, column=1)
tk.Button(root, text="Preprocess Image", command=preprocess_image).grid(row=7, column=2)
tk.Button(root, text="Enhance Image", command=enhance_image).grid(row=7, column=3)
tk.Button(root, text="Detect Cataract", command=detect_cataract).grid(row=7, column=4)

root.mainloop()

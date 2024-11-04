import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

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

def register_patient(first_name, last_name, dob, gender, contact_number, email):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO patients (first_name, last_name, dob, gender, contact_number, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, dob, gender, contact_number, email)
            cursor.execute(query, values)
            connection.commit()
            messagebox.showinfo("Success", "Patient registered successfully")
        except Error as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def submit_form():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    dob = entry_dob.get()
    gender = var_gender.get()
    contact_number = entry_contact_number.get()
    email = entry_email.get()

    if not all([first_name, last_name, dob, gender, contact_number, email]):
        messagebox.showwarning("Input Error", "All fields are required")
        return

    register_patient(first_name, last_name, dob, gender, contact_number, email)

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Patient Registration")

tk.Label(root, text="First Name").grid(row=0, column=0)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=0, column=1)

tk.Label(root, text="Last Name").grid(row=1, column=0)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=1, column=1)

tk.Label(root, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0)
entry_dob = tk.Entry(root)
entry_dob.grid(row=2, column=1)

tk.Label(root, text="Gender").grid(row=3, column=0)
var_gender = tk.StringVar(value="Male")
tk.Radiobutton(root, text="Male", variable=var_gender, value="Male").grid(row=3, column=1)
tk.Radiobutton(root, text="Female", variable=var_gender, value="Female").grid(row=3, column=2)

tk.Label(root, text="Contact Number").grid(row=4, column=0)
entry_contact_number = tk.Entry(root)
entry_contact_number.grid(row=4, column=1)

tk.Label(root, text="Email").grid(row=5, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=5, column=1)

tk.Button(root, text="Register", command=submit_form).grid(row=6, column=1, columnspan=2)

root.mainloop()
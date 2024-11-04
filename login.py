import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import subprocess

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

def login():
    email = entry_email.get()
    password = entry_password.get()
    user_type = var_user_type.get()

    if not email or not password:
        messagebox.showwarning("Input Error", "Both email and password are required")
        return

    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()

            # Query based on the user type selection
            if user_type == "Patient":
                query = "SELECT * FROM patients WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Login", "Patient login successful")
                    root.destroy()  # Close the login window
                    subprocess.run(["python", "patienttreatments.py"])  # Open patient treatments page
                else:
                    messagebox.showerror("Login Failed", "Invalid credentials")

            elif user_type == "Doctor":
                query = "SELECT * FROM doctors WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Login", "Doctor login successful")
                    root.destroy()  # Close the login window
                    subprocess.run(["python", "doctor.py"])  # Open doctor dashboard page
                else:
                    messagebox.showerror("Login Failed", "Invalid credentials")

            else:
                messagebox.showwarning("Selection Error", "Please select a valid user type")

        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

def back_to_home():
    root.destroy()  # Close the current window
    subprocess.run(["python", "home.py"])  # Open home.py

# Set up the Tkinter login form
root = tk.Tk()
root.title("Login Form")
root.geometry("1500x850")  # Set window size to 1500x850
root.configure(bg='#e2eaf4')

# Center the form on the screen
form_frame = tk.Frame(root, bg='#ffffff', bd=2, relief=tk.SOLID, padx=50, pady=50)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place it at the center of the window

# Labels and entry fields
tk.Label(form_frame, text="Email", bg='#ffffff', font=('Arial', 16)).grid(row=0, column=0, pady=10, sticky='w')
entry_email = tk.Entry(form_frame, font=('Arial', 14), width=30)
entry_email.grid(row=0, column=1, pady=10)

tk.Label(form_frame, text="Password", bg='#ffffff', font=('Arial', 16)).grid(row=1, column=0, pady=10, sticky='w')
entry_password = tk.Entry(form_frame, show="*", font=('Arial', 14), width=30)
entry_password.grid(row=1, column=1, pady=10)

# Dropdown menu to select user type (Patient or Doctor)
tk.Label(form_frame, text="Login as", bg='#ffffff', font=('Arial', 16)).grid(row=2, column=0, pady=10, sticky='w')
var_user_type = tk.StringVar(value="Patient")
user_type_menu = tk.OptionMenu(form_frame, var_user_type, "Patient", "Doctor")
user_type_menu.config(font=('Arial', 14), width=27)
user_type_menu.grid(row=2, column=1, pady=10)

# Add a login button and Back button, all with #6495ed color
tk.Button(form_frame, text="Login", command=login, bg='#6495ed', fg='white', font=('Arial', 16), padx=20, pady=10).grid(row=3, column=0, columnspan=2, pady=20)
tk.Button(form_frame, text="Back", command=back_to_home, bg='#6495ed', fg='white', font=('Arial', 16), padx=20, pady=10).grid(row=4, column=0, columnspan=2)

root.mainloop()
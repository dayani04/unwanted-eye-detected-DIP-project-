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

def add_doctor():
    def submit_doctor():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        specialty = entry_specialty.get()
        contact_number = entry_contact_number.get()
        email = entry_email.get()
        password = entry_password.get()

        if not all([first_name, last_name, specialty, contact_number, email, password]):
            messagebox.showwarning("Input Error", "All fields are required")
            return

        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO doctors (first_name, last_name, specialty, contact_number, email, password)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (first_name, last_name, specialty, contact_number, email, password)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Doctor added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
                add_doctor_window.destroy()

    add_doctor_window = tk.Toplevel(root)
    add_doctor_window.title("Add Doctor")
    add_doctor_window.geometry("1600x850")  # Set the size to 1600x850
    
    tk.Label(add_doctor_window, text="First Name", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    entry_first_name = tk.Entry(add_doctor_window, font=("Arial", 14))
    entry_first_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_doctor_window, text="Last Name", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    entry_last_name = tk.Entry(add_doctor_window, font=("Arial", 14))
    entry_last_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_doctor_window, text="Specialty", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    entry_specialty = tk.Entry(add_doctor_window, font=("Arial", 14))
    entry_specialty.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_doctor_window, text="Contact Number", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5)
    entry_contact_number = tk.Entry(add_doctor_window, font=("Arial", 14))
    entry_contact_number.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_doctor_window, text="Email", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5)
    entry_email = tk.Entry(add_doctor_window, font=("Arial", 14))
    entry_email.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_doctor_window, text="Password", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=5)
    entry_password = tk.Entry(add_doctor_window, show="*", font=("Arial", 14))
    entry_password.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(add_doctor_window, text="Add Doctor", command=submit_doctor, font=("Arial", 14), bg="#6495ed", fg="white").grid(row=6, column=1, padx=10, pady=10)

def add_disease():
    def submit_disease():
        disease_name = entry_disease_name.get()
        description = entry_description.get()

        if not disease_name or not description:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO diseases (disease_name, description)
                VALUES (%s, %s)
                """
                values = (disease_name, description)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Disease added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
                add_disease_window.destroy()

    add_disease_window = tk.Toplevel(root)
    add_disease_window.title("Add Disease")
    add_disease_window.geometry("1600x850")  # Set the size to 1600x850
    
    tk.Label(add_disease_window, text="Disease Name", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    entry_disease_name = tk.Entry(add_disease_window, font=("Arial", 14))
    entry_disease_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_disease_window, text="Description", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    entry_description = tk.Entry(add_disease_window, font=("Arial", 14))
    entry_description.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(add_disease_window, text="Add Disease", command=submit_disease, font=("Arial", 14), bg="#6495ed", fg="white").grid(row=2, column=1, padx=10, pady=10)

def manage_treatments():
    def submit_treatment():
        checkup_id = entry_checkup_id.get()
        treatment_date = entry_treatment_date.get()
        treatment_description = entry_treatment_description.get()

        if not all([checkup_id, treatment_date, treatment_description]):
            messagebox.showwarning("Input Error", "All fields are required")
            return

        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO treatments (checkup_id, treatment_date, treatment_description)
                VALUES (%s, %s, %s)
                """
                values = (checkup_id, treatment_date, treatment_description)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Treatment added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
                manage_treatments_window.destroy()

    manage_treatments_window = tk.Toplevel(root)
    manage_treatments_window.title("Manage Treatments")
    manage_treatments_window.geometry("1600x850")  # Set the size to 1600x850
    
    tk.Label(manage_treatments_window, text="Checkup ID", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    entry_checkup_id = tk.Entry(manage_treatments_window, font=("Arial", 14))
    entry_checkup_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(manage_treatments_window, text="Treatment Date (YYYY-MM-DD)", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    entry_treatment_date = tk.Entry(manage_treatments_window, font=("Arial", 14))
    entry_treatment_date.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(manage_treatments_window, text="Treatment Description", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    entry_treatment_description = tk.Entry(manage_treatments_window, font=("Arial", 14))
    entry_treatment_description.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(manage_treatments_window, text="Add Treatment", command=submit_treatment, font=("Arial", 14), bg="#6495ed", fg="white").grid(row=3, column=1, padx=10, pady=10)

def go_back():
    root.destroy()
    # Assuming home.py is the main script, this line will run home.py again
    # If using subprocess to launch home.py:
    # import subprocess
    # subprocess.Popen(["python", "home.py"])

# Main dashboard window
root = tk.Tk()
root.title("Doctor Dashboard")
root.geometry("1600x850")  # Set the size to 1600x850
root.configure(bg='#e2eaf4')

tk.Label(root, text="Doctor Dashboard", font=("Arial", 24), bg='#e2eaf4').pack(pady=20)
tk.Button(root, text="Add New Doctor", command=add_doctor, font=("Arial", 14), bg="#6495ed", fg="white").pack(pady=10)
tk.Button(root, text="Add New Disease", command=add_disease, font=("Arial", 14), bg="#6495ed", fg="white").pack(pady=10)
tk.Button(root, text="Manage Treatments", command=manage_treatments, font=("Arial", 14), bg="#6495ed", fg="white").pack(pady=10)
tk.Button(root, text="Back", command=go_back, font=("Arial", 14), bg="#6495ed", fg="white").pack(pady=10)

root.mainloop()
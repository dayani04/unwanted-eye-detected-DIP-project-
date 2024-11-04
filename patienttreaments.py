import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2001',
            database='eye_checkup_system'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def fetch_treatments():
    checkup_id = entry_checkup_id.get()

    if not checkup_id:
        messagebox.showwarning("Input Error", "Checkup ID is required")
        return

    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            SELECT treatment_date, treatment_description
            FROM treatments
            WHERE checkup_id = %s
            """
            cursor.execute(query, (checkup_id,))
            treatments = cursor.fetchall()

            if treatments:
                text_treatments.delete("1.0", tk.END)  # Clear previous text
                for treatment in treatments:
                    treatment_date, treatment_description = treatment
                    text_treatments.insert(tk.END, f"Date: {treatment_date}\nDescription: {treatment_description}\n\n")
            else:
                messagebox.showinfo("No Treatments", "No treatments found for this Checkup ID")
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

def cancel_form():
    root.quit()  # Closes the form

# Set up the Tkinter GUI for viewing treatments
root = tk.Tk()
root.title("View Treatments")

# Set the window size to 1600x850
root.geometry("1600x850")
root.resizable(False, False)  # Optional: Prevents resizing

# Set the background color to rgb(226, 234, 244)
root.configure(bg='#e2eaf4')

# Set label background color to match the form background
tk.Label(root, text="Checkup ID", bg='#e2eaf4').grid(row=0, column=0, padx=10, pady=5)
entry_checkup_id = tk.Entry(root)
entry_checkup_id.grid(row=0, column=1, padx=10, pady=5)

# Add a button to fetch treatments
tk.Button(root, text="Fetch Treatments", command=fetch_treatments).grid(row=1, column=1, padx=10, pady=5)

# Text area to display treatments
text_treatments = tk.Text(root, height=15, width=80)
text_treatments.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Add a cancel button
tk.Button(root, text="Cancel", command=cancel_form).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
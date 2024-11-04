import mysql.connector
connection = mysql.connector.connect(
            host='localhost',           # Replace with your MySQL host
            user='root',       # Replace with your MySQL username
            password='root',   # Replace with your MySQL password
            database='eye_checkup_system'    # Replace with your MySQL database name
        )
my_cursor=connection.cursor()

connection.commit()
connection.close()
print("connection succesfully created")
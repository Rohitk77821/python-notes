import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    date TEXT NOT NULL,
    punch_in_time TEXT,
    punch_out_time TEXT
)
''')
conn.commit()

def punch_in(employee_id):
    today = datetime.now().date().isoformat()
    now = datetime.now().strftime('%H:%M:%S')

    # Check if already punched in today
    cursor.execute('''
    SELECT * FROM attendance WHERE employee_id = ? AND date = ? AND punch_in_time IS NOT NULL
    ''', (employee_id, today))
    record = cursor.fetchone()

    if record:
        print(f"Employee {employee_id} already punched in today at {record[3]}")
    else:
        cursor.execute('''
        INSERT INTO attendance (employee_id, date, punch_in_time) VALUES (?, ?, ?)
        ''', (employee_id, today, now))
        conn.commit()
        print(f"Employee {employee_id} punched in at {now}")

def punch_out(employee_id):
    today = datetime.now().date().isoformat()
    now = datetime.now().strftime('%H:%M:%S')

    # Check if punched in today and not punched out yet
    cursor.execute('''
    SELECT * FROM attendance WHERE employee_id = ? AND date = ? AND punch_in_time IS NOT NULL AND punch_out_time IS NULL
    ''', (employee_id, today))
    record = cursor.fetchone()

    if record:
        cursor.execute('''
        UPDATE attendance SET punch_out_time = ? WHERE id = ?
        ''', (now, record[0]))
        conn.commit()
        print(f"Employee {employee_id} punched out at {now}")
    else:
        print(f"Employee {employee_id} has not punched in today or already punched out.")

def view_attendance(employee_id):
    cursor.execute('''
    SELECT date, punch_in_time, punch_out_time FROM attendance WHERE employee_id = ? ORDER BY date DESC
    ''', (employee_id,))
    records = cursor.fetchall()
    print(f"Attendance records for Employee {employee_id}:")
    for rec in records:
        print(f"Date: {rec[0]}, Punch In: {rec[1]}, Punch Out: {rec[2]}")

# Example usage
if __name__ == "__main__":
    while True:
        print("\n1. Punch In\n2. Punch Out\n3. View Attendance\n4. Exit")
        choice = input("Enter choice: ")
        emp_id = input("Enter Employee ID: ")

        if choice == '1':
            punch_in(emp_id)
        elif choice == '2':
            punch_out(emp_id)
        elif choice == '3':
            view_attendance(emp_id)
        elif choice == '4':
            break
        else:
            
            print("Invalid choice. Try again.")

conn.close()

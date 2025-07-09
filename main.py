import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
import smtplib
from email.message import EmailMessage

# Email credentials
SENDER_EMAIL = "akshitha111723039007@gmail.com"
APP_PASSWORD = "bjmswejzdydqxyan"  # ⚠️ Keep this secret in production

# Number of hours per day
num_hours = 5

# Student data
students = [
    {"uid": 1111723039001, "name": "sowmya", "email": "sowmya.parent@gmail.com"},
    {"uid": 1111723039002, "name": "Yamini", "email": "yamini.parent@gmail.com"},
    {"uid": 1111723039003, "name": "Bhavya", "email": "bhavya.parent@gmail.com"},
    {"uid": 1111723039004, "name": "Rishika", "email": "rishika.parent@gmail.com"},
    {"uid": 1111723039005, "name": "Alice", "email": "alice.parent@gmail.com"},
    {"uid": 1111723039006, "name": "Jhansi", "email": "jhansi.parent@gmail.com"},
    {"uid": 1111723039007, "name": "Akshitha", "email": "akshithagidigam@gmail.com"},
    {"uid": 1111723039008, "name": "Mounika", "email": "mounika.parent@gmail.com"},
    {"uid": 1111723039009, "name": "Raja Rani", "email": "rajarani.parent@gmail.com"},
    {"uid": 1111723039010, "name": "Raziya", "email": "raziya.parent@gmail.com"},
    {"uid": 1111723039011, "name": "Manasa", "email": "manasa.parent@gmail.com"},
    {"uid": 1111723039012, "name": "Sudhiksha", "email": "Sudhikshagoud23@gmail.com"},
    {"uid": 1111723039013, "name": "Rubeena", "email": "rubeena.parent@gmail.com"},
    {"uid": 1111723039014, "name": "Lasya", "email": "lasya.parent@gmail.com"},
    {"uid": 1111723039015, "name": "Fatima", "email": "fatima.parent@gmail.com"},
    {"uid": 111723039031, "name": "Kurma Sampath", "email": "sampath11172@gmail.com"}
]

# Database setup
conn = sqlite3.connect("attendance.db")
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        date TEXT,
        uid INTEGER,
        name TEXT,
        hour1 TEXT,
        hour2 TEXT,
        hour3 TEXT,
        hour4 TEXT,
        hour5 TEXT
    )
''')
conn.commit()

# Email sending function
def send_email_alert(to_email, student_name, uid, absent_hours):
    hour_list = ", ".join([f"H{h+1}" for h in absent_hours])
    msg = EmailMessage()
    msg['Subject'] = f"Absentee Alert: {student_name}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg.set_content(f"""Dear Parent,

This is to inform you that your child {student_name} (UID: {uid}) was marked absent today for the following hours: {hour_list}.

Thank you,
Smart Attendance System
""")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            print(f"📨 Email sent to {student_name}'s parent at {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email for {student_name}: {e}")

# GUI setup
root = tk.Tk()
root.title("Smart Attendance System")

tk.Label(root, text="Select Date:", font=("Arial", 12)).grid(row=0, column=0, pady=10)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Click each box to mark P/A", font=("Arial", 14)).grid(row=1, column=0, columnspan=10, pady=10)

tk.Label(root, text="UID", font=("bold")).grid(row=2, column=0)
tk.Label(root, text="Name", font=("bold")).grid(row=2, column=1)

for h in range(num_hours):
    tk.Label(root, text=f"H{h+1}", font=("bold")).grid(row=2, column=2 + h)

attendance_data = {}
buttons = {}

def toggle_button(uid, hour):
    current = buttons[(uid, hour)]['text']
    new_status = "A" if current == "P" else "P"
    buttons[(uid, hour)]['text'] = new_status
    buttons[(uid, hour)]['bg'] = "red" if new_status == "A" else "lightgreen"
    attendance_data[uid][hour] = new_status

# Add student rows
for r, student in enumerate(students, start=3):
    uid = student["uid"]
    name = student["name"]
    attendance_data[uid] = ["P"] * num_hours

    tk.Label(root, text=uid).grid(row=r, column=0)
    tk.Label(root, text=name).grid(row=r, column=1)

    for h in range(num_hours):
        btn = tk.Button(root, text="P", width=4, bg="lightgreen", command=lambda uid=uid, h=h: toggle_button(uid, h))
        btn.grid(row=r, column=2 + h)
        buttons[(uid, h)] = btn

# Submit button function
def submit_attendance():
    selected_date = date_entry.get()
    for student in students:
        uid = student["uid"]
        name = student["name"]
        email = student["email"]
        hours = attendance_data[uid]

        # Save to database
        cur.execute('''
            INSERT INTO attendance (date, uid, name, hour1, hour2, hour3, hour4, hour5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (selected_date, uid, name, *hours))

        # Find absent hours and send email
        absent_hours = [i for i, status in enumerate(hours) if status == "A"]
        if absent_hours:
            send_email_alert(email, name, uid, absent_hours)

    conn.commit()
    conn.close()
    messagebox.showinfo("Done", "Attendance saved and alerts sent!")
    root.destroy()

tk.Button(root, text="Submit Attendance", bg="blue", fg="white", command=submit_attendance).grid(
    row=len(students)+4, column=0, columnspan=10, pady=20)

root.mainloop()

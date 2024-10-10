import smtplib
import re
import random
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Global variables
otp = None
otp_expiry = None
timer_label = None
timer_id = None
attempts = 0
max_attempts = 3

# Generating an OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


# Email Validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|net|org|edu)$'
    valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]

    if re.match(pattern, email):
        domain = email.split('@')[1]
        return domain in valid_domains
    return False


# SMTP to send OTP
def send_otp(email, otp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "appbluetesting@gmail.com"
    sender_password = "wrgc jzcu vubm vqgx"
    subject = "OTP VERIFICATION"
    body = f"Your OTP code is {otp}. Please enter this code to verify your identity."
    msg = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg)
        print("OTP sent successfully.")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

# Update Timer
def update_timer():
    global timer_id, otp_expiry
    if otp_expiry:
        remaining_time = otp_expiry - datetime.now()
        seconds = int(remaining_time.total_seconds())
        if seconds > 0:
            timer_label.config(text=f"Time remaining: {seconds} seconds")
            timer_id = window.after(1000, update_timer)  # Updates every second
        else:
            timer_label.config(text="OTP has expired.")
            messagebox.showwarning("Warning", "OTP has expired. Please request a new OTP.")

#checking email and sending OTP
def check_email():
    global otp, otp_expiry
    email = Email_entry.get("1.0", "end-1c").strip()
    if is_valid_email(email):
        otp = generate_otp()
        # OTP expire set to 3 minutes
        otp_expiry = datetime.now() + timedelta(minutes=3)
        send_otp(email, otp)
        messagebox.showinfo("Success", "OTP sent to your email.")
        if timer_id:
            window.after_cancel(timer_id)
        # Start the timer
        update_timer()
    else:
        messagebox.showerror("Error", "Invalid email address. Re-enter the correct email.")


# OTP verification
def verify_otp():
    global otp, otp_expiry,timer_id, attempts
    entered_otp = otp_entry.get().strip()

    if otp_expiry and datetime.now() > otp_expiry:
        messagebox.showwarning("Warning", "OTP has expired. Please request a new OTP.")
        otp = None
        otp_expiry = None
        return

    if entered_otp == otp:
        messagebox.showinfo("Info", "OTP verified successfully.")
        otp = None
        otp_expiry = None
        timer_label.config(text="")
        if timer_id:
            #Stop the timer if OTP is verified
            window.after_cancel(timer_id)
    else:
        attempts += 1
        remaining_attempts = max_attempts - attempts
        if remaining_attempts > 0:
            messagebox.showwarning("Warning", f"Invalid OTP. You have {remaining_attempts} attempts left.")
        else:
            messagebox.showerror("Error", "Maximum attempts reached. Please request a new OTP.")

# GUI Setup
window = tk.Tk()
window.title("OTP Verification")
window.minsize(width=600, height=550)
window.resizable(False, False)

# Labels and Entries
canvas = tk.Canvas(window, bg="light blue", width=400, height=400)
canvas.pack()

login_title = tk.Label(window, text="OTP Verification", font='bold', bg='light blue')
login_title.place(x=230, y=10)

label1 = tk.Label(window, text="Enter your email address:", bg="light blue")
label1.place(x=220, y=80)

Email_entry = tk.Text(window, borderwidth=2, highlightthickness=0, wrap="word", width=20, height=2)
Email_entry.place(x=220, y=100)

send_otp_button = tk.Button(window, text="Send OTP", command=check_email, bg='sky blue')
send_otp_button.place(x=270, y=150)

label2 = tk.Label(window, text="Enter OTP:", bg="light blue")
label2.place(x=220, y=190)

otp_entry = tk.Entry(window, borderwidth=2, highlightthickness=0, width=20)
otp_entry.place(x=220, y=220)

submit_button = tk.Button(window, text="SUBMIT", command=verify_otp, bg='sky blue')
submit_button.place(x=280, y=260)

timer_label = tk.Label(window, text="", bg="light blue", font=("Arial", 12))
timer_label.place(x=190, y=300)

window.mainloop()


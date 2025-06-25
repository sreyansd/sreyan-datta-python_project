import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime
import pickle


reminder_file = "reminders.pkl"


def load_reminders():
    try:
        with open(reminder_file, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_reminders(reminders):
    with open(reminder_file, "wb") as f:
        pickle.dump(reminders, f)

def display_calendar(month, year):
    cal = calendar.monthcalendar(year, month)
    for widget in frame_calendar.winfo_children():
        widget.destroy()

    for week in cal:
        for day in week:
            if day == 0:
                continue
            button = tk.Button(frame_calendar, text=str(day), width=4, height=2, command=lambda day=day: add_reminder(day))
            button.grid(row=cal.index(week), column=week.index(day))

def add_reminder(day):
    def save_reminder():
        reminder_text = reminder_entry.get()
        if reminder_text.strip():
            reminders[day] = reminder_text
            save_reminders(reminders)
            update_reminder_label(day)
            reminder_window.destroy()

    reminder_window = tk.Toplevel(root)
    reminder_window.title(f"Add Reminder for {day}")
    reminder_label = tk.Label(reminder_window, text=f"Enter reminder for {day}:")
    reminder_label.pack(pady=10)
    
    reminder_entry = tk.Entry(reminder_window, width=50)
    reminder_entry.pack(pady=10)
    
    save_button = tk.Button(reminder_window, text="Save", command=save_reminder)
    save_button.pack(pady=10)

def update_reminder_label(day):
    reminder_text = reminders.get(day, "No reminders set.")
    label = tk.Label(frame_calendar, text=reminder_text, anchor="w", width=20)
    label.grid(row=cal.index(week), column=week.index(day))


def display_reminders():
    reminder_list_window = tk.Toplevel(root)
    reminder_list_window.title("All Reminders")
    for day, reminder in reminders.items():
        reminder_label = tk.Label(reminder_list_window, text=f"Day {day}: {reminder}")
        reminder_label.pack()

root = tk.Tk()
root.title("Monthly Calendar with Reminders")


reminders = load_reminders()

frame_calendar = tk.Frame(root)
frame_calendar.pack(pady=20)


current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year


display_calendar(current_month, current_year)


def previous_month():
    global current_month, current_year
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    display_calendar(current_month, current_year)

def next_month():
    global current_month, current_year
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    display_calendar(current_month, current_year)

prev_button = tk.Button(root, text="Previous Month", command=previous_month)
prev_button.pack(side="left", padx=20)

next_button = tk.Button(root, text="Next Month", command=next_month)
next_button.pack(side="right", padx=20)


view_reminders_button = tk.Button(root, text="View All Reminders", command=display_reminders)
view_reminders_button.pack(pady=20)

root.mainloop()

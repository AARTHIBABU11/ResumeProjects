import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, Text, END
from tkinter import *


# ------------------- API Setup -------------------
API_URL = "http://127.0.0.1:8001/deadlines/"  # Ensure FastAPI is running here
window = Tk()
# ------------------- GUI Setup -------------------
root = tk.Tk()
root.title("💖 Deadline Manager 💖")
root.geometry("550x600")
root.configure(bg="#FFE4F2")  # Light pink

# ------------------- Fonts & Styles -------------------
font_label = ("Comic Sans MS", 12, "bold")
font_entry = ("Verdana", 11)
font_button = ("Arial", 12, "bold")

# ------------------- Title Input -------------------
tk.Label(root, text="📌 Title", font=font_label, bg="#FFE4F2", fg="#99004d").pack(pady=(20, 5))
title_entry = tk.Entry(root, font=font_entry, width=40, bg="#fff0f5", bd=2, relief=tk.RIDGE)
title_entry.pack()

# ------------------- Due Date Input -------------------
tk.Label(root, text="📅 Due Date (YYYY-MM-DD)", font=font_label, bg="#FFE4F2", fg="#99004d").pack(pady=(20, 5))
due_entry = tk.Entry(root, font=font_entry, width=40, bg="#fff0f5", bd=2, relief=tk.RIDGE)
due_entry.pack()

# ------------------- Description -------------------
tk.Label(root, text="📝 Description", font=font_label, bg="#FFE4F2", fg="#99004d").pack(pady=(20, 5))
desc_entry = tk.Text(root, font=font_entry, height=5, width=40, bg="#fff0f5", bd=2, relief=tk.RIDGE)
desc_entry.pack()

# ------------------- Delete ID -------------------
tk.Label(root, text="Enter Deadline ID to Delete:", font=font_label, bg="#FFE4F2").pack(pady=(20, 5))
delete_entry = tk.Entry(root, font=font_entry)
delete_entry.pack()

# ------------------- Status Message -------------------
status_label = tk.Label(root, text="", font=("Verdana", 11), bg="#FFE4F2", fg="green")
status_label.pack(pady=10)

# ------------------- Display Box -------------------
display_box = tk.Text(root, height=10, width=60, font=("Courier", 10), bg="#f0f8ff", bd=2, relief=tk.SUNKEN)
display_box.pack(pady=15)

# ------------------- Functions -------------------

def add_deadline():
    title = title_entry.get()
    due_date = due_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()

    if not title or not due_date:
        messagebox.showwarning("Missing Info", "Please fill in both Title and Due Date.")
        return

    data = {
        "title": title,
        "due_date": due_date,
        "description": description
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            status_label.config(text="✅ Deadline added successfully!", fg="green")
            title_entry.delete(0, tk.END)
            due_entry.delete(0, tk.END)
            desc_entry.delete("1.0", tk.END)
            show_deadlines()
        else:
            status_label.config(text="❌ Failed to add deadline", fg="red")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Couldn't connect to server:\n{str(e)}")

def show_deadlines():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            
            if not isinstance(data, list):
                messagebox.showerror("Error", "Invalid response format (Expected List).")
                return

            display_box.delete("1.0", tk.END)

            if not data:
                display_box.insert(tk.END, "✨ No deadlines yet!\n")
            else:
                for d in data:
                    display_box.insert(tk.END, f"🆔 ID: {d.get('id', 'N/A')}\n")
                    display_box.insert(tk.END, f"📌 {d.get('title', '')}\n")
                    display_box.insert(tk.END, f"🗓️ Due: {d.get('due_date', '')}\n")
                    display_box.insert(tk.END, f"📝 {d.get('description', '')}\n")
                    display_box.insert(tk.END, "-"*40 + "\n")
        else:
            messagebox.showerror("Error", "Could not fetch deadlines.")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

def delete_deadline():
    deadline_id = delete_entry.get().strip()
    if not deadline_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric Deadline ID.")
        return

    try:
        response = requests.delete(f"{API_URL}{deadline_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Deadline deleted!")
            delete_entry.delete(0, tk.END)
            show_deadlines()
        else:
            messagebox.showerror("Error", "Deadline not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



def check_overdue_deadlines():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            today = datetime.today().date()

            overdue = []
            for d in data:
                try:
                    due_date = datetime.strptime(d['due_date'], "%Y-%m-%d").date()
                    if due_date < today:
                        overdue.append(d)
                except:
                    continue

            if overdue:
                msg = "⚠️ Overdue Deadlines:\n\n"
                for d in overdue:
                    msg += f"🔹 {d['title']} (Due: {d['due_date']})\n"
                messagebox.showwarning("Overdue Alert!", msg)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_deadlines():
    try:
        response = requests.get("http://127.0.0.1:8001/deadlines/")
        data = response.json()
        
        # Clear the textbox before showing fresh data
        display_box.delete("1.0", END)

        if not data:
            display_box.insert(END, "No deadlines found.\n")
            return

        for item in data:
            display_box.insert(END, f"ID: {item['id']}\n")
            display_box.insert(END, f"Title: {item['title']}\n")
            display_box.insert(END, f"Due Date: {item['due_date']}\n")
            display_box.insert(END, f"Description: {item['description']}\n")
            display_box.insert(END, "-"*40 + "\n")
    
    except Exception as e:
        display_box.insert(END, f"Error: {e}")

def check_due_today():
    try:
        response = requests.get("http://127.0.0.1:8000/due-today")
        if response.status_code == 200:
            deadlines = response.json()
            if deadlines:
                for d in deadlines:
                    messagebox.showinfo("⏰ Reminder!", f"Today is the deadline!\n\n📝 Title: {d['title']}\n📄 Description: {d['description']}")
    except Exception as e:
        print("Error while checking today's deadlines:", e)


# ------------------- Buttons -------------------
tk.Button(root, text="➕ Add Deadline", font=font_button, bg="#cc0066", fg="white", padx=10, pady=5, command=add_deadline).pack(pady=10)
tk.Button(root, text="📋 Show All Deadlines", font=font_button, bg="#3366cc", fg="white", command=show_deadlines).pack(pady=10)
tk.Button(root, text="❌ Delete Deadline", font=font_button, bg="#cc0000", fg="white", command=delete_deadline).pack(pady=10)
view_btn = Button(window, text="📋 View All Deadlines", command=view_deadlines, font=("Comic Sans MS", 12, "bold"))
view_btn.pack(pady=5)
# ------------------- Run -------------------
check_overdue_deadlines()
check_due_today() 
root.mainloop()

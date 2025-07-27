mport tkinter as tk
from tkinter import messagebox, ttk
import os

TASKS_FILE = "tasks.txt"
tasks = []

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(f"{task['done']}|{task['text']}\n")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return
    with open(TASKS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if '|' not in line:
                continue  # skip malformed lines
            done, text = line.split("|", 1)
            add_task(text, done == '1')


def add_task(text=None, done=False):
    task_text = text if text else task_entry.get().strip()
    if not task_text:
        messagebox.showwarning("Empty Task", "Please enter a task!")
        return

    var = tk.BooleanVar(value=done)
    check = tk.Checkbutton(task_frame, text=task_text, variable=var, bg="#1e1e1e", fg="white", anchor="w", selectcolor="#1e1e1e", activebackground="#1e1e1e")
    check.pack(fill="x", padx=10, pady=2)

    tasks.append({'text': task_text, 'done': var})
    if not text:
        task_entry.delete(0, tk.END)
    save_tasks()

def delete_completed():
    for i in reversed(range(len(tasks))):
        if tasks[i]['done'].get():
            tasks[i]['done'].set(False)
            task_frame.winfo_children()[i].destroy()
            del tasks[i]
    save_tasks()

# --- UI Setup ---
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")
root.config(bg="#1e1e1e")

# Title
tk.Label(root, text="To-Do List", font=("Arial", 16), fg="white", bg="#1e1e1e").pack(pady=10)

# Task Entry
task_entry = tk.Entry(root, font=("Arial", 14), width=25, bg="#2e2e2e", fg="white", insertbackground="white")
task_entry.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Task", command=add_task, width=12, bg="#007acc", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Done", command=delete_completed, width=12, bg="#e06c75", fg="white").grid(row=0, column=1, padx=5)

# Scrollable Task Frame
canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#1e1e1e")

task_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(10,0))
scrollbar.pack(side="right", fill="y")

# Load previous tasks
load_tasks()

root.mainloop()

import os
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

# ---------- File Operations ----------
def create_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filename:
        try:
            with open(filename, "x") as f:
                messagebox.showinfo("Success", f"File {filename} created successfully!")
            refresh_file_list()
        except FileExistsError:
            messagebox.showwarning("Warning", f"File {filename} already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def view_all_files():
    file_list.delete(0, tk.END)
    files = os.listdir()
    if not files:
        messagebox.showinfo("Info", "No files exist in this directory.")
    else:
        for file in files:
            file_list.insert(tk.END, file)

def delete_file():
    selection = file_list.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a file to delete!")
        return
    filename = file_list.get(selection[0])
    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {filename}?")
    if confirm:
        try:
            os.remove(filename)
            messagebox.showinfo("Success", "File deleted successfully.")
            refresh_file_list()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def read_file():
    selection = file_list.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a file to read!")
        return
    filename = file_list.get(selection[0])
    try:
        with open(filename, "r") as f:
            content = f.read()
        show_content_window(filename, content, editable=False)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def edit_file():
    selection = file_list.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a file to edit!")
        return
    filename = file_list.get(selection[0])
    try:
        with open(filename, "r") as f:
            content = f.read()
        show_content_window(filename, content, editable=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Helper ----------
def refresh_file_list():
    file_list.delete(0, tk.END)
    for file in os.listdir():
        file_list.insert(tk.END, file)

def show_content_window(filename, content, editable):
    win = tk.Toplevel(root)
    win.title(f"{'Edit' if editable else 'Read'}: {filename}")
    win.geometry("500x400")
    win.configure(bg="#f4f6f7")

    text_area = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Segoe UI", 12))
    text_area.insert(tk.END, content)
    if not editable:
        text_area.configure(state="disabled")
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    if editable:
        def save_changes():
            with open(filename, "w") as f:
                f.write(text_area.get("1.0", tk.END))
            messagebox.showinfo("Success", "Changes saved successfully!")
            win.destroy()
        save_btn = tk.Button(win, text="💾 Save Changes", command=save_changes, bg="#2ecc71", fg="white", font=("Segoe UI", 12, "bold"))
        save_btn.pack(pady=5)

# ---------- UI Setup ----------
root = tk.Tk()
root.title("📂 File Management App")
root.geometry("700x500")
root.configure(bg="#f4f6f7")

title = tk.Label(root, text="📂 File Management App", font=("Segoe UI", 18, "bold"), bg="#f4f6f7", fg="#2c3e50")
title.pack(pady=15)

# Buttons
btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=10)

btn_style = {"font": ("Segoe UI", 12, "bold"), "width": 18, "height": 2, "relief": "flat", "bd": 0, "cursor": "hand2"}

create_btn = tk.Button(btn_frame, text="➕ Create File", command=create_file, bg="#3498db", fg="white", **btn_style)
create_btn.grid(row=0, column=0, padx=10, pady=5)

view_btn = tk.Button(btn_frame, text="📑 View All Files", command=view_all_files, bg="#2ecc71", fg="white", **btn_style)
view_btn.grid(row=0, column=1, padx=10, pady=5)

read_btn = tk.Button(btn_frame, text="📖 Read File", command=read_file, bg="#9b59b6", fg="white", **btn_style)
read_btn.grid(row=1, column=0, padx=10, pady=5)

edit_btn = tk.Button(btn_frame, text="✏️ Edit File", command=edit_file, bg="#f39c12", fg="white", **btn_style)
edit_btn.grid(row=1, column=1, padx=10, pady=5)

delete_btn = tk.Button(btn_frame, text="🗑️ Delete File", command=delete_file, bg="#e74c3c", fg="white", **btn_style)
delete_btn.grid(row=2, column=0, columnspan=2, pady=10)

# File list
file_list = tk.Listbox(root, width=80, height=12, font=("Segoe UI", 11))
file_list.pack(pady=10)

refresh_file_list()

# ---------- Hover Effects ----------
def on_enter(e): e.widget.config(bg="#1abc9c")
def on_leave(e):
    if e.widget == create_btn: e.widget.config(bg="#3498db")
    elif e.widget == view_btn: e.widget.config(bg="#2ecc71")
    elif e.widget == read_btn: e.widget.config(bg="#9b59b6")
    elif e.widget == edit_btn: e.widget.config(bg="#f39c12")
    elif e.widget == delete_btn: e.widget.config(bg="#e74c3c")

for b in (create_btn, view_btn, read_btn, edit_btn, delete_btn):
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

root.mainloop()

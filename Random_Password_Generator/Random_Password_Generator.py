import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    password_text.delete(1.0, tk.END)
    password_text.insert(tk.END, password)
    password_text.tag_add("center", "1.0", "end")

root = tk.Tk()
root.title("Random Password Generator")

logo = tk.PhotoImage(file="logo.png")
background_label = tk.Label(root, image=logo)
background_label.place(relwidth=1, relheight=1)

password_text = tk.Text(root, height=1, font=("Helvetica", 24), bg="white", bd=0, highlightthickness=0, wrap="none")
password_text.tag_configure("center", justify='center')
password_text.place(relx=0.5, rely=0.67, anchor=tk.CENTER, width=400)

generate_btn = tk.Button(
    root, text="Generate Password", command=generate_password,
    bg="white", font=("Helvetica", 24), width=20, height=2, padx=20, pady=20
)
generate_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()
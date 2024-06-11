import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        result.set(f"BMI: {bmi}")

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        
        messagebox.showinfo("BMI Result", f"Your BMI is {bmi} which is considered {category}.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

root = tk.Tk()
root.title("BMI Calculator")

root.geometry("400x300")

root.configure(bg="#f0f0f0")

result = tk.StringVar()

font_label = ('Helvetica', 14)
font_entry = ('Helvetica', 14)
font_button = ('Helvetica', 14, 'bold')
font_result = ('Helvetica', 16)

logo = tk.PhotoImage(file="unnamed.png")
label_logo = tk.Label(root, image=logo, bg="#f0f0f0")
label_logo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

label_weight = tk.Label(root, text="Weight (kg):", font=font_label, bg="#f0f0f0")
label_weight.place(relx=0.3, rely=0.35, anchor=tk.E)
entry_weight = tk.Entry(root, font=font_entry)
entry_weight.place(relx=0.5, rely=0.35, anchor=tk.W)

label_height = tk.Label(root, text="Height (m):", font=font_label, bg="#f0f0f0")
label_height.place(relx=0.3, rely=0.45, anchor=tk.E)
entry_height = tk.Entry(root, font=font_entry)
entry_height.place(relx=0.5, rely=0.45, anchor=tk.W)

btn_calculate = tk.Button(root, text="Calculate BMI", font=font_button, command=calculate_bmi)
btn_calculate.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

label_result = tk.Label(root, textvariable=result, font=font_result, bg="#f0f0f0")
label_result.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

root.mainloop()
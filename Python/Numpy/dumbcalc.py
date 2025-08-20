from tkinter import * 
from tkinter import messagebox 
import numpy as np 

def calc():
    try:
        # Get values from entry boxes
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()

        # Use NumPy for calculations
        if operation == "Add":
            result = np.add(num1, num2)
        elif operation == "Subtract":
            result = np.subtract(num1, num2)
        elif operation == "Multiply":
            result = np.multiply(num1, num2)
        elif operation == "Divide":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                return
            result = np.divide(num1, num2)
        else:
            messagebox.showerror("Error", "Select an operation!")
            return

        # Display result
        result_label.config(text=f"Result: {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")



window = Tk()
window.geometry("360x440")

Label(window, text="Enter Fist Number:").pack()
entry1 = Entry(window)
entry1.pack(fill=BOTH)

Label(window, text="Enter Second Number:").pack()
entry2 = Entry(window)
entry2.pack(fill=BOTH)

operation_var = StringVar()
operation_var.set("Add")

operations = ["Add", "Subtract", "Multiply", "Divide"]
OptionMenu(window, operation_var, *operations).pack()

Button(window, text="Calculate", command=calc).pack()

result_label = Label(window, text="Result:", font=("Arial", 20))
result_label.pack()

window.mainloop()

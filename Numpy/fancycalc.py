from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import numpy as np 

last_answer = None #Sets last_answer as Null at first. 

def calc(): 
    global last_answer
    expr = entry.get()

    try: 
        expr = expr.replace("x", "*")
        expr = expr.replace("^", "**")
        expr = expr.replace("pi", "np.pi")
        expr = expr.replace("sqrt", "np.sqrt")
        expr = expr.replace("Ans", str(last_answer) if last_answer is not None else "0")


        result = eval(expr, {"np": np, "__builtins__": {}})

        last_answer = result 

        result_label.config(text=f"Result: {result}")

    except Exception as e: 
      messagebox.showerror("Error", f"Invalid Expression!\n{e}")


def SI(): 
   global last_answer
   if last_answer is None: 
      messagebox.showinfo("Info", "No Previous Answer To Format")
      return 
   sci_results = np.format_float_scientific(last_answer, precision=2, exp_digits=2)
   result_label.config(text=f"Result: {sci_results}")

window = Tk()
window.title("Calculatror+")
window.geometry("360x440")

Label(window, text="Enter Expressions:").pack()
entry = Entry(window, width=40)
entry.pack(fill=BOTH)

Calculate = Button(window, text="Calculate", command=calc)
Calculate.pack()
Scientific_Notation = Button(window, text="Convert To S.I", command=SI)
Scientific_Notation.pack()

result_label = Label(window, text="Results:", font=("Comfortaa", 20,))
result_label.pack()

options = ("+", "-", "x", "^", "pi", "sqrt()", "Ans",)

combo_box = ttk.Combobox(window, values=options)
combo_box.pack()

window.mainloop()
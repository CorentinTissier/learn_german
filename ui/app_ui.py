import tkinter as tk
from logic.declension_logic import check_declension

def submit_answer():
    determinant = determinant_entry.get()
    case = case_entry.get()
    answer = answer_entry.get()

    if check_declension(determinant, case, answer):
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Incorrect.", fg="red")

root = tk.Tk()
root.title("German Declension Practice")

tk.Label(root, text="Determinant (der/die/das):").pack()
determinant_entry = tk.Entry(root)
determinant_entry.pack()

tk.Label(root, text="Case (nominative/accusative/dative/genitive):").pack()
case_entry = tk.Entry(root)
case_entry.pack()

tk.Label(root, text="Your Answer:").pack()
answer_entry = tk.Entry(root)
answer_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit_answer)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
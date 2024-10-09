import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd

import depersonalization_functions as fu

items = ["ФИО", "Паспортные данные", "Откуда", "Куда", "Дата отъезда", "Дата приезда", "Рейс", "Выбор вагона и места",
         "Стоимость", "Карта оплаты"]

quasi_ident = {item: False for item in items}
filename = ""
root = tk.Tk()
root.title("Деанонимизация")
root.geometry("800x600")

main_menu = tk.Menu(root)


def close_window():
    root.quit()


def print_result(var: tk.BooleanVar, item: str):
    state: bool = var.get()
    quasi_ident[item] = state


def open_file_explorer():
    global filename
    filename = filedialog.askopenfilename(
        initialdir="'D:\python_projects",
        title="Выберите файл",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
    )
    input_file_name.config(text=filename)


def show_popup(message):
    messagebox.showinfo("Информация", message)


def depersonalize_and_notify():
    if not filename:
        show_popup("Выберите файл перед расчетом K-anonymity!")
        return
    fu.depersonalize_data(quasi_ident, filename)
    show_popup("Обезлично! файл: depersonalized_data.xlsx")


def calculate_k_anonymity():
    if not filename:
        show_popup("Выберите файл перед расчетом K-anonymity!")
        return

    try:
        k_anonymity, unique_rows, worst_k_values = fu.calculate_k_anonymity(quasi_ident, filename)
        show_unique_k_anonymity(unique_rows)
        show_worst_k_anonymity(worst_k_values)
        show_popup(f'K-anonymity набора данных: {k_anonymity}')

    except Exception as e:
        show_popup(f"Ошибка при расчете K-anonymity!: {str(e)}")


def show_unique_k_anonymity(unique_rows: pd.DataFrame):
    try:
        result_window = tk.Toplevel(root)
        result_window.title("Уникальные ряды")

        for index, row in unique_rows.iterrows():
            row_data = ', '.join([f"{col}: {row[col]}" for col in unique_rows.columns])
            tk.Label(result_window, text=row_data).pack(anchor="w")

        if len(unique_rows) == 0:
            tk.Label(result_window, text="K-anonymity больше 1").pack()

    except Exception as e:
        messagebox.showinfo("ОШИБКА!", f"ОШИБКА!: {str(e)}")


def show_worst_k_anonymity(worst_k_anon: pd.DataFrame):
    try:
        for index, row in worst_k_anon.iterrows():

            tk.Label(root,
                     text=f'K-anonymity: {row["counts"]}, процент: {row["percentage"]}%').pack(
                anchor="e")

    except Exception as e:
        messagebox.showinfo("ОШИБКА!", f"ОШИБКА!: {str(e)}")


main_menu.add_cascade(label="Сохранить")
main_menu.add_cascade(label="Рассчитать K-anonymity", command=calculate_k_anonymity)
main_menu.add_cascade(label="Обезличить", command=depersonalize_and_notify)
main_menu.add_cascade(label="Выход", command=close_window)

quasi_lbl = tk.Label(text="Выберите квази идентификаторы", font=("Helvetica", 16, "bold"))
quasi_lbl.pack(anchor="nw")

for item in items:
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text=item, variable=checkbox_var,
                              command=lambda var=checkbox_var, label=item: print_result(var, label))
    checkbox.pack(anchor="w")

input_file_name_lbl = tk.Label(text="Имя файла ввода", font=("Helvetica", 16, "bold"))
input_file_name_lbl.pack(anchor="w")
input_file_name = tk.Label(text=filename)
input_file_name.pack(anchor="w")
worst_k_anon_lbl = tk.Label(text="Худший K-anonymity", font=("Helvetica", 16, "bold"))
worst_k_anon_lbl.pack(anchor="e")
button_explore = tk.Button(root, text="Выбрать файл", command=open_file_explorer)
button_explore.pack(side=tk.LEFT)

root.config(menu=main_menu)

root.mainloop()

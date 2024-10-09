import tkinter as tk

import config as c
import main

root = tk.Tk()
root.title("Доля банков и платёжных систем")

bank_sliders = {}
payment_sliders = {}

bank_frame = tk.LabelFrame(root, text="Банки")
bank_frame.pack()
payment_frame = tk.LabelFrame(root, text="Платёжные системы")
payment_frame.pack()


def update_prob_payment_system(val):
    total_prob = 0
    for payment_system_name in c.payment_systems:
        total_prob += payment_sliders[payment_system_name].get()
        if total_prob > 100:
            excess = total_prob - 100
            for payment_systems in c.payment_systems:
                if excess <= 0:
                    break
                current_value = payment_sliders[payment_systems].get()
                if current_value > 0:
                    decrease = min(current_value, excess)
                    payment_sliders[payment_systems].set(current_value - decrease)
                    excess -= decrease


def update_prob_bank(val):
    total_prob = 0
    for bank_name in c.banks:
        total_prob += bank_sliders[bank_name].get()

    if total_prob > 100:
        excess = total_prob - 100

        for banki in c.banks:
            if excess <= 0:
                break
            current_value = bank_sliders[banki].get()
            if current_value > 0:
                decrease = min(current_value, excess)
                bank_sliders[banki].set(current_value - decrease)
                excess -= decrease


for bank in c.banks:
    label = tk.Label(bank_frame, text=bank)
    label.pack(anchor='w')
    slider = tk.Scale(bank_frame, from_=0, to=100, orient='horizontal', command=update_prob_bank)
    slider.set(100 // len(c.banks))
    slider.pack(fill='x')
    bank_sliders[bank] = slider

for payment_system in c.payment_systems:
    label = tk.Label(payment_frame, text=payment_system)
    label.pack(anchor='w')
    slider = tk.Scale(payment_frame, from_=0, to=100, orient='horizontal', command=update_prob_payment_system)
    slider.set(100 // len(c.payment_systems))
    slider.pack(fill='x')
    payment_sliders[payment_system] = slider

num_of_people_slider = tk.Scale(root, from_=50000, to=250000, orient='horizontal', label="Выбрать количество людей")
num_of_people_slider.set(c.num_of_people)
num_of_people_slider.pack(fill='x')

create_file_btn = tk.Button(root, text="создать файл с данными значениями",
                            command=lambda: main.generate_data(bank_sliders["Сбер"].get(), bank_sliders["ВТБ"].get(),
                                                               payment_sliders["Visa"].get(),
                                                               payment_sliders["Mastercard"].get(),
                                                               num_of_people_slider.get()))
create_file_btn.pack()
root.mainloop()

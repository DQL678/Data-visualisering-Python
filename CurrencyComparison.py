import tkinter as tk
from tkinter import ttk
import requests


def open_currency_comparison():
    def compare():
        c1 = var1.get()
        c2 = var2.get()
        if c1 == c2:
            result_label.config(text="Valutaerne er ens. Kurs: 1.0")
            return
        try:
            url = f"https://api.frankfurter.dev/v1/latest?base={c1}&symbols={c2}"
            data = requests.get(url).json()
            rate = data['rates'][c2]
            result_label.config(text=f"1 {c1} = {rate} {c2}\nDato: {data['date']}")
        except Exception as e:
            result_label.config(text="Fejl: " + str(e))

    # Valutaer fra currency_info inkl. DKK
    available_currencies = ["DKK", "EUR", "GBP", "AUD", "USD", "JPY", "CNY"]

    # Vindue
    win = tk.Tk()
    win.title("Currency Comparison")
    win.geometry("450x200")

    var1 = tk.StringVar(value=available_currencies[0])
    var2 = tk.StringVar(value=available_currencies[1])

    dropdown1 = ttk.Combobox(win, textvariable=var1, values=available_currencies, state="readonly")
    dropdown1.grid(row=0, column=0, padx=10, pady=10)

    dropdown2 = ttk.Combobox(win, textvariable=var2, values=available_currencies, state="readonly")
    dropdown2.grid(row=0, column=1, padx=10, pady=10)

    compare_btn = tk.Button(win, text="Compare", command=compare)
    compare_btn.grid(row=1, column=0, columnspan=2, pady=10)

    result_label = tk.Label(win, text="", font=("Arial", 12))
    result_label.grid(row=2, column=0, columnspan=2, pady=10)

    win.mainloop()

# Kør standalone
if __name__ == "__main__":
    open_currency_comparison()

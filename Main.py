import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import datetime

# --- Funktion: Åbn vindue for Currency Information ---
def open_currency_info():
    compare_currency = "USD"
    FLAG_SIZE = (120, 80)
    CURRENCY_IMG_SIZE = (200, 100)
    available_currencies = ["DKK","EUR", "GBP", "AUD", "CAD", "USD", "JPY", "CNY"]

    window = tk.Toplevel()
    window.title("Facts about currency")
    window.geometry("380x500")

    flag_label = tk.Label(window)
    flag_label.pack(pady=8)

    currency_label = tk.Label(window)
    currency_label.pack(pady=8)

    title_label = tk.Label(window, text="Currency Facts", font=("Arial", 16, "bold"))
    title_label.pack(pady=5)

    currency_text = tk.Label(window, font=("Arial", 12))
    currency_text.pack()

    rate_text = tk.Label(window, font=("Arial", 12))
    rate_text.pack(pady=6)

    date_text = tk.Label(window, font=("Arial", 10))
    date_text.pack(pady=4)

    selected_currency = tk.StringVar(value=available_currencies[0])
    dropdown = ttk.Combobox(window, textvariable=selected_currency, values=available_currencies, state="readonly")
    dropdown.pack(pady=10)

    def update_currency(base_currency):
        try:
            if base_currency == compare_currency:
                rate = 1
                date = "N/A"
            else:
                url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}&symbols={compare_currency}"
                data = requests.get(url).json()
                rate = data["rates"][compare_currency]
                date = data["date"]

            flag_path = f"flags/{base_currency.lower()}.png"
            flag_img = Image.open(flag_path).resize(FLAG_SIZE)
            flag_photo = ImageTk.PhotoImage(flag_img)
            flag_label.config(image=flag_photo)
            flag_label.image = flag_photo

            currency_path = f"currency_images/{base_currency.lower()}_note.png"
            currency_img = Image.open(currency_path).resize(CURRENCY_IMG_SIZE)
            currency_photo = ImageTk.PhotoImage(currency_img)
            currency_label.config(image=currency_photo)
            currency_label.image = currency_photo

            currency_text.config(text=f"Currency: {base_currency}")
            rate_text.config(text=f"Exchange Rate:\n1 {base_currency} = {rate} {compare_currency}")
            date_text.config(text=f"Rate Date: {date}")

        except Exception as e:
            currency_text.config(text="Error fetching data")
            rate_text.config(text=str(e))
            date_text.config(text="")

    def on_currency_change(event):
        update_currency(selected_currency.get())

    dropdown.bind("<<ComboboxSelected>>", on_currency_change)

    def resize_fonts(event):
        scale = event.width / 380
        min_font = 8
        title_label.config(font=("Arial", max(int(16 * scale), min_font), "bold"))
        currency_text.config(font=("Arial", max(int(12 * scale), min_font)))
        rate_text.config(font=("Arial", max(int(12 * scale), min_font)))
        date_text.config(font=("Arial", max(int(10 * scale), min_font)))

    window.bind("<Configure>", resize_fonts)
    update_currency(selected_currency.get())

# --- Funktion: Åbn vindue og vis valutagraf ---
def open_currency_graph():
    def date_to_days(date_string, reference_date):
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        ref = datetime.datetime.strptime(reference_date, "%Y-%m-%d")
        return (date - ref).days

    def format_json(data):
        start = data["start_date"]
        rates = {}
        for key in data["rates"]:
            rates[date_to_days(key, start)] = data["rates"][key]
        return {
            "rates": rates,
            "start": start,
            "end": data["end_date"],
            "base": data["base"]
        }

    def get_data(valutas, base):
        url = f"https://api.frankfurter.dev/v1/1999-01-01..?base={base}&symbols={','.join(valutas)}"
        response = requests.get(url)
        data = response.json()
        return format_json(data)

    valutas = ["USD", "DKK", "GBP"]
    base = "AUD"
    data = get_data(valutas, base)

    plt.figure(figsize=(10,5))
    for valuta in valutas:
        xs = []
        ys = []
        for day, rate_dict in data["rates"].items():
            xs.append(day)
            ys.append(rate_dict[valuta])
        plt.plot(xs, ys, label=valuta)

    plt.title(f"Valutakurser relativt til {base}")
    plt.xlabel("Dage siden startdato")
    plt.ylabel("Kurs")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Funktion: Sammenlign to valutaer ---
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

    available_currencies = ["DKK","EUR", "GBP", "AUD", "CAD", "USD", "JPY", "CNY" ]

    win = tk.Toplevel()
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

# --- STARTMENU ---
root = tk.Tk()
root.title("Startmenu")
root.geometry("300x200")

overskrift = tk.Label(root, text="Welcome to the currency visualization app", font=("Arial", 12))
overskrift.pack(pady=10)

knap1 = tk.Button(root, text="Currency Information", command=open_currency_info)
knap1.pack(pady=5)

knap2 = tk.Button(root, text="Currency Comparison", command=open_currency_comparison)
knap2.pack(pady=5)

knap3 = tk.Button(root, text="Currency Visualization", command=open_currency_graph)
knap3.pack(pady=5)

root.mainloop()
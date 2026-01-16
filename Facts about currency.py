import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk

# Used https://flagcdn.com/h60/us.png for flag images and Google for currency images

# --- Size and options ---
compare_currency = "USD"  # Fixed currency to compare to
FLAG_SIZE = (120, 80)
CURRENCY_IMG_SIZE = (200, 100)

available_currencies = ["DKK","EUR", "GBP", "AUD", "USD", "JPY", "CNY", ]  # Currency options in drop-menu

# --- Window ---
window = tk.Tk()
window.title("Facts about currency")
window.geometry("380x500")

# --- Flag and currency image ---
flag_label = tk.Label(window)
flag_label.pack(pady=8)

currency_label = tk.Label(window)
currency_label.pack(pady=8)

# --- Text ---
title_label = tk.Label(window, text="Currency Facts", font=("Arial", 16, "bold"))
title_label.pack(pady=5)

currency_text = tk.Label(window, font=("Arial", 12))
currency_text.pack()

rate_text = tk.Label(window, font=("Arial", 12))
rate_text.pack(pady=6)

date_text = tk.Label(window, font=("Arial", 10))
date_text.pack(pady=4)

# --- Update Info ---
def update_currency(base_currency):
    try:
        if base_currency == compare_currency:
            # If base and compare are the same, rate is 1:1
            rate = 1
            date = "N/A"

        else:
            # Fetch API data
            url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}&symbols={compare_currency}"
            data = requests.get(url).json()
            rate = data["rates"][compare_currency]
            date = data["date"]

        # --- Update flag image ---
        flag_path = f"flags/{base_currency.lower()}.png"
        flag_img = Image.open(flag_path).resize(FLAG_SIZE)
        flag_photo = ImageTk.PhotoImage(flag_img)
        flag_label.config(image=flag_photo)
        flag_label.image = flag_photo

        # --- Update currency image ---
        currency_path = f"currency_images/{base_currency.lower()}_note.png"
        currency_img = Image.open(currency_path).resize(CURRENCY_IMG_SIZE)
        currency_photo = ImageTk.PhotoImage(currency_img)
        currency_label.config(image=currency_photo)
        currency_label.image = currency_photo

        # --- Update text ---
        currency_text.config(text=f"Currency: {base_currency}")
        rate_text.config(text=f"Exchange Rate:\n1 {base_currency} = {rate} {compare_currency}")
        date_text.config(text=f"Rate Date: {date}")

    except Exception as e:
        currency_text.config(text="Error grabbing data")
        rate_text.config(text=str(e))
        date_text.config(text="")

# --- Dropdown-menu ---
selected_currency = tk.StringVar(value=available_currencies[0])
dropdown = ttk.Combobox(window, textvariable=selected_currency, values=available_currencies, state="readonly")
dropdown.pack(pady=10)

# Change of currency, update info
def on_currency_change(event):
    update_currency(selected_currency.get())

dropdown.bind("<<ComboboxSelected>>", on_currency_change)

# --- Initial update ---
update_currency(selected_currency.get())

window.mainloop()
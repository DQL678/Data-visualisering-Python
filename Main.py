import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk

# --- Funktion: Åbn vindue for Currency Information ---
def open_currency_info():
    # --- Nyttige konstanter ---
    compare_currency = "USD"
    FLAG_SIZE = (120, 80)
    CURRENCY_IMG_SIZE = (200, 100)
    available_currencies = ["EUR", "GBP", "AUD", "USD"]

    # --- Nyt vindue (ikke nyt Tk-vindue!) ---
    window = tk.Toplevel()
    window.title("Facts about currency")
    window.geometry("380x500")

    # --- GUI-elementer ---
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

    # --- Dropdown menu ---
    selected_currency = tk.StringVar(value=available_currencies[0])
    dropdown = ttk.Combobox(window, textvariable=selected_currency, values=available_currencies, state="readonly")
    dropdown.pack(pady=10)

    # --- Funktion til opdatering af valuta-info ---
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

            # Flag-billede
            flag_path = f"flags/{base_currency.lower()}.png"
            flag_img = Image.open(flag_path).resize(FLAG_SIZE)
            flag_photo = ImageTk.PhotoImage(flag_img)
            flag_label.config(image=flag_photo)
            flag_label.image = flag_photo

            # Valuta-billede
            currency_path = f"currency_images/{base_currency.lower()}_note.png"
            currency_img = Image.open(currency_path).resize(CURRENCY_IMG_SIZE)
            currency_photo = ImageTk.PhotoImage(currency_img)
            currency_label.config(image=currency_photo)
            currency_label.image = currency_photo

            # Tekster
            currency_text.config(text=f"Currency: {base_currency}")
            rate_text.config(text=f"Exchange Rate:\n1 {base_currency} = {rate} {compare_currency}")
            date_text.config(text=f"Rate Date: {date}")

        except Exception as e:
            currency_text.config(text="Error fetching data")
            rate_text.config(text=str(e))
            date_text.config(text="")

    # --- Dropdown opdatering ---
    def on_currency_change(event):
        update_currency(selected_currency.get())

    dropdown.bind("<<ComboboxSelected>>", on_currency_change)

    # --- Skaler skrifttyper når vinduet ændres ---
    def resize_fonts(event):
        scale = event.width / 380
        min_font = 8
        title_label.config(font=("Arial", max(int(16 * scale), min_font), "bold"))
        currency_text.config(font=("Arial", max(int(12 * scale), min_font)))
        rate_text.config(font=("Arial", max(int(12 * scale), min_font)))
        date_text.config(font=("Arial", max(int(10 * scale), min_font)))

    window.bind("<Configure>", resize_fonts)

    # Startvisning
    update_currency(selected_currency.get())

# --- STARTMENU ---
root = tk.Tk()
root.title("Startmenu")
root.geometry("300x200")

overskrift = tk.Label(root, text="Welcome to the currency visualization app", font=("Arial", 12))
overskrift.pack(pady=10)

# Knap 1 - Åbner valutainformation
knap1 = tk.Button(root, text="Currency Information", command=open_currency_info)
knap1.pack(pady=5)

# Knap 2 og 3 (midlertidigt tomme)
knap2 = tk.Button(root, text="Currency Comparison")
knap2.pack(pady=5)

knap3 = tk.Button(root, text="Currency Visualization")
knap3.pack(pady=5)

root.mainloop()

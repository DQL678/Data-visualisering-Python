import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import datetime
import os
from FactsAboutCurrency import open_currency_info
from CurrencyComparison import open_currency_comparison
from Graph import open_currency_graph


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
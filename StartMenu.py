import tkinter as tk

# Vinduet oprettes
root = tk.Tk()
root.title("Startmenu")
root.geometry("300x200")

# Overskrift oprettes
overskrift = tk.Label(root, text="Welcome to the currency visualization app", font=("Arial", 12))
overskrift.pack(pady=10)

# Knap 1
knap1 = tk.Button(root, text="Currency Information")
knap1.pack(pady=5)

# Knap 2
knap2 = tk.Button(root, text="Currency Comparison")
knap2.pack(pady=5)

# Knap 3
knap3 = tk.Button(root, text="Currency Visualization")
knap3.pack(pady=5)

# Dette kører vinduet
root.mainloop()
import matplotlib.pyplot as plt
import requests
import datetime

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

# Liste of alle valutaer
def get_supported_currencies():
    url2 = "https://api.frankfurter.dev/v1/currencies"
    response = requests.get(url2)
    return response.json()

currencies = get_supported_currencies()
for code, name in currencies.items():
    print(f"{code}: {name}")
# Slut liste

valutas = ["USD", "DKK", "GBP"]
base = input("Indtast basisvaluta (fx EUR, USD, AUD): ").upper()
data = get_data(valutas, base)

# Lidt info
print("Base:", data["base"])
print("Start:", data["start"])
print("End:", data["end"])

# Plot valutakurser
plt.figure(figsize=(10,5))

for valuta in valutas:
    xs = []
    ys = []
    for day, rate_dict in data["rates"].items():
        xs.append(day)
        ys.append(rate_dict[valuta])
    plt.plot(xs, ys, label=valuta)

plt.title(f"Valutakurser relativt til {base}", fontsize=15)
plt.xlabel("Dage siden startdato", fontsize = 12)
plt.ylabel("Kurs", fontsize = 12)
plt.legend()
plt.grid(True)
plt.show()



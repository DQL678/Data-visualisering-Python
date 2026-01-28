import matplotlib.pyplot as plt
import requests
import datetime

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
        # Fjern basisvaluta hvis den findes i listen
        if base in valutas:
            valutas = [v for v in valutas if v != base]

        url = f"https://api.frankfurter.dev/v1/1999-01-01..?base={base}&symbols={','.join(valutas)}"
        response = requests.get(url)
        data = response.json()
        return format_json(data), valutas

    def get_supported_currencies():
        url2 = "https://api.frankfurter.dev/v1/currencies"
        response = requests.get(url2)
        return response.json()

    # Udskriv alle valutaer
    currencies = get_supported_currencies()
    for code, name in currencies.items():
        print(f"{code}: {name}")

    # Brugeren vælger selv valutaer
    valuta_input = input("Indtast valutaer der skal sammenlignes (fx USD, DKK, GBP): ")
    valutas = [v.strip().upper() for v in valuta_input.split(",")]

    # Brugeren vælger basisvaluta
    base = input("Indtast kun 1 basisvaluta (fx EUR, USD, AUD): ").upper()

    # Hent data og opdateret valutaliste
    data, valutas = get_data(valutas, base)

    # Fjern valutaer der slet ikke findes i API-data
    valutas = [v for v in valutas if any(v in r for r in data["rates"].values())]

    # Lidt info
    print("Base:", data["base"])
    print("Start:", data["start"])
    print("End:", data["end"])

    # Plot valutakurser
    plt.figure(figsize=(10, 5))

    for valuta in valutas:
        xs = []
        ys = []
        for day, rate_dict in data["rates"].items():
            if valuta not in rate_dict:
                continue  # spring dage uden data over
            xs.append(day)
            ys.append(rate_dict[valuta])

        if xs:  # kun plot hvis der faktisk er data
            plt.plot(xs, ys, label=valuta)

    plt.title(f"Valutakurser relativt til {base}", fontsize=15)
    plt.xlabel("Dage siden 01-04-1999", fontsize=12)
    plt.ylabel("Kurs", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

#lavgrafen() kaldes hvis det her script køres alene:.. Altså hvis __name__ == __main__
if __name__ == "__main__":
    open_currency_graph()

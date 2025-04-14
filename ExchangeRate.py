import requests

def get_exchange_rates(api_url):
    """Fetches the latest exchange rates from the given API URL.

    Args:
        api_url (str): The URL of the exchange rates API.

    Returns:
        dict: A dictionary containing the exchange rates if the request is successful,
              otherwise None.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data.get("success"):
            return data.get("rates")
        else:
            print(f"Error fetching exchange rates: {data.get('error', {}).get('info')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except ValueError:
        print("Error decoding JSON response.")
        return None

def convert_currency(amount, from_currency, to_currency, exchange_rates):
    """Converts an amount from one currency to another using the provided exchange rates.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from (e.g., "USD").
        to_currency (str): The currency to convert to (e.g., "INR").
        exchange_rates (dict): A dictionary of exchange rates with EUR as the base.

    Returns:
        float: The converted amount, or None if the currencies are not found.
    """
    if from_currency not in exchange_rates:
        print(f"Error: Currency '{from_currency}' not found.")
        return None
    if to_currency not in exchange_rates:
        print(f"Error: Currency '{to_currency}' not found.")
        return None

    # If the base currency is EUR
    if from_currency == "EUR":
        converted_amount = amount * exchange_rates[to_currency]
    elif to_currency == "EUR":
        converted_amount = amount / exchange_rates[from_currency]
    else:
        # Convert to EUR first, then to the target currency
        amount_in_eur = amount / exchange_rates[from_currency]
        converted_amount = amount_in_eur * exchange_rates[to_currency]

    return converted_amount

def main():
    """Main function to run the currency converter app."""
    api_url = "http://api.exchangeratesapi.io/v1/latest?access_key=ab5436a1add8391359833bd1e44c35c5"
    exchange_rates = get_exchange_rates(api_url)

    if not exchange_rates:
        return

    print("Welcome to the Simple Currency Converter!")

    while True:
        try:
            amount_str = input("Enter the amount to convert: ")
            amount = float(amount_str)
            if amount < 0:
                print("Amount cannot be negative.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue

        from_currency = input("Enter the currency to convert from (e.g., USD): ").upper()
        to_currency = input("Enter the currency to convert to (e.g., INR): ").upper()

        converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)

        if converted_amount is not None:
            print(f"{amount:.2f} {from_currency} is equal to {converted_amount:.2f} {to_currency}")

        another_conversion = input("Do you want to perform another conversion? (yes/no): ").lower()
        if another_conversion != "yes":
            print("Thank you for using the converter!")
            break

if __name__ == "__main__":
    main()
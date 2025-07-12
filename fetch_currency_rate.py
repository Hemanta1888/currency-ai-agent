import requests
import json
from typing import Dict, Any


def fetch_exchange_rate(to_currency: str) -> float:
    """
    Fetches the current exchange rate from USD to the target currency
    using the Open Exchange Rates API's open access endpoint.

    Args:
        to_currency (str): The three-letter uppercase currency code
                           (e.g., "EUR", "GBP", "JPY") to convert to.

    Returns:
        float: The exchange rate (1 USD = X to_currency).

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: If the API response indicates an error or the
                    target currency rate is not found.
    """
    url = "https://open.er-api.com/v6/latest/USD"


    try:
        response = requests.get(url)
        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        if data.get("result") != "success":
            error_type = data.get("error-type", "unknown_api_error")
            documentation_link = data.get("documentation", "No documentation link provided.")
            raise ValueError(
                f"❌ API returned an error: {error_type}. "
                f"Please check documentation: {documentation_link}"
            )

        rate = data.get("rates", {}).get(to_currency.upper())

        if rate is None:
            supported_currencies = list(data.get("rates", {}).keys())
            raise ValueError(
                f"❌ Exchange rate not found for currency: '{to_currency.upper()}'. "
                f"Supported currencies include: {', '.join(supported_currencies[:5])}... "
                f"Please ensure the currency code is correct."
            )

        return float(rate)

    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"❌ HTTP error occurred: {http_err} - {response.text}") from http_err # type: ignore
    except requests.exceptions.ConnectionError as conn_err:
        raise Exception(f"❌ Network connection error: {conn_err}") from conn_err
    except requests.exceptions.Timeout as timeout_err:
        raise Exception(f"❌ Request timed out: {timeout_err}") from timeout_err
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"❌ An error occurred during the request: {req_err}") from req_err
    except json.JSONDecodeError as json_err:
        raise ValueError(f"❌ Failed to parse JSON response: {json_err}. Response: {response.text}") from json_err # type: ignore
    except ValueError as val_err:
        raise val_err
    except Exception as e:
        raise Exception(f"❌ An unexpected error occurred: {e}") from e


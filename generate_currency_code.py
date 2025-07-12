import vertexai
import requests

from settings import get_settings


from langchain_google_vertexai import VertexAI
from langchain.prompts import ChatPromptTemplate
from functools import lru_cache



settings = get_settings()
vertexai.init(project=settings.project_id, location=settings.location)

model = VertexAI(model_name=settings.gemini_model_name, temperature=0.4)
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that extracts only the 3-letter currency code from the user's message.

Examples:
- Indian currency → INR
- Euro → EUR
- British pounds → GBP

Always respond with ONLY the 3-letter ISO currency code like INR, EUR, GBP.

User: {input_text}
""")


@lru_cache(maxsize=1)
def get_supported_currencies():
    """Fetches the list of supported currencies from the exchange rate API.
    Returns:
        List[str]: A list of supported currency codes.
    """

    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("❌ Failed to fetch currency list.")
    return list(response.json().get("rates", {}).keys())

def get_target_currency(response_msg: str) -> str:
    """Extracts the target currency code from the model response.

    Args:
        response_msg (str): model response text.

    Returns:
        str: The 3-letter ISO currency code.
    """
    
    supported_currencies = get_supported_currencies()
    response = response_msg.upper()
    
    if isinstance(supported_currencies, list):
        for currency_code in supported_currencies:
            if currency_code in response:
                return currency_code
    return "UNKNOWN"

chain = prompt | model | get_target_currency

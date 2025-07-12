from model import PortfolioState
from fetch_currency_rate import fetch_exchange_rate
from generate_currency_code import chain

from langgraph.graph import StateGraph, START, END


def calc_total(state: PortfolioState) -> PortfolioState:
    """Calculate the total amount in the portfolio based on the current state."""
    
    state['total_usd'] = state['usd_amount'] * 1.08
    return state

def convert_currency(state: PortfolioState) -> PortfolioState:
    """Dynamically convert total USD to the target currency."""
    rate = fetch_exchange_rate(state["target_currency"])
    state["total_amount"] = round(state["total_usd"] * rate, 2)
    return state

def decide_currency(state: PortfolioState) -> PortfolioState:
    """Decide the target currency based on user input."""


    llm_response = chain.invoke({"input_text": state['user_input']})

    state['target_currency'] = llm_response
    return state



builder = StateGraph(PortfolioState)
builder.add_node("decide_currency_node", decide_currency)
builder.add_node("calc_total_node", calc_total)
builder.add_node("convert_currency_node", convert_currency)

builder.add_edge(START, "decide_currency_node")
builder.add_edge("decide_currency_node", "calc_total_node")
builder.add_edge("calc_total_node", "convert_currency_node")
builder.add_edge("convert_currency_node", END)

graph = builder.compile()
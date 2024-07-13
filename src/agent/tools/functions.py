import requests
import json

from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool

@tool()
def get_testnet_tokens(receiver: str):
    """Send some Near testnet tokens to a Near receiver address
    Args:
        receiver (str): The receiver of the tokens
    Returns:
        JSON response of the request that contains either a transaction hash (txh) or an error message (error)"""

def get_testnet_tokens_raw(receiver: str):
    response = requests.post(
        "https://near-faucet.io/api/faucet/tokens",
        json={"contractId":"near_faucet","receiverId": receiver,"amount":"10000000000000000000000000"}
    )
    data = response.json()

    error_message = data.get('error')
    if error_message is None:
        return f"Successfully sent 10 Near tokens with transaction hash {data.get('txh')}"
    else:
        return f"An error occured: {error_message}"


TOOLS = [get_testnet_tokens]

def get_tools() -> list:
    return [convert_to_openai_tool(t) for t in TOOLS]

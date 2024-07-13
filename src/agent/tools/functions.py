import requests
from requests.auth import HTTPBasicAuth
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from py_near.account import Account
from py_near.dapps.core import NEAR

from config import env

@tool()
def get_testnet_tokens(receiver: str):
    """Send some Near testnet tokens to a Near account
    Args:
        receiver (str): The receiver of the tokens
    Returns:
        String explaining what happened"""

def get_testnet_tokens_raw(receiver: str) -> str:
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

@tool()
def google_search(query: str):
    """Search Google results, call this if you need more information on a subject
    Args:
        query (str): The query to search for
    Returns:
        list: A list of dictionaries containing the title, link, snippet, and other information about the search results."""

def google_search_raw(query: str) -> list[dict]:
    basic_auth = HTTPBasicAuth(env.oxylabs_username, env.oxylabs_password)

    response = requests.post(
        'https://realtime.oxylabs.io/v1/queries',
        auth=basic_auth,
        json={"source": "google_search", "query": query, "parse": True}
    )

    data = response.json()
    return data.get('results')[0].get('content').get('results')

@tool()
def mint_near_nft(receiver: str):
    """Create an NFT and send it to a Near account
    Args:
        receiver (str): The receiver of the tokens
    Returns:
        String explaining what happened"""

async def mint_near_nft_raw(receiver: str) -> str:
    account = Account(env.near_account_id, env.near_account_private_key, env.near_rpc_url)
    await account.startup()

    result = await account.function_call(
        "nearaibot.testnet",
        "nft_mint",
        {
            "token_id": "2",
            "receiver_id": receiver,
            "token_metadata": {
            "title": "AI NFT",
                "description": "Hello World from nearaibot.testnet!",
                "media": "https://ipfs.io/ipfs/QmQMZcwxrYF499EL1gvJ5Anw4UqAugoYv5XmQwmnoFS3eM",
                "copies": 1
            }
        },
        amount=int(0.1 * NEAR)
    )
    status = result.status
    if status.get('SuccessValue', None) is not None:
        return f"Successfully minted and sent NFT with transaction hash {result.transaction.hash}"
    elif status.get('Failure', None) is not None:
        return f"An error occured: {status.get('Failure')}"
    else:
        return "An unknown error occured"

TOOLS = [get_testnet_tokens, google_search, mint_near_nft]

def get_tools() -> list:
    return [convert_to_openai_tool(t) for t in TOOLS]

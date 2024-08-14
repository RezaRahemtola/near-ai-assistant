# 🇧🇪 ETHGlobal Brussels 2024 - [Near AI Assistant](https://ethglobal.com/showcase/near-ai-assistant-jmwgf)

This project aims to provide a one-stop AI chatbot to discover the [Near](https://near.org/) ecosystem 🚀
It was built during the ETHGlobal Brussels 2024 hackathon and won the Near prizes in the AI track.

It features an AI agent using an open-source model running on the [Aleph.im](https://aleph.im/) decentralized cloud, and a basic frontend to simplify interactions with it.

The agent has access to several functions to serve requests about Near as best as possible:
- Access to realtime search results (Google), which is used to answer questions related to general Near architecture
- Ability to send testnet NEAR tokens to an address when a user requests it
- Capable of minting and sending a special ETHGlobal Brussels NFT on Near testnet when a user requests it
- Able to simplify the understanding of what happened in a testnet transaction with a given hash and sender

❓ It's always better with examples, so here are some questions that this AI is able to handle:
- What is Near?
- What are the different transaction actions on Near?
- Can I please have an ETHGlobal Brussels NFT sent to me at rezarah.testnet? Thanks
- I want to start using Near, can you send me some tokens on my testnet address random.testnet?
- I don't understand what this transaction is doing, can you help me? The transaction hash is `hash` and it was sent by someone.testnet.

## ⚙️ Installation

### AI

Setup your Python environment with these commands:
```shell
cd ai/
python -m venv venv
python -m pip install poetry
poetry install
```

Then you can create a `.env` file and fill it with values inspired from the [`.env.example`](/ai/.env.example) file.


### Front

Setup your frontend with these commands:
```shell
cd front/
yarn
```

## 🚀 Getting started

Now you're only two command away from using your Near AI assistant 🔥

Start the AI
```shell
python src/main.py
```

and launch the frontend
```shell
yarn dev
```

## 📈 Current caveats and future improvements

As a hackathon project built in solo, this is obviously not finished and can be improved in many ways. This section will focus on the AI / features side, but the frontend and the way of interacting with this AI can of course also be enhanced.

- **Better / longer context and retry**\
  The model currently used is [Nous Hermes 2 Pro - Llama 3 8B](https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B), which is really good for handling JSON and function calls in particular (that's why I chose it for this hackathon).
  While it produces great results, the `8192` context length can be limiting.
  Having models with higher context length could allow for chat history persistence, more recursive / retry loops etc (but of course such models like [Phi 3](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct) with its 128k context length have worst results with JSON, XML, function calls etc).

- **Fully autonomous and on-chain agent**\
  Having the AI inference done in a decentralize way is already a big step forward
  a fully decentralized AI agent. As it's already connected to the blockchain, able to control a wallet and make transactions, a future where we have an agent that provide services to people, receive tokens for it, and use them to pay for its own computing on a decentralized cloud like Aleph is really near (no pun intended 🤪)

- **Better integration with the Near ecosystem**\
  This is the main obvious point, but currently the action done by the AI on-chain are pretty basic. Developing other complex tools available for the AI would really make it an interesting project to become the one-stop AI chatbot for Near 🚀

## ➕ Miscellaneous

Other things I have used / fixed related to Near during this hackathon

- Made a fork of [py-near](https://github.com/pvolnov/py-near), based on [another fork](https://github.com/pinnace/py-near) that was solving some [dependencies issues](https://github.com/pvolnov/py-near/issues/18): [https://github.com/RezaRahemtola/py-near](https://github.com/RezaRahemtola/py-near)\
This allowed me to use the latest version of `py-near` without the dependency issues from the base project.
> 🧠 I found this `py-near` package really cool (great typing) and useful, but to be perfect a few things are missing imho:
>  - Add it to the `near` organization and maintain it if possible, currently there is an [outdated API package there](https://github.com/near/near-api-py) linking to `py-near`. Having someone maintaining it would avoid this "fork of a fork of a replacement of `near-api-py`" that I had to made
> - Enhance the error handling, some error messages are really unclear
>   - For example, a wrong `contract_id` param in the `account.function_call` method gave me... a Rust error (from the `.so` of the core primitives) about `transaction.get_hash()` returning a wrong value
> - Could be a great thing to add to the [`awesome-near`](https://github.com/near/awesome-near) repo in a Libraries / Frameworks section
- Some small PRs for outdated documentations or typos:
  - https://github.com/near/docs/pull/2139
  - https://github.com/pvolnov/py-near/pull/22

<div align="center">
  <h2>Made with ❤️ by</h2>
  <a href="https://github.com/RezaRahemtola">
    <img src="https://github.com/RezaRahemtola.png?size=85" width=85/>
    <br>
    <sub>Reza Rahemtola</sub>
  </a>
</div>

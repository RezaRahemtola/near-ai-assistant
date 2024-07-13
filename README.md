# near-ai

ETHGlobal Brussels 2024

## Installation

```shell
python -m venv venv
python -m pip install poetry
poetry install

# Start the project
python src/main.py
```

## Miscellaneous

Other things I have used / fixed related to Near during this hackathon

- Made a fork of [py-near](https://github.com/pvolnov/py-near), based on [another fork](https://github.com/pinnace/py-near) that was solving some [dependencies issues](https://github.com/pvolnov/py-near/issues/18): https://github.com/RezaRahemtola/py-near\
This allowed me to use the latest version of `py-near` without the dependency issues from the base project.
> 🧠 I found this `py-near` package really cool (great typing) and useful, but to be perfect a few things are missing imho:
>  - Add it to the `near` organization and maintain it if possible, currently there is an [outdated API package there](https://github.com/near/near-api-py) linking to `py-near`. Having someone maintaining it would avoid this "fork of a fork of a replacement of `near-api-py`" that I had to made
> - Enhance the error handling, some error messages are really unclear
>   - For example, a wrong `contract_id` param in the `account.function_call` method gave me... a Rust error (from the `.so` of the core primitives) about `transaction.get_hash()` returning a wrong value
> - Could be a great thing to add to the [`awesome-near`](https://github.com/near/awesome-near) repo in a Libraries / Frameworks section
- Made some small PRs for outdated documentations or typos:
  - https://github.com/near/docs/pull/2139
  - https://github.com/pvolnov/py-near/pull/22

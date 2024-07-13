import aiohttp

from logger import logger
from .prompt import PromptGenerator


class Agent:
    def __init__(self, config: dict):
        # Model
        self.model_api_url: str = config["model"]["api_url"]
        self.max_prompt_tokens: int = config["model"]["max_prompt_tokens"]
        self.max_completion_tokens: int = config["model"]["max_completion_tokens"]
        self.temperature: float = config["model"]["temperature"]
        self.top_p: float = config["model"]["top_p"]
        self.top_k: float = config["model"]["top_k"]

        # Agent
        self.max_recurse_depth: int = config["agent"]["max_recurse_depth"]

        # Utils
        self.prompt_generator = PromptGenerator(config)

    async def generate_prompt(self, message: str) -> str:
        """Generate the prompt within the model's context window"""

        system_prompt, used_system_tokens = self.prompt_generator.system_prompt(self.max_prompt_tokens)

        user_prompt = self.prompt_generator.user_prompt(
            message, token_limit=self.max_prompt_tokens - used_system_tokens
        )

        return f"{system_prompt}{user_prompt}"

    async def complete(self, prompt: str) -> tuple[str, int]:
        """Complete on a prompt with the model"""

        session = aiohttp.ClientSession()
        slot_id = -1

        params = {
            "prompt": prompt,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,

            # llamacpp config
            "n_predict": self.max_completion_tokens,
            "id_slot": slot_id,
            "slot_id": slot_id,
            "typical_p": 1,
            "tfs_z": 1,
            "cache_prompt": True,
            "use_default_badwordsids": False,
        }

        async with session.post(self.model_api_url, json=params) as response:
            if response.status == 200:
                response_data = await response.json()
                result = response_data["content"]
                await session.close()
                return result
            else:
                raise RuntimeError(f"Agent::complete: Request failed: {response.status}")


    async def yield_response(self, message: str):
        """Yield a string containing the agent response"""

        # Build the prompt
        prompt = await self.generate_prompt(message)

        logger.debug(f"Agent::yield_response: prompt: {prompt}")

        # Keep track of the depth of self recursion
        recurse_depth = 0

        while recurse_depth < self.max_recurse_depth:
            # Actually do the completion
            completion = await self.complete(prompt)

            logger.debug(f"Agent::yield_response: completion: {completion}")

            tool_message = None
            try:
                # TODO: tool calls
                _tmp = 42
            except Exception as e:
                logger.warn(f"An error occured on tools completion {e}")
                raise e
            finally:
                # If there's nothing to do, return the completion
                if tool_message is None:
                    logger.debug(f"Agent::yield_response: recursion_depth: {recurse_depth}")
                    yield completion
                    return

                recurse_depth += 1

                if recurse_depth >= self.max_recurse_depth:
                    raise RecursionError("Function call depth exceeded")

                # TODO: generate tool message, and generate prompt again with it
                # prompt = f"{prompt}{completion}{tool_message}"

                logger.debug(
                    f"Agent::yield_response: doing recursion on prompt: {prompt}"
                )

                yield "Loading..."

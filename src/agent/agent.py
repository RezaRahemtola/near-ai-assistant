import aiohttp

from logger import logger
from .prompt import PromptGenerator
from .tools import ToolsHandler
from .utils import calculate_token_length


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
        self.max_completion_tries = config["agent"]["max_completion_tries"]
        self.max_recurse_depth: int = config["agent"]["max_recurse_depth"]
        self.stop_sequences = config["chat_ml"]["stop_sequences"]

        # Utils
        self.prompt_generator = PromptGenerator(config)
        self.tools_handler = ToolsHandler()

    async def generate_prompt(self, message: str) -> str:
        """Generate the prompt within the model's context window"""

        system_prompt, used_system_tokens = self.prompt_generator.system_prompt(self.max_prompt_tokens)

        user_prompt, _used_user_tokens = self.prompt_generator.user_prompt(
            message, token_limit=self.max_prompt_tokens - used_system_tokens
        )

        return f"{system_prompt}{user_prompt}"

    async def complete(self, prompt: str) -> tuple[str, int]:
        """Complete on a prompt with the model"""

        session = aiohttp.ClientSession()

        params = {
            "prompt": prompt,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,

            # llamacpp params
            "n_predict": self.max_completion_tokens,
            "typical_p": 1,
            "tfs_z": 1,
            "stop": self.stop_sequences,
            "cache_prompt": True,
            "use_default_badwordsids": False,
        }

        tries = 0
        errors = []
        full_result = ""
        result = ""
        while tries < self.max_completion_tries:
            # Append the compound result to the prompt
            params["prompt"] = f"{params['prompt']}{result}"
            try:
                async with session.post(self.model_api_url, json=params) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        result = response_data["content"]
                        full_result = f"{full_result}{result}"
                        token_count = calculate_token_length(full_result)
                        await session.close()
                        return full_result, token_count
                    else:
                        raise RuntimeError(f"Agent::complete: Request failed: {response.status}")
            except Exception as e:
                logger.debug(f"Agent::complete: Error completing prompt: {e}")
                errors.append(e)
            finally:
                tries += 1
        raise RuntimeError(f"Agent::complete: Failed to complete prompt: {errors}")


    async def yield_response(self, message: str):
        """Yield a string containing the agent response"""

        # Build the prompt
        prompt = await self.generate_prompt(message)

        logger.debug(f"Agent::yield_response: prompt: {prompt}")

        # Keep track of the depth of self recursion
        recurse_depth = 0

        while recurse_depth < self.max_recurse_depth:
            # Actually do the completion
            completion, _tokens = await self.complete(prompt)

            logger.debug(f"Agent::yield_response: completion: {completion}")

            tool_message = None
            try:
                tool_calls = self.tools_handler.extract_tool_calls(completion)

                if len(tool_calls) > 0:
                    yield "Gathering some information to help you..."
                tool_message = self.tools_handler.complete(tool_calls, self.max_recurse_depth)
            except Exception as e:
                logger.warn(f"An error occured on tools completion {e}")
                raise e
            finally:
                # If there's nothing to do, return the completion
                if tool_message is None:
                    yield completion
                    return

                recurse_depth += 1

                if recurse_depth >= self.max_recurse_depth:
                    raise RecursionError("Function call depth exceeded")

                tool_message = self.prompt_generator.tool_prompt(tool_message)

                # TODO: real max tokens with already used ones
                prompt, _ = self.prompt_generator.user_prompt(f"{prompt}{completion}{tool_message}", self.max_prompt_tokens)

                logger.debug(f"Agent::yield_response: doing recursion on prompt: {prompt}")

                yield "Loading..."

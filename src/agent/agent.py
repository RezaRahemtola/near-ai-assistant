from logger import logger


class Agent:
    def __init__(self, ai_config: dict):
        # Model
        self.model_api_url = ai_config["model"]["api_url"]
        self.model_engine = ai_config["model"]["engine"]

        self.max_prompt_tokens = ai_config["model"]["max_prompt_tokens"]

        # Agent
        self.max_recurse_depth = ai_config["agent"]["max_recurse_depth"]

    async def generate_prompt(self, _message: str) -> str:
        """Generate the prompt within the model's context window"""

        # TODO: system prompt
        system_prompt = "You are an AI agent."

        # TODO: prompt with Near context

        return f"{system_prompt}"

    async def yield_response(self, message: str):
        """Yield a string containing the agent response"""

        # Build the prompt
        prompt = await self.generate_prompt(message)

        logger.debug(f"Agent::yield_response: prompt: {prompt}")

        # Keep track of the depth of self recursion
        recurse_depth = 0

        while recurse_depth < self.max_recurse_depth:
            # Actually do the completion

            # TODO: real completion
            # completion = await self.complete(prompt)
            completion = "Hello world!"

            logger.debug(f"Agent::yield_response(): completion: {completion}")

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

                    logger.info(
                        f"Agent::yield_response: recusion_depth: {recurse_depth}"
                    )
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

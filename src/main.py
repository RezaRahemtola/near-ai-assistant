import asyncio

from agent.agent import Agent
from logger import logger
from config import env

try:
    AGENT = Agent(env.ai_config)
except Exception as e:
    logger.error(f"An error occurred during setup: {e}")

async def entrypoint():
    try:
        logger.debug("Starting...")
        async for answer in AGENT.yield_response("Who are you? Search on Google"):
            logger.info(f"Response: {answer}")
    except Exception as e:
        logger.error(f"An error occured: {e}")
    finally:
        logger.debug("Stopping...")


if __name__ == "__main__":
    asyncio.run(entrypoint())

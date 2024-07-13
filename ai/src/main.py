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
        while True:
            question = input("Enter your question: ")
            async for answer in AGENT.yield_response(question):
                print(f"Response: {answer}")
    except KeyboardInterrupt:
        print("\nSee you later!")
    except Exception as e:
        logger.error(f"An error occured: {e}")
    finally:
        logger.debug("Stopping...")


if __name__ == "__main__":
    try:
        asyncio.run(entrypoint())
    except KeyboardInterrupt:
        pass

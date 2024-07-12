import asyncio

from logger import logger

async def entrypoint():
    try:
        logger.debug("Starting...")
        # TODO: logic
    except Exception as e:
        logger.error(f"An error occured: {e}")
    finally:
        logger.debug("Stopping...")


if __name__ == "__main__":
    asyncio.run(entrypoint())

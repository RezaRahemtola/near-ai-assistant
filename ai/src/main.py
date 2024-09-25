import socketio

from aiohttp import web
from agent.agent import Agent
from logger import logger
from config import env

try:
    AGENT = Agent(env.ai_config)
except Exception as e:
    logger.error(f"An error occurred during setup: {e}")


sio = socketio.AsyncServer(async_mode='aiohttp', async_handlers=True, cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

@sio.on('message')
async def handle_message(sid, question: str):
    print('Received message: ', question)
    try:
        logger.debug("Starting...")
        async for answer in AGENT.yield_response(question):
            await sio.emit('response', answer)
    except Exception as e:
        logger.error(f"An error occured: {e}")
    finally:
        logger.debug("Stopping...")


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=3001)

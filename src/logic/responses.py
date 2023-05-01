
from .validations import is_registered_channel, response_needed
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")


def respond_to_message(incoming_message):
    logger.info("processing message")
    channel_id = get_channel_id(incoming_message)
    logger.debug("Received channel ID as {}", channel_id)
    if channel_id is not None:
        if is_registered_channel(channel_id):
            logger.info(" channel id {} is registered processing the request", channel_id)
            logger.info("processing the message")
            if response_needed(incoming_message):
                return "Hello from Optimus Prime", channel_id
            else:
                logger.info("Response Not needed for the request")
                return "NO_RESPONSE_NEEDED", 101
        else:
            logger.error("Invalid channel id {}", channel_id)
            return "Invalid channel id", 500


def respond_to_challenge(incoming_request):
    logger.info("processing challenge")
    if incoming_request.get("challenge") is not None:
        logger.info("Responding Success")
        return incoming_request.get("challenge"), 200
    else:
        logger.info("Responding Error")
        return "Challenge not found", 500


def get_channel_id(incoming_message):
    logger.debug("Finding channel id from request = {}", incoming_message)
    if incoming_message.get("event") is not None and incoming_message.get("event").get("channel"):
        channel_id = incoming_message.get("event").get("channel")
        logger.debug("Received channel id as {}", channel_id)
        return channel_id
    else:
        return None

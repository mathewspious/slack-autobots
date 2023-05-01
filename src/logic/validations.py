from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")



channel_list = ["C051ZBDQN2H"]


def is_registered_channel(channel_id):
    logger.debug("Verifying if channel {} is registered", {channel_id})
    if channel_id in channel_list:
        logger.info("Channel {} is registered", {channel_id})
        return True
    else:
        logger.warning("Channel {} is NOT-registered", {channel_id})
        return False


def response_needed(incoming_message):
    logger.debug("Checking if response required for req {}", incoming_message)
    if not is_bot_event(incoming_message):
        logger.debug("Response is required")
        return True
    else:
        logger.debug("Response is NOT required")
        return False


def is_bot_event(incoming_message):
    logger.debug("Checking if {} is bot event", incoming_message)
    if incoming_message.get("event") is not None and incoming_message.get("event").get("bot_profile"):
        logger.debug("Bot pofile found")
        return True
    else:
        logger.debug("Bot profile not found")
        return False

import logging
from .validations import is_registered_channel, response_needed
logger = logging.getLogger(__name__)


def respond_to_message(incoming_message):
    logger.info("processing message")
    if incoming_message.get("event") is not None and incoming_message.get("event").get("channel"):
        channel_id = incoming_message.get("event").get("channel")
        logger.info("Received channel id as %s", channel_id)
    if is_registered_channel(channel_id):
        print(incoming_message)
        logger.info(" channel id %s is registered processing the request", channel_id)
        logger.info("processing the message")
        if response_needed(incoming_message):
            return "Hello from Optimus Prime", 200

    else:
        logger.error("Invalid channel id %s", channel_id)
        return "Invalid channel id", 500


def respond_to_challenge(incoming_request):
    logger.info("processing challenge")
    if incoming_request.get("challenge") is not None:
        logger.info("Responding Success")
        return incoming_request.get("challenge"), 200
    else:
        logger.info("Responding Error")
        return "Challenge not found", 500

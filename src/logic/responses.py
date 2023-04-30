import logging
logger = logging.getLogger(__name__)


def respond_to_challenge(incoming_request):
    logger.info("processing")
    if incoming_request.get("challenge") is not None:
        logger.info("Responding Success")
        return incoming_request.get("challenge"), 200
    else:
        logger.info("Responding Error")
        return "Challenge not found", 500

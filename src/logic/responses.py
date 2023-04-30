import logging
logger = logging.getLogger(__name__)


def respond_to_message(incoming_message):
    logger.info("processing message")
    # TODO add logic to populate the channel_id from incoming message
    channel_id = "C051ZBDQN2H"
    # TODO read channel Id and validate for registration before responding
    print(incoming_message)





def respond_to_challenge(incoming_request):
    logger.info("processing challenge")
    if incoming_request.get("challenge") is not None:
        logger.info("Responding Success")
        return incoming_request.get("challenge"), 200
    else:
        logger.info("Responding Error")
        return "Challenge not found", 500

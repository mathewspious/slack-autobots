channel_list = ["C051ZBDQN2H"]


def is_registered_channel(channel_id):
    if channel_id in channel_list:
        return True
    else:
        return False


def response_needed(incoming_message):
    if not is_bot_event(incoming_message):
        return True


def is_bot_event(incoming_message):
    if incoming_message.get("event") is not None and incoming_message.get("event").get("bot_profile"):
        return True
channel_list = ["C051ZBDQN2H"]


def is_registered_channel(channel_id):
    if channel_id in channel_list:
        return True
    else:
        return False


def response_needed():
    pass


def is_bot_event(incoming_request):
    pass
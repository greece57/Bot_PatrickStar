""" Configure Bot Reactions """

def react(slack_client, history, channel_id, bot_id):
    """ React on messages

    Keyword arguments:
    slack_client -- Slack Client to post messages
    history -- Last messages
    """
    history = crop_history(history, bot_id)
    for message in history['messages']:
        if "instrument" in message['text'] \
        or "music" in message['text']:
            ask_if_mayonese_is_an_instrument(slack_client, channel_id)


def crop_history(history_data, bot_id):
    """ Removes Messages that are not of type message and messages written by this bot """
    history_data['messages'] = [m for m in history_data['messages'] \
    if m['type'] == 'message' and 'user' in m and m['user'] != bot_id]
    return history_data

def ask_if_mayonese_is_an_instrument(slack_client, channel_id):
    """ Asks if Mayonese is an instrument """
    slack_client.api_call("chat.postMessage", channel=channel_id, text='Is mayonnaise an instrument?', as_user='true')
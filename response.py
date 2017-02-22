""" Configure Bot Reactions """
import time
from random import randint

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
        elif message_has_sign_of_bad_mood(message['text']):
            tell_story_of_the_ugly_barnacle(slack_client, channel_id, message)
        elif randint(1, 101) == 42:
            ask_if_user_is_an_instrument(slack_client, channel_id, message)


def crop_history(history_data, bot_id):
    """ Removes Messages that are not of type message and messages written by this bot """
    history_data['messages'] = [m for m in history_data['messages'] \
    if m['type'] == 'message' and 'user' in m and m['user'] != bot_id]
    return history_data

def postMessage(slack_client, channel_id, message):
    response = slack_client.api_call("chat.postMessage", channel=channel_id, text=message, as_user='true')
    if response['ok'] != True:
        if response['error'] == 'not_in_channel':
            print "Bot was not in Channel - attempting to join!"
            channel_name = get_channel_name_by_id(channel_id)
            response = slack_client.api_call("channels.join", name=channel_name)
            if response['ok'] == True:
                postMessage(slack_client, channel_id, message)
            else:
                print "Couldn't join the Channel " + channel_name
                print response['error']

def get_channel_name_by_id(slack_client, channel_id):
    channels = slack_client.api_call("channels.list")['channels']
    for channel in channels:
        if channel['id'] == channel_id:
            return channel['name']


def ask_if_mayonese_is_an_instrument(slack_client, channel_id):
    """ Asks if Mayonese is an instrument """
    postMessage(slack_client, channel_id, 'Is mayonnaise an instrument?')

def ask_if_user_is_an_instrument(slack_client, channel_id, message):
    """ Asks if User is an instrument """
    user = slack_client.api_call("users.info", user=message['user'])['user']
    responseText = "Is " + str(user['profile']['first_name']) + " an instrument?"
    postMessage(slack_client, channel_id, responseText)
    

def tell_story_of_the_ugly_barnacle(slack_client, channel_id, message):
    """ Tells the Story of the Ugly Barnacle """
    userFirstName = slack_client.api_call("users.info", user=message['user'])['user']['profile']['first_name']
    storyText1 = "Oh " + userFirstName + " maybe a story will cheer you up!"
    storyText2 = "It's called the \"Ugly Barnacle\""
    storyText3 = "Once there was an ugly barnacle! He was so ugly that everyone died"
    storyText4 = "The end! :D"
    postMessage(slack_client, channel_id, storyText1)
    time.sleep(2)
    postMessage(slack_client, channel_id, storyText2)
    time.sleep(2)
    postMessage(slack_client, channel_id, storyText3)
    time.sleep(2)
    postMessage(slack_client, channel_id, storyText4)

def message_has_sign_of_bad_mood(text):
    text = text.lower()
    bad_mood = ["bad mood", "not so good", "don't feel good", "don't feel so good", \
     "don't feel so well", "don't feel well", " sad", " ill", "feel down", ":disappointed:", \
     ":confused:", ":slightly_frowning_face:", ":pensive:", ":expressionless:", ":neutral_face:", \
     ":worried:", ":white_frowning_face:", ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:"]
    for bad_mood_text in bad_mood:
        if bad_mood_text in text:
            return True

    return False

""" Fetching the last messages every second """
from __future__ import print_function
import sys
import time
from slackclient import SlackClient
from response import Patrick

READ_HISTORY_DELAY = 1
API_TOKEN = "#"

def get_latest_message(history_data, curr_latest):
    """ Returns the TimeStamp of the latest message of a given history """
    messages = history_data['messages']
    if len(messages) == 0:
        return curr_latest
    new_latest = messages[0]
    if curr_latest < new_latest['ts']:
        return new_latest['ts']
    else:
        return curr_latest


def retrieve_groups():
    """ get all Groups where Bot is in """
    response_groups = SC.api_call("groups.list")
    response_channels = SC.api_call("channels.list")
    if response_groups['ok'] and response_channels['ok']:
        groups = response_groups['groups']
        channels = response_channels['channels']
        return groups, channels

    # Retrieving Error
    else:
        if not response_groups['ok']:
            print ("Error while retrieving Groups: " + response_groups['error'])

        if not response_channels['ok']:
            print ("Error while retrieving Channels: " + response_channels['error'])

        return [], []


def remove_initial_history():
    """ returns timestamp of latest message"""

    latest = 0
    groups, channels = retrieve_groups()
    for group in groups:
        history = SC.api_call("groups.history", channel=group['id'], oldest=latest)
        latest = get_latest_message(history, latest)

    for channel in channels:
        history = SC.api_call("channels.history", channel=channel['id'], oldest=latest)
        latest = get_latest_message(history, latest)

    return latest


def main_loop():
    """ Main Loop of the Bot """

    latest_message = remove_initial_history()
    seconds = 0
    while True:
        groups, channels = retrieve_groups()

        for group in groups:
            history = SC.api_call("groups.history", channel=group['id'], \
                                    oldest=latest_message)
            latest_message = get_latest_message(history, latest_message)

            PATRICK_BOT.react(history, group['id'])

        for channel in channels:
            history = SC.api_call("channels.history", channel=channel['id'], \
                                    oldest=latest_message)
            latest_message = get_latest_message(history, latest_message)

            PATRICK_BOT.react(history, channel['id'])

        output = "." * (1 + seconds % 3) + "Latest message: " + latest_message + "   \r"
        print (output, end="")
        sys.stdout.flush()

        time.sleep(READ_HISTORY_DELAY)
        seconds = seconds + READ_HISTORY_DELAY



if __name__ == "__main__":

    with open('token.key', 'r') as keyFile:
        while API_TOKEN.startswith("#"):
            API_TOKEN = keyFile.readline()

    SC = SlackClient(API_TOKEN)

    if SC.api_call("api.test")['ok'] is True:
        BOT_ID = SC.api_call("auth.test")['user_id']
        PATRICK_BOT = Patrick(SC, BOT_ID)
        print ("StarterBot connected and running!")

        main_loop()
    else:
        print ("Connection failed. Invalid Slack token or bot ID?")

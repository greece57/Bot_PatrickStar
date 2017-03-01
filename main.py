""" Fetching the last messages every second """
from __future__ import print_function
import sys
import time
from ChannelTypes import ChannelType
from Patrick import Patrick
from slackclient import SlackClient

READ_HISTORY_DELAY = 1
API_TOKEN = "#"
DEVMODE = False

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
    response_ims = SC.api_call("im.list")

    if not response_groups['ok']:
        print ("Error while retrieving Groups: " + response_groups['error'])
        groups = []
    else:
        groups = response_groups['groups']

    if not response_channels['ok']:
        print ("Error while retrieving Channels: " + response_channels['error'])
        channels = []
    else:
        channels = response_channels['channels']

    if not response_ims['ok']:
        print ("Error while retrieving IMs: " + response_ims['error'])
        ims = []
    else:
        ims = response_ims['ims']

    return groups, channels, ims


def remove_initial_history():
    """ returns timestamp of latest message"""

    latest = 0
    groups, channels, ims = retrieve_groups()
    for group in groups:
        history = SC.api_call("groups.history", channel=group['id'], oldest=latest)
        if not history['ok']:
            print ("Error while retrieving History of Channel \"" + group['name'] \
                    + "\": " + history['error'])
        else:
            latest = get_latest_message(history, latest)

    for channel in channels:
        history = SC.api_call("channels.history", channel=channel['id'], oldest=latest)
        if not history['ok']:
            print ("Error while retrieving History of Channel \"" + channel['name'] \
                    + "\": " + history['error'])
        else:
            latest = get_latest_message(history, latest)

    for im_chat in ims:
        history = SC.api_call("im.history", channel=im_chat['id'], oldest=latest)
        if not history['ok']:
            print ("Error while retrieving History of Channel \"" + im_chat['name'] \
                    + "\": " + history['error'])
        else:
            latest = get_latest_message(history, latest)

    return latest


def main_loop():
    """ Main Loop of the Bot """

    latest_message = remove_initial_history()
    seconds = 0
    while True:
        try:
            groups, channels, ims = retrieve_groups()

            for group in groups:
                history = SC.api_call("groups.history", channel=group['id'], \
                                        oldest=latest_message)
                if not history['ok']:
                    print ("Error while retrieving History of Group \"" + group['name'] \
                            + "\": " + history['error'])
                else:
                    latest_message = get_latest_message(history, latest_message)

                    PATRICK_BOT.react(history, group['id'], ChannelType.Group)

            if not DEVMODE:
                for channel in channels:
                    history = SC.api_call("channels.history", channel=channel['id'], \
                                            oldest=latest_message)
                    if not history['ok']:
                        print ("Error while retrieving History of Channel \"" + channel['name'] \
                                + "\": " + history['error'])
                    else:
                        latest_message = get_latest_message(history, latest_message)

                        PATRICK_BOT.react(history, channel['id'], ChannelType.Channel)

            for im_chat in ims:
                history = SC.api_call("im.history", channel=im_chat['id'], \
                                            oldest=latest_message)
                if not history['ok']:
                    print ("Error while retrieving History of IM-Chat of User \"" \
                                + im_chat['user'] + "\": " + history['error'])
                else:
                    latest_message = get_latest_message(history, latest_message)

                    PATRICK_BOT.react(history, im_chat['id'], ChannelType.ImChat)

            output = "." * (1 + seconds % 3) + "Latest message: " + latest_message + "   \r"
            print (output, end="")
            sys.stdout.flush()

            time.sleep(READ_HISTORY_DELAY)
            seconds = seconds + READ_HISTORY_DELAY
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print (" !!! " + e.__doc__ + ": " + e.message + " Trying to resume...               ")
            if DEVMODE:
                raise


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

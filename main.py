""" Fetching the last messages every second """
import time
from slackclient import SlackClient
from response import react

def get_latest_message(history_data, curr_latest):
    """ Returns the TimeStamp of the latest message of a given history """
    messages = history_data['messages']
    if len(messages) == 0:
        return curr_latest
    latest_message = messages[0]
    if curr_latest < latest_message['ts']:
        return latest_message['ts']
    else:
        return curr_latest

def remove_initial_history():
    """ returns timestamp of latest message"""

    latest = 0
    groups = SC.api_call("groups.list")['groups']
    channels = SC.api_call("channels.list")['channels']
    for group in groups:
        history = SC.api_call("groups.history", channel=group['id'], oldest=latest)
        latest = get_latest_message(history, latest)

    for channel in channels:
        history = SC.api_call("channels.history", channel=channel['id'], oldest=latest)
        latest = get_latest_message(history, latest)

    return latest

if __name__ == "__main__":
    READ_HISTORY_DELAY = 2
    API_TOKEN = "#"

    with open('token.key', 'r') as keyFile:
        while API_TOKEN.startswith("#"):
            API_TOKEN = keyFile.readline()

    SC = SlackClient(API_TOKEN)

    if SC.api_call("api.test")['ok'] is True:
        BOT_ID = SC.api_call("auth.test")['user_id']
        print "StarterBot connected and running!"

        latestMessage = remove_initial_history()
        while True:
            groups = SC.api_call("groups.list")['groups']
            channels = SC.api_call("channels.list")['channels']
            for group in groups:
                history = SC.api_call("groups.history", channel=group['id'], oldest=latestMessage)
                latestMessage = get_latest_message(history, latestMessage)
                
                react(SC, history, group['id'], BOT_ID)

            for channel in channels:
                history = SC.api_call("channels.history", channel=channel['id'], oldest=latestMessage)
                latestMessage = get_latest_message(history, latestMessage)

                react(SC, history, channel['id'], BOT_ID)

            print "Latest Timestamp: " + str(latestMessage)
            time.sleep(READ_HISTORY_DELAY)


    else:
        print "Connection failed. Invalid Slack token or bot ID?"

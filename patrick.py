""" Configure Bot Reactions """
import os
import imp
import inspect
from fnmatch import fnmatch

class Patrick(object):
    """ Patrick Bot - Does what Patrick does """

    MOOD_COMMENT_DICT = {0: "I'm happy! :blush:", \
                         1: "I'm slightly upset.", \
                         2: "I'm Angry! :angry:"}

    NO_SOURCE_TEXT = "The Inner Machinations of my Mind are an Enigma\n" + \
                     "https://www.youtube.com/watch?v=KNZSXnrbs_k"

    REACTIONS = []

    def __init__(self, slack_client, bot_id):
        """ Constructor """
        self.slack_client = slack_client
        self.bot_id = bot_id
        self.mood = 0
        self.message_counter = 0
        self.last_mood_change = 0
        self.last_method = None
        self.get_all_reactions()


    def react(self, history, channel_id):
        """ React on messages

        Keyword arguments:
        slack_client -- Slack Client to post messages
        history -- Last messages
        """

        history = self.crop_history(history)
        for message in history['messages']:
            if self.mood < 3:
                for reaction in self.REACTIONS:
                    if reaction.condition(message):
                        reaction.consequence(channel_id)
                        self.last_method = reaction.IDENTIFIER

            if self.message_asks_how_patricks_mood_is(message['text']):
                self.tell_mood(channel_id)

            if self.user_asks_for_source(message['text']):
                self.give_source(channel_id)

            self.message_counter += 1
            self.adjust_mood()


    def crop_history(self, history_data):
        """ Removes Messages that are not of type message and messages written by this bot """

        history_data['messages'] = [m for m in history_data['messages'] \
        if m['type'] == 'message' and 'user' in m and m['user'] != self.bot_id]
        return history_data


    def post_message(self, channel_id, message):
        """ Sends a Message and tries to resolve Error """

        response = self.slack_client.api_call("chat.postMessage", channel=channel_id, \
                                                text=message, as_user='true')
        if response['ok'] != True:
            if response['error'] == 'not_in_channel':
                print "Bot was not in Channel - attempting to join!"
                channel_name = self.get_channel_name_by_id(channel_id)
                response = self.slack_client.api_call("channels.join", name=channel_name)
                if response['ok']:
                    self.post_message(channel_id, message)
                else:
                    print "Couldn't join the Channel " + channel_name
                    print response['error']


    def get_channel_name_by_id(self, channel_id):
        """ Returns the Channel Name of a given Channel ID """

        channels = self.slack_client.api_call("channels.list")['channels']
        for channel in channels:
            if channel['id'] == channel_id:
                return channel['name']


    def tell_mood(self, channel_id):
        """ Sends Message to communicate his current Mood """
        text = ""
        if self.mood > 2:
            text = "I'M TRIGGERED :rage: :rage: :rage:"
        else:
            text = self.MOOD_COMMENT_DICT[self.mood]

        self.post_message(channel_id, text)

        self.last_method = None


    def give_source(self, channel_id):
        """ Sends the source for the last message """
        if self.last_method == None:
            self.post_message(channel_id, self.NO_SOURCE_TEXT)
        for reaction in self.REACTIONS:
            print reaction.IDENTIFIER + " - " + self.last_method
            if self.last_method == reaction.IDENTIFIER:
                self.post_message(channel_id, reaction.SOURCE)

        self.last_method = None


    def message_asks_how_patricks_mood_is(self, text):
        """ Check is the Message asks Patrick how he feels """
        text = text.lower()
        questions = ["how are you " + self.str_at_patrick() + "?", \
                     self.str_at_patrick() + " how are you?"]

        for question in questions:
            if text == question:
                return True

        return False

    def user_asks_for_source(self, text):
        """ Checks if user asks for source of last answer by Patrick """
        text = text.lower()
        if text == "why did you say that " + self.str_at_patrick() + "?" \
        or text == self.str_at_patrick() + " why did you say that?" \
        or text == self.str_at_patrick() + " source for that please":
            return True
        else:
            return False


    def adjust_mood(self):
        """ Calms Patrick down after a specific amount of messages """

        # It needs 20 * mood Messages to calm Patrick down
        if self.mood > 0 and self.message_counter - self.last_mood_change > 4 * self.mood:
            self.mood = self.mood - 1
            self.last_mood_change = self.message_counter


    def make_angry(self):
        """ Makes Patrick Angry """
        self.mood = self.mood + 1
        self.last_mood_change = self.message_counter

    def make_happy(self):
        """ Makes Patrick Happy """
        self.mood = 0
        self.last_mood_change = self.message_counter

    def str_at_patrick(self):
        """ Returns "<@PATRICKS_BOT_ID>" as String """
        return "<@" + self.bot_id.lower() + ">"

    def get_all_reactions(self):
        """ Source: http://stackoverflow.com/questions/39431287/how-do-i-dynamically-create-instances-of-all-classes-in-a-directory-with-python """
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/Reactions"
        pattern = "*.py"

        for path, subdirs_top, files in os.walk(dir_path):
            for name in files:
                if fnmatch(name, pattern):# and not fnmatch(name, "AbstractReaction.py"):
                    found_module = imp.find_module(name[:-3], [path])
                    module = imp.load_module(name, found_module[0], found_module[1], found_module[2])
                    for mem_name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and inspect.getmodule(obj) is module:
                            self.REACTIONS.append(obj(self))

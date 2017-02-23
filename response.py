""" Configure Bot Reactions """
import time
import re
from random import randint
from patrick_reactions import PatricksReactions

class Patrick(object):
    """ Patrick Bot - Does what Patrick does """


    BAD_MOOD = ["bad mood", "not so good", "don't feel good", "don't feel so good", \
                "don't feel so well", "don't feel well", " sad", " ill", "feel down", \
                ":disappointed:", ":confused:", ":slightly_frowning_face:", ":pensive:", \
                ":expressionless:", ":neutral_face:", ":worried:", ":white_frowning_face:", \
                ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:", \
                ":(", ":/", ";(", ":'("]

    THIS_IS_PATRICK_MOOD_DICT = {0: "No this is Patrick :slightly_smiling_face:", \
                                 1: "No this is Patrick! :angry:", \
                                 2: "NO THIS IS PATRICK! :rage:"}

    MOOD_COMMENT_DICT = {0: "I'm happy! :blush:", \
                         1: "I'm slightly upset.", \
                         2: "I'm Angry! :angry:"}

    LAST_METHOD_SOURCE = {None: \
                            "I don't know", \
                          PatricksReactions.INSTRUMENT: \
                            "https://youtu.be/d1JA-nh0IfI?t=4s", \
                          PatricksReactions.THIS_IS_PATRICK: \
                            "https://www.youtube.com/watch?v=YSzOXtXm8p0", \
                          PatricksReactions.UGLY_BARNACLE: \
                            "https://www.youtube.com/watch?v=WejTV7r3tkU"}


    def __init__(self, slack_client, bot_id):
        """ Constructor """
        self.slack_client = slack_client
        self.bot_id = bot_id
        self.mood = 0
        self.is_this_pattern = re.compile(r"[Ii]s this [\s\S]*\?")
        self.message_counter = 0
        self.last_mood_change = 0
        self.last_method = None


    def react(self, history, channel_id):
        """ React on messages

        Keyword arguments:
        slack_client -- Slack Client to post messages
        history -- Last messages
        """

        history = self.crop_history(history)
        for message in history['messages']:
            if self.mood < 3:
                if self.user_asks_for_source(message['text']):
                    self.give_source(channel_id)

                elif "instrument" in message['text'] \
                or "music" in message['text']:
                    self.ask_if_mayonese_is_an_instrument(channel_id)

                elif self.message_has_sign_of_bad_mood(message['text']):
                    self.tell_story_of_the_ugly_barnacle(channel_id, message)

                elif self.message_asks_if_this_is_the_crusty_crab(message['text'], channel_id):
                    self.no_this_is_patrick(channel_id)

                elif randint(1, 101) == 42:
                    self.ask_if_user_is_an_instrument(channel_id, message)

            if self.message_asks_how_patricks_mood_is(message['text']):
                self.tell_mood(channel_id)

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


    def ask_if_mayonese_is_an_instrument(self, channel_id):
        """ Asks if Mayonese is an instrument """
        self.post_message(channel_id, 'Is mayonnaise an instrument?')

        self.last_method = PatricksReactions.INSTRUMENT


    def ask_if_user_is_an_instrument(self, channel_id, message):
        """ Asks if User is an instrument """

        user = self.slack_client.api_call("users.info", user=message['user'])['user']
        response_text = "Is " + str(user['profile']['first_name']) + " an instrument?"
        self.post_message(channel_id, response_text)

        self.last_method = PatricksReactions.INSTRUMENT


    def tell_story_of_the_ugly_barnacle(self, channel_id, message):
        """ Tells the Story of the Ugly Barnacle """

        user_first_name = self.slack_client.api_call("users.info", \
                                            user=message['user'])['user']['profile']['first_name']
        story_text = {0: "Oh " + user_first_name + " maybe a story will cheer you up!", \
                      1: "It's called the \"Ugly Barnacle\"", \
                      2: "Once there was an ugly barnacle! He was so ugly that everyone died", \
                      3: "The end! :upside_down_face:"}
        self.post_message(channel_id, story_text[0])
        time.sleep(2)
        self.post_message(channel_id, story_text[1])
        time.sleep(2)
        self.post_message(channel_id, story_text[2])
        time.sleep(2)
        self.post_message(channel_id, story_text[3])

        self.last_method = PatricksReactions.UGLY_BARNACLE


    def no_this_is_patrick(self, channel_id):
        """ NO THIS IS PATRICK """
        self.post_message(channel_id, self.THIS_IS_PATRICK_MOOD_DICT[self.mood])
        self.make_angry()

        self.last_method = PatricksReactions.THIS_IS_PATRICK


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
        self.post_message(channel_id, self.LAST_METHOD_SOURCE[self.last_method])
        self.last_method = None


    def message_has_sign_of_bad_mood(self, text):
        """ Checks if a Message has signs of bad mood of the author - e.g. sad smilies """

        text = text.lower()
        for bad_mood_text in self.BAD_MOOD:
            if bad_mood_text in text:
                return True

        return False

    def message_asks_if_this_is_the_crusty_crab(self, text, channel_id):
        """ Checks if the Message asks for the Crusty Crab """
        text = text.lower()
        if text == "is this patrick?":
            self.post_message(channel_id, "Yes this is Patrick :blush:")
            self.make_happy()
            return False
        else:
            return self.is_this_pattern.match(text)


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

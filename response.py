""" Configure Bot Reactions """
import time
import re
from random import randint

class Patrick(object):
    """ Patrick Bot - Does what Patrick does """

    def __init__(self, slack_client, bot_id):
        """ Constructor """
        self.slack_client = slack_client
        self.bot_id = bot_id
        self.mood = 0
        self.is_this_pattern = re.compile(r"[Ii]s this [\s\S]*\?")
        self.message_counter = 0
        self.last_mood_change = 0


    def react(self, history, channel_id):
        """ React on messages

        Keyword arguments:
        slack_client -- Slack Client to post messages
        history -- Last messages
        """

        history = self.crop_history(history)
        for message in history['messages']:
            if self.mood < 3:
                if "instrument" in message['text'] \
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


    def ask_if_user_is_an_instrument(self, channel_id, message):
        """ Asks if User is an instrument """

        user = self.slack_client.api_call("users.info", user=message['user'])['user']
        response_text = "Is " + str(user['profile']['first_name']) + " an instrument?"
        self.post_message(channel_id, response_text)
        

    def tell_story_of_the_ugly_barnacle(self, channel_id, message):
        """ Tells the Story of the Ugly Barnacle """

        userFirstName = self.slack_client.api_call("users.info", user=message['user'])['user']['profile']['first_name']
        storyText1 = "Oh " + userFirstName + " maybe a story will cheer you up!"
        storyText2 = "It's called the \"Ugly Barnacle\""
        storyText3 = "Once there was an ugly barnacle! He was so ugly that everyone died"
        storyText4 = "The end! :D"
        self.post_message(channel_id, storyText1)
        time.sleep(2)
        self.post_message(channel_id, storyText2)
        time.sleep(2)
        self.post_message(channel_id, storyText3)
        time.sleep(2)
        self.post_message(channel_id, storyText4)

    
    def no_this_is_patrick(self, channel_id):
        """ NO THIS IS PATRICK """
        mood_dict = {0: "No this is Patrick :slightly_smiling_face:", 1: "No this is Patrick! :angry:", 2: "NO THIS IS PATRICK! :rage:"}
        self.post_message(channel_id, mood_dict[self.mood])
        self.make_angry()

    
    def tell_mood(self, channel_id):
        mood_dict = {0: "I'm happy! :blush:", 1: "I'm slightly upset.", 2: "I'm Angry! :angry:"}
        text = ""
        if (self.mood > 2):
            text = "I'M TRIGGERED :rage: :rage: :rage:"
        else:
            text = mood_dict[self.mood]
        
        self.post_message(channel_id, text)


    def message_has_sign_of_bad_mood(self, text):
        """ Checks if a Message has signs of bad mood of the author - e.g. sad smilies """

        text = text.lower()
        bad_mood = ["bad mood", "not so good", "don't feel good", "don't feel so good", \
                    "don't feel so well", "don't feel well", " sad", " ill", "feel down", \
                    ":disappointed:", ":confused:", ":slightly_frowning_face:", ":pensive:", \
                    ":expressionless:", ":neutral_face:", ":worried:", ":white_frowning_face:", \
                    ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:"]
        for bad_mood_text in bad_mood:
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
        questions = ["how are you <@" + self.bot_id.lower() + ">?", \
                    "<@" + self.bot_id.lower() + "> how are you?"]
        print questions
        print text
        for question in questions:
            if text == question:
                return True

        return False


    def adjust_mood(self):
        """ Calms Patrick down after a specific amount of messages """

        # It needs 20 * mood Messages to calm Patrick down
        if self.mood > 0 and self.message_counter - self.last_mood_change > 2 * self.mood:
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

""" Patrick Reactions on "Is this <something>?" """
import re
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class IsThisReaction(Reaction):
    """ Reaction when somebody asks if sth is sth """

    IDENTIFIER = "THIS IS PATRICK"
    SOURCE = "https://www.youtube.com/watch?v=YSzOXtXm8p0"

    CHANNEL_TYPES = [ChannelType.Channel, ChannelType.Group]


    THIS_IS_PATRICK_MOOD_DICT = {0: "No this is Patrick :slightly_smiling_face:", \
                                 1: "No this is Patrick! :angry:", \
                                 2: "NO THIS IS PATRICK! :rage:"}

    def __init__(self, patrick):
        self.is_this_pattern = re.compile(r"[Ii]s this [\s\S]*\?")
        self.asked_if_its_patrick = False
        super(IsThisReaction, self).__init__(patrick)

    def condition(self, message):
        """ Checks if the Message asks for the Crusty Crab """
        text = message['text'].lower()
        if text == "is this patrick?":
            self.asked_if_its_patrick = True
            return True
        else:
            self.asked_if_its_patrick = False
            return self.is_this_pattern.match(text)


    def consequence(self, channel_id):
        """ NO THIS IS PATRICK """
        if self.asked_if_its_patrick:
            self.patrick.post_message(channel_id, "Yes this is Patrick :blush:")
            self.patrick.make_happy()
            self.asked_if_its_patrick = False
        else:
            self.patrick.post_message(channel_id, self.THIS_IS_PATRICK_MOOD_DICT[self.patrick.mood])
            self.patrick.make_angry()


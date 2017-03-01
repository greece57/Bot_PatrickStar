""" Patrick Reactions on Instruments """
import re
from Memegenerator.memegenerator import make_meme
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class WhyDontMemeCreateReaction(Reaction):
    """ Little Meme Generator """

    IDENTIFIER = "WhyDontMeme"
    SOURCE = "https://www.youtube.com/watch?v=WnaiVxUTK7Y"
    CHANNEL_TYPES = [ChannelType.ImChat]

    PATTERN = "(why don't [\\w\\W]*) (and [\\w\\W]*)"
    FOLDER = "Memegenerator"
    MEME = "whydontwe.jpg"

    def __init__(self, patrick):
        self.user_met_condition = ""
        self.top_string = ""
        self.bottom_string = ""
        super(WhyDontMemeCreateReaction, self).__init__(patrick)

    def condition(self, message):
        """ Condition: Music or Insrument is in the Message """
        text = message['text']
        rematch = re.match(self.PATTERN, text, re.IGNORECASE)

        if rematch:
            self.top_string = rematch.group(1)
            self.bottom_string = rematch.group(2)
            self.user_met_condition = message['user']
            return True
        else:
            return False


    def consequence(self, channel_id):
        """ Consequence: Ask if Mayonese is an Instrument """
        make_meme(self.top_string, self.bottom_string, self.MEME, self.FOLDER, \
                    self.user_met_condition)
        self.patrick.post_message(channel_id, 'I\'m ready :slightly_smiling_face:')

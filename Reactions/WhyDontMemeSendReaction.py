""" Patrick Reactions on Instruments """
import re
from memegenerator.memegenerator import make_meme
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class WhyDontMemeSendReaction(Reaction):
    """ Little Meme Generator """

    IDENTIFIER = "WhyDontMeme"
    SOURCE = "https://www.youtube.com/watch?v=WnaiVxUTK7Y"
    CHANNEL_TYPES = [ChannelType.Group, ChannelType.Channel, ChannelType.ImChat]

    PATTERN = ["tell them patrick"]
    FOLDER = "Memegenerator"

    def __init__(self, patrick):
        self.PATTERN.append("tell them " + patrick.str_at_patrick())
        self.file_name = ""
        super(WhyDontMemeSendReaction, self).__init__(patrick)

    def condition(self, message):
        """ Condition: Music or Insrument is in the Message """
        text = message['text'].lower()
        if text in self.PATTERN:
            self.file_name = message['user']
            return True
        else:
            return False


    def consequence(self, channel_id):
        """ Consequence: Ask if Mayonese is an Instrument """
        try:
            path = self.FOLDER + "/" + self.file_name + ".png"
            file_obj = open(path, 'r')
            self.patrick.upload_file(channel_id, file_obj)
        except IOError:
            self.patrick.post_message(channel_id, "What should i tell them? :worried:")

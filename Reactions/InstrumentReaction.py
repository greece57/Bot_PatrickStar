""" Patrick Reactions on Instruments """
from random import randint
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class InstrumentReaction(Reaction):
    """ Reaction when somebody referse to instruments or music """

    IDENTIFIER = "Instrument"
    SOURCE = "https://youtu.be/d1JA-nh0IfI?t=4s"
    CHANNEL_TYPES = [ChannelType.Channel, ChannelType.Group]

    def __init__(self, patrick):
        self.random_number = 0
        self.tmp_first_name = ""
        super(InstrumentReaction, self).__init__(patrick)

    def condition(self, message):
        """ Condition: Music or Insrument is in the Message """
        text = message['text'].lower()
        self.random_number = randint(1, 101)

        if "music" in text or "instrument" in text:
            return True
        elif self.random_number == 42:
            user_json = \
                    self.patrick.slack_client.api_call("users.info", user=message['user'])['user']
            self.tmp_first_name = user_json['profile']['first_name']
            return True
        else:
            return False


    def consequence(self, channel_id):
        """ Consequence: Ask if Mayonese is an Instrument """
        if self.random_number == 42:
            # Asks if User is an instrument
            response_text = "Is " + self.tmp_first_name + " an instrument?"
            self.patrick.post_message(channel_id, response_text)

        else:
            self.patrick.post_message(channel_id, 'Is mayonnaise an instrument?')

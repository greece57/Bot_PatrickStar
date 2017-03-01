""" Patricks Reaction if it's after 3am """
from datetime import datetime
import pytz
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class ThreeAmReaction(Reaction):
    """ Reaction when somebody talks after 3am """

    IDENTIFIER = "3am"
    SOURCE = "https://www.youtube.com/watch?v=YZ6K3m9TsPs"
    CHANNEL_TYPES = [ChannelType.Channel, ChannelType.Group]

    TIMEZONE = pytz.timezone('Europe/Berlin')

    def __init__(self, patrick):
        self.last_date_said = datetime.min.date()
        super(ThreeAmReaction, self).__init__(patrick)

    def condition(self, message):
        """ Condition: between 3am and 4am """
        curr_date = datetime.now(self.TIMEZONE).date()
        if self.last_date_said < curr_date:
            curr_hour = datetime.now(self.TIMEZONE).hour
            if curr_hour == 3:
                return True
        else:
            return False


    def consequence(self, channel_id):
        """ Consequence: Ask if Mayonese is an Instrument """
        self.patrick.post_message(channel_id, "Oh Boy!! 3am!! :heart_eyes::hamburger:")
        self.last_date_said = datetime.now(self.TIMEZONE).date()

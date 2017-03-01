""" Patrick Reactions on bad mood """
import time
from ChannelTypes import ChannelType
from AbstractReaction import Reaction

class UglyBarnacleReaction(Reaction):
    """ Reaction when somebody is sad """

    IDENTIFIER = "Ugly Barnacle"
    SOURCE = "https://www.youtube.com/watch?v=WejTV7r3tkU"
    CHANNEL_TYPES = [ChannelType.Channel, ChannelType.Group]

    BAD_MOOD = ["bad mood", "not so good", "don't feel good", "don't feel so good", \
                "don't feel so well", "don't feel well", " sad", " ill", "feel down", \
                ":disappointed:", ":confused:", ":slightly_frowning_face:", ":pensive:", \
                ":expressionless:", ":neutral_face:", ":worried:", ":white_frowning_face:", \
                ":confounded:", ":tired_face:", ":weary:", ":cry:", ":sob:", \
                " :(", " :/", " ;(", " :'("]

    def __init__(self, patrick):
        self.last_message = ""
        super(UglyBarnacleReaction, self).__init__(patrick)

    def condition(self, message):
        """ Checks if a Message has signs of bad mood of the author - e.g. sad smilies """

        text = message['text'].lower()
        for bad_mood_text in self.BAD_MOOD:
            if bad_mood_text in text:
                self.last_message = message
                return True

        return False


    def consequence(self, channel_id):
        """ Tells the Story of the Ugly Barnacle """

        user_first_name = self.patrick.slack_client.api_call("users.info", \
                                    user=self.last_message['user'])['user']['profile']['first_name']
        story_text = {0: "Oh " + user_first_name + " maybe a story will cheer you up!", \
                      1: "It's called the \"Ugly Barnacle\"", \
                      2: "Once there was an ugly barnacle! He was so ugly that everyone died", \
                      3: "The end! :upside_down_face:"}
        self.patrick.post_message(channel_id, story_text[0])
        time.sleep(2)
        self.patrick.post_message(channel_id, story_text[1])
        time.sleep(2)
        self.patrick.post_message(channel_id, story_text[2])
        time.sleep(2)
        self.patrick.post_message(channel_id, story_text[3])

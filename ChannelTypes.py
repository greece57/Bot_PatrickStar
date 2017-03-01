""" Slack ChannelTypes """
from enum import Enum

class ChannelType(Enum):
    """ Different Communication Channels of Slack """
    Group = 1
    Channel = 2
    ImChat = 3

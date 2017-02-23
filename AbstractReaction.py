""" Interface of an Reaction """

class Reaction(object):
    """ This defines the methods of an Reaction """

    IDENTIFIER = None
    SOURCE = None

    def __init__(self, patrick):
        """ Init of Reaction """
        self.patrick = patrick

    def condition(self, message):
        """ Condition of Reaction """
        raise NotImplementedError("Condition not Implemented")

    def consequence(self, channel_id):
        """ Consequence of Reaction """
        raise NotImplementedError("Consequence not Implemented")


from .voting import Vote
from .upVote import UpVote
from .downVote import DownVote
from .positiveVote import PositiveVote
from .negativeVote import NegativeVote
from .karmaCommand import KarmaCommand

class KarmaHistoryManager():

    def __int__(self, inputUp = False, inputDown = False):
        self.up = inputUp
        self.down = inputDown
        self.voted = Vote
        self.commandCarriedOut = KarmaCommand
        self.setCommand()

    def setCommand(self):
        if self.up == True:
            self.voted = PositiveVote
            self.commandCarriedOut = UpVote
        else:
            if self.down == True:
                self.voted = NegativeVote
                self.commandCarriedOut = DownVote

    def calculateKarma(self):
        self.commandCarriedOut.execute()

            

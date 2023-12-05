from .karmaCommand import KarmaCommand

class DownVote(KarmaCommand):

    def __init__(self):
        self.voted = KarmaCommand
    
    def execute(self):
        self.voted.addVote()
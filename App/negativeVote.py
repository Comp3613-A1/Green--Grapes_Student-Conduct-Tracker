from App.models.voting import Vote

class NegativeVote(Vote):

    numberDownVote = 0

    def __init__(self, vote):
        self.vote = vote
    
    def addVote(self):
        numberDownVote +=1
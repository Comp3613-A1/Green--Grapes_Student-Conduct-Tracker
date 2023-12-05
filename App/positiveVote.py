from App.models.voting import Vote

class PositiveVote(Vote):

    numberUpVote = 0

    def __init__(self, vote):
        self.vote = vote
    
    def addVote(self):
        numberUpVote +=1
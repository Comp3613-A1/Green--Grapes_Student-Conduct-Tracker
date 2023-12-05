from abc import ABC, abstractmethod

class Vote(ABC):
    @abstractmethod
    def addVote(self):
        pass
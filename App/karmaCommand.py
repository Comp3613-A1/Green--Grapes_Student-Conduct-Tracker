from abc import ABC, abstractmethod

class KarmaCommand(ABC):
    @abstractmethod
    def execute():
        pass
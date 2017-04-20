from abc import ABCMeta, abstractmethod

class IAlterationEntity():

    @abstractmethod
    def checkNChange(self, logLine):
        """ Change the entity due to string from logFile"""

class IAction():
    def doAction(self):
        """ Does some action and returns bool if it valid"""
from File import File
from datetime import datetime
from random import *
from Agent import Agent


class Chit:
    def __init__(self, agent: Agent, operation: str, PathFile: str):
        self.code = self._generateCode()
        self._file = File(PathFile)
        self.num = self._file.get_last_id() + 1
        self.operation = operation
        self.agent = agent

    def saveChit(self):
        """
        :return: this code must save the curent chit information in the file
        """
        self._file.saveData(f"{self.num}_{self.code}_{self.operation}_"
                            f"{datetime.now().strftime('%d-%m-%y')}_{self.agent.getSignature()}")

    def getnum(self):
        """
        :return: return the current num to use
        """
        return self._file.get_last_id() + 1

    def _generateCode(self):
        """
        :return: generate the current code recu
        """
        code = ""
        if len(self._file.getData() == 0):
            code = str(datetime.now().strftime("%d-%m")) + self.operation[:2] + str(randint(100, 1000))
        elif len(self._file.getData() > 0):
            code = self._file.getData()[-1].split("_")[0] + datetime.now().strftime("%d-%m") + self.operation[:2] \
                   + str(randint(100, 1000))
        return code

    def deleteChit(self, num):
        """
        :param num: the num of the chit to delete
        :return:  the chit that the num is given
        """
        pass

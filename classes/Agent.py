from classes.File import *


class Agent:
    def __init__(self, contact: str, password: str):
        self._name = ""
        self._password = password
        self._contact = contact
        self._typeUser = "admin"
        self._signature = ""
        self._loadData()

    def getName(self):
        """
        :return: this return the name of the agent
        """
        return self._name

    def _getPassword(self):
        """
        :return: this return the password of the agent
        """
        return self._password

    def _getSignature(self):
        """
        :return: this return the signature of the agent
        """
        return self._signature

    def typeUser(self):
        """
        :return: this return the type of the agent
        """
        return self._typeUser

    def isAdmin(self):
        """
        :return: this function return True if the user id an admin and false in other case
        """
        if self._typeUser.lower() == "admin":
            return True
        return False

    def _loadData(self):
        """
        :return: this function loads data
        """
        file = File("files/agent/agentList")
        for data in file.getData():
            if data.split("_")[5] == self._contact or data.split("_")[6] == self._contact and data.split("_")[
                7] == self._password:
                self._name = data.split("_")[1] + data.split("_")[2] + data.split("_")[3]
                self._contact = [data.split("_")[5], data.split("_")[7]]
                self._signature = data.split("_")[9]
                self._typeUser = data.split("_")[8]
from datetime import *


class File:
    def __init__(self, pathFile: str):
        self.path = pathFile

    def get_All_Data(self) -> list:
        """
        :return: return all the data from the file of the given path
        """
        with open(f"{str(self.path)}", "r") as data:
            content = [a for a in data.read().split("\n") if len(a) > 0]
            return content

    def getData(self) -> list:
        """
        :return: return all the data without the title
        """
        return self.get_All_Data()[1:]

    def saveData(self, newData: str):
        content = self.get_All_Data()
        content.append(newData)
        # writing data
        with open(f"{self.path}", "w") as dat:
            dat.write("\n".join(content))

    def save_list_data(self, list_data: list):
        with open(f"{self.path}", "w") as dat:
            dat.write("\n".join(list_data))

    def getDayData(self, service: str) -> list:
        if str(service).lower() == "achat" or str(service).lower() == "vente":
            return [a for a in self.getData() if
                    a.split("_")[1] == datetime.now().strftime("%d/%m/%Y") and a.split("_")[3] == service]

    def get_last_id(self) -> str:
        """
        :return: this function return the last id of the opening file
        """
        if len(self.getData()) > 0:
            return self.getData()[-1].split("_")[0]
        else:
            return "1"

    def delete_all_data(self):
        """
        :return: this function writes only the title and despite erevy thingd
        """
        data = self.get_All_Data()
        with open(f"{self.path}", "w") as file:
            file.write("\n".join(data[0]))


class Date_trait:
    def __int__(self):
        self.date = datetime

    def getUpdateDate(self):
        """
        :return: this  function return only the date in dd/mm/yy date format as an str
        """
        return self.date.now().strftime("")

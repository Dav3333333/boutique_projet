from classes.File import File
import datetime
import calendar
from classes.Produit import Produit
from tkinter import messagebox


def is_not_empty_data(data: list):
    if len(data) > 0:
        return True
    else:
        return messagebox.showinfo("Donne vide", "Il y a pas de donne pour cette periode")


class Rapport(File):
    def __init__(self, directory_path: str = "files/flux"):
        super().__init__(f"{directory_path}/fluxFile")
        self.products_file = File(f"{directory_path}/produit")
        self.flux_app_data = File(f"{directory_path}/flux_date_app")
        # getting month from the calendar module and convert the to lower
        self.__months = [a.lower() for a in calendar.month_name[1:]]

    def __service_years(self):
        fist_year = [int(a.split("_")[2]) for a in self.flux_app_data.getData()]
        list_year = []
        if fist_year[0] < int(datetime.datetime.now().strftime("%Y")):
            for i in range(fist_year[0], int(datetime.datetime.now().strftime("%Y")) + 1):
                list_year.append(i)
        elif fist_year[0] == int(datetime.datetime.now().strftime("%Y")):
            list_year.append(fist_year[0])
        else:
            return False
        return list_year

    def dailly_rapport(self, date: str):
        """
        :param date: this must be a date in dd/m/Y
        :return: this method return a list of data of the given date
        """
        list_data = []
        for data in self.getData():
            if date.lower().strip() == data.split("_")[1]:
                list_data.append(data)
        return list_data

    def month_rapport(self, month: str):
        """
        :param month: this must be a complete moth. Ex: january, february, ...
        :return: this method returns a list of the operation of the opened file on the given month
        """
        if month.lower().strip() in self.__months:
            list_data = []
            size_month_number = len(str(datetime.datetime.strptime(month, "%B").month))
            # loop on the data
            for data in super().getData():
                # check if the size of the number of the month is 1 to complete the date for the rule of the month file
                if size_month_number == 1:
                    # check if the month number from the file is the save as the given month
                    if data.split("_")[1].split("/")[1] == ("0" + str(datetime.datetime.strptime(month, "%B").month)):
                        list_data.append(data)
                elif size_month_number == 2:
                    if data.split("_")[1].split("/")[1] == str(datetime.datetime.strptime(month, "%B").month):
                        # print(datetime.datetime.strptime(month, "%B").month)
                        list_data.append(data)
            return list_data
        return "Invalid month"

    def year_repport(self, year: int):
        """
        :param year: this is the year of the report and must be in the service years
        :return: the report of all the year of all the product
        """
        service_year = self.__service_years()
        if int(year) in service_year:
            list_data = []
            if int(year) <= int(datetime.datetime.now().year):
                for data in self.getData():
                    if data.split("_")[1].split("/")[2] == str(year):
                        list_data.append(data)
                return list_data
        else:
            print(type(service_year[0]))
            return "Invalid year"

    def __rapport_products(self, periode: str):
        """
        :param periode: this is the periode of the rapport, mabe day, month or year
        :return: A dictionnary of products as keys and total achat and totol vente as values separeted by _
        """
        products = {}
        periode = periode.strip().lower()

        if periode.isnumeric():
            if int(periode) in self.__service_years():

                for product_name in self.products_file.getData():
                    # create a new Product objet for every itineration
                    product = Produit(product_name.split("_")[1].strip())
                    # adding a product in the list of products
                    products[
                        product.get_name()] = f"{product.get_general_benefit()}_" \
                                              f"{product.get_vente_total_price()}({product.get_vente_total_pieces()} pieces)_" \
                                              f"{product.get_achat_total_price()} ({product.get_achat_total_pieces()}"

        elif "/" in periode and len(periode.split("/")) == 3:
            counter = 1
            for product in self.products_file.getData():
                counter += 1
                product_name = product.split("_")[1].strip()
                total_achat = []
                total_vente = []
                total_vente_pices = []
                total_achat_pices = []
                for line in self.dailly_rapport(f"{periode}"):
                    # split the data line
                    splited_line = line.strip().split("_")
                    # check if the product name is equal to the product in the data
                    if product_name == splited_line[2]:
                        # check if is the achat activity
                        if splited_line[3].strip() == "achat":
                            # add to the achat_total list
                            total_achat.append(float(splited_line[6].strip()))
                            total_achat_pices.append(float(splited_line[4].strip()))
                        # check if is the vente activity
                        elif splited_line[3] == "vente":
                            total_vente.append(float(splited_line[6].strip()))
                            total_vente_pices.append(float(splited_line[4].strip()))
                products[product_name] = f"{(sum(total_vente) - sum(total_achat))}_" \
                                         f"{sum(total_vente)}({sum(total_vente_pices)} pieces)_" \
                                         f"{sum(total_achat)} ({sum(total_achat_pices)} pieces)"

        elif periode.strip() in self.__months:
            for line in self.month_rapport(periode):
                # create a new Product objet for every itineration
                product = Produit(line.split("_")[2].strip())
                # adding a product in the list of products
                products[
                    product.get_name()] = f"{product.get_general_benefit()}_" \
                                          f"{product.get_vente_total_price()}({product.get_vente_total_pieces()} pieces)" \
                                          f"_{product.get_achat_total_price()} ({product.get_achat_total_pieces()}"
        else:
            return "invalid period"
        return products

    def __period_verification(self, period: str):
        period = period.strip().lower()
        if period.isnumeric():
            return True
        elif "/" in period and len(period.split("/")) == 3:
            return True
        elif period in self.__months:
            return True
        else:
            return False

    def getRapport(self, period: str):
        period = period.lower().strip()
        if self.__period_verification(period):
            # getting data according to the given period
            data = [(self.__rapport_products(period)[a].split("_") + [a]) for a in self.__rapport_products(period)]
            # adding and creating the head to the pdf data
            new_data = [['Numero', "Produit", "Achat", "Vente", "Benefice"]]

            for row, n in zip(data, range(1, len(data) + 1)):
                row.append(n)
                row.reverse()
                new_data.append(row)
            return new_data
        else:
            return ["invalid period"]

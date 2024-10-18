import datetime
from classes.File import File
from view.functions import get_user_string, convert_user_string


class Produit:
    def __init__(self, nom_produit: str):
        self._nom = convert_user_string(nom_produit.lower()).strip()
        self._file_flux = File("files/flux/fluxFile")
        self._file_produit = File("files/flux/produit")
        self._operation = ""

    def get_name(self):
        """
        :return: return the name
        """
        return self._nom

    def _list_produit(self) -> list:
        """
        :return: return all the list of the product
        """
        return [a.split("_")[1].lower() for a in self._file_produit.getData()]

    def get_achat_total_pieces(self):
        """
        :return: return the sum of all the piece bought and permanent in the store
        """
        if self._nom in self._list_produit():

            return sum([float(a.split("_")[4]) for a in self._file_flux.getData()
                        if a.split("_")[2] == self._nom and a.split("_")[3] == "achat"])
        else:
            return -1

    def get_achat_total_price(self):
        """
        :return: the total money that all the bought pieces
        """
        return sum([float(a.split("_")[6]) for a in self._file_flux.getData()
                    if a.split("_")[2] == self._nom and a.split("_")[3] == "achat"])

    def get_vente_total_pieces(self):
        """
        :return: return the sum of all the piece sold
        """
        if len(self._file_flux.getData()) > 0:
            return sum([float(a.split("_")[4]) for a in self._file_flux.getData()
                        if a.split("_")[2] == self._nom and a.split("_")[3] == "vente"])

        else:
            return 0

    def get_vente_total_price(self):
        """
        :return: the total money that all the sold piece made
        """
        if len(self._file_flux.getData()) > 1:
            return sum([float(a.split("_")[6]) for a in self._file_flux.getData()
                        if a.split("_")[2] == self._nom and a.split("_")[3] == "vente"])
        else:
            return 0

    def get_sold_store_pieces(self):
        """
        :return: return the sold of the pieces in the store
        """
        return self.get_achat_total_pieces() - self.get_vente_total_pieces()

    def _get_prix_achat(self):
        """
        :return: return the price with which the pieces were bought
        """
        if self._nom in self._list_produit():
            if len(self._file_produit.getData()) > 1:
                return [a.split("_")[2] for a in self._file_produit.getData() if a.split("_")[1] == self._nom][0]
            else:
                return [0]
        else:
            return [0]

    def get_price_vente(self):
        """
        :return: this return the price of the products
        """
        if len(self._file_produit.getData()) > 0:
            return [a.split("_")[2] for a in self._file_produit.getData() if a.split("_")[1] == self._nom]
        else:
            return [0]

    def set_price(self, newPrice: int):
        """
        :param newPrice: the price to effect at the place of the old price
        :return: changes the price of the product
        """
        new_prod_list = []
        for line in self._file_produit.get_All_Data():
            if line.split("_")[1] == self._nom:
                lis = line.split("_")
                lis.pop(2)
                lis.insert(2, f"{newPrice}")
                new_prod_list.append("_".join(lis))
            else:
                new_prod_list.append(line)
        self._file_produit.save_list_data(new_prod_list)

    def delete_product(self):
        """
        :return: this function delete the product form the file name and destroy the object (itself)
        """
        prod_list = self._file_produit.get_All_Data()
        #  getting the name of the product at 2 as index creatting a new list of product
        new_prod_list = [prod for prod in prod_list if prod.split("_")[1].strip() != self._nom]
        self._file_produit.delete_all_data()
        self._file_produit.save_list_data(new_prod_list)

    def delete_all_operations(self):
        """
        :return: delete all operation the passed product
        """
        data = [s for s in self._file_flux.get_All_Data() if s.split("_")[2] != self._nom]
        self._file_flux.delete_all_data()
        self._file_flux.save_list_data(data)

    def is_operation_valid(self, pieces: float):
        """
        :param pieces: verify if the operation is valid for the sold
        :return: True if the product can be sold
        """
        if float(pieces) <= float(self.get_achat_total_pieces()):
            return True
        else:
            return False

    def save_operation(self, libelle, quantite: float, prix_unitaire, reduction, FsseurOuClient):
        """
        :param libelle: this is the title aof the activity (achat or vente)
        :param quantite: this is the quantity of the product
        :param prix_unitaire: the price of the product
        :param reduction: the reduction of the product
        :param FsseurOuClient: the name of the one who sell or buy the product
        :return: this save the operation in the file of the given file
        """
        if self.is_operation_valid(quantite) is True:
            self._operation = (
                f"{int(self._file_flux.get_last_id()) + 1}_{datetime.datetime.now().strftime('%d/%m/%Y')}_"
                f"{self._nom}_{str(libelle)}_{str(float(quantite))}_{str(float(prix_unitaire))}_"
                f"{str((float(quantite) * float(prix_unitaire)) - ((float(quantite) * float(prix_unitaire)) * (float(reduction))) / 100)}_"
                f"{str(FsseurOuClient)}")
            self._file_flux.saveData(self._operation)

    def is_produit_valid(self):
        """
        :return: this function returns a boolean and its returns True if the product exist
        """
        if self._nom in self._list_produit():
            return True
        else:
            return False

    def get_general_benefit(self):
        """
        :return: the general benefits of the passed product and does take care of the sold product or no
        """
        return float(self.get_vente_total_price() - self.get_achat_total_price())

    def get_real_benefits(self):
        """
        :return: the real benefits from the sold product and not general
        """
        return float((float(self.get_vente_total_pieces()) * float(self.get_price_vente()[0])) -
                     (float(self.get_vente_total_pieces()) * float(self._get_prix_achat()[0])))

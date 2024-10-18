from datetime import datetime
import datetime
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from classes.File import File
import view.functions as functions
from classes.Produit import Produit


class AchatFrame(CTkFrame):
    def __init__(self, master, fluxFile: File, products_file: File, identif_prod_file: File):
        super().__init__(master)
        self.pack(padx=0, fill=BOTH, expand=True)

        # general frame
        self.genFrame = CTkFrame(master=self)
        self.genFrame.pack(fill=BOTH, expand=True)

        self.title = CTkLabel(master=self.genFrame, text="FACTURATION (ACHAT)", font=('roboto', 25),
                              fg_color="blue",
                              corner_radius=0)
        self.title.pack(side=TOP, padx=0, pady=0, fill=X)

        # data
        self.file = fluxFile
        if len(self.file.get_All_Data()) < 1:  # verifying if the title file exist
            # saving the title in the file
            self.file.saveData("id_dateActitive_nomProduit_libelle_"
                               "quantite_prixVenteUnitaire_prixtot_nomFsseurouClient")
        self.data_achat = self.file.getDayData("achat")
        self.data_flux = self.file.getData()

        # product file verifcations
        self.prod_file = products_file
        if len(self.prod_file.get_All_Data()) == 0:
            self.prod_file.saveData("id_nomProd_typeProd_prixProd_dateAjout")

        self.products = []
        if len(self.prod_file.getData()) == 0:
            self.products.append("Pas de produit")
        elif len(self.prod_file.getData()) >= 1:
            for lines in self.prod_file.getData():
                self.products.append(lines.split("_")[1])

        # identif files verifications
        self.__identif_prod_file = identif_prod_file
        if len(self.__identif_prod_file.get_All_Data()) <1:
            self.__identif_prod_file.saveData("id_nomProduit_dateCreation")
        else:
            pass

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        # side of the agent datail frame on the left
        leftFrame = CTkFrame(master=self.genFrame)
        leftFrame.pack(pady=5, padx=5, expand=True, side=LEFT)

        self.agentInfo(leftFrame)

        return leftFrame

    def create_right_frame(self):
        rightFrame = CTkFrame(master=self.genFrame)
        rightFrame.pack(pady=5, padx=5, expand=True, side=RIGHT, fill=BOTH)

        self.facturation(rightFrame)
        # self.treevAchat(rightFrame)

        return rightFrame

    def aff(self, data: list, trev: ttk.Treeview, type_data="achat"):
        nb = 1
        for line in data:
            if line.split("_")[1] == self.getUpdate() and line.split("_")[3] == type_data:
                trev.insert("", "end", text=f"{nb}",
                            values=(f"{nb}", f"{functions.get_user_string(line.split('_')[1])}",
                                    f"{functions.get_user_string(line.split('_')[2])}",
                                    f"{functions.get_user_string(line.split('_')[4])}",
                                    f"{functions.get_user_string(line.split('_')[5])}",
                                    f"{float(line.split('_')[5]) * float(line.split('_')[4])}"))
            nb = nb + 1

    def facturation(self, master):

        nameProd = CTkComboBox(master,
                               values=self.products,
                               font=("arial", 15), width=475)
        nameProd.pack(padx=30, pady=5)

        quantProd = CTkEntry(master, placeholder_text="Quantite", font=("arial", 20),
                             width=475)
        quantProd.pack(padx=30, pady=5)

        prixProd = CTkEntry(master, placeholder_text="Prix Unitaire (en dollars)", font=("arial", 20),
                            width=475)
        prixProd.pack(padx=30, pady=5)

        nomFournisseur = CTkEntry(master, placeholder_text="Nom fournisseur",
                                  font=("arial", 20),
                                  width=475)
        nomFournisseur.pack(padx=30, pady=5)

        # loading the icon for save

        icon = CTkImage(light_image=Image.open("view/icons/save-file.png"), size=(40, 40))

        btnSub = CTkButton(master, text="ACHETER", font=("arial", 18), image=icon, width=300,
                           command=lambda: self.saveAchat(nameProd, trev,
                                                          self.data_flux, quantProd,
                                                          prixProd, nomFournisseur))
        btnSub.pack(padx=30, pady=5)

        treviewFrame = master
        # creating the title bar

        CTkLabel(master=treviewFrame, text="ACHAT DU JOUR ", corner_radius=2,
                 font=("arial", 25), fg_color="black").pack(padx=2, pady=2, fill=BOTH)

        # creating the treview objet
        trev = ttk.Treeview(treviewFrame)
        trev.pack(fill=BOTH, expand=True, padx=5, pady=5)
        # Scrollbar
        trevSCrollBar = CTkScrollbar(trev, command=trev.yview)
        trevSCrollBar.pack(side="right", fill=Y)

        # configure the treev
        trev.configure(yscrollcommand=trevSCrollBar.set)

        trev["columns"] = ("1", "2", "3", "4", "5", "6")
        trev["show"] = "headings"

        # add header of the trev table

        trev.column("1", width=80, anchor="c")
        trev.column("2", width=80, anchor="c")
        trev.column("3", width=80, anchor="c")
        trev.column("4", width=80, anchor="c")
        trev.column("5", width=80, anchor="c")
        trev.column("6", width=80, anchor="c")

        trev.heading("1", text="NUMERO")
        trev.heading("2", text="DATE DU JOUR")
        trev.heading("3", text="NOM PRODUIT")
        trev.heading("4", text="QUANTITE")
        trev.heading("5", text="COUT UNIT")
        trev.heading("6", text="COUT TOTAL")

        data = File("files/flux/fluxFIle").getDayData("achat")
        self.aff(data, trev)

    # method of the left frame
    def agentInfo(self, master):

        icon = CTkImage(light_image=Image.open("view/icons/agent.png"), size=(200, 200))
        CTkLabel(master, text="", image=icon, width=200, height=200).pack(padx=4, pady=4)

        CTkLabel(master, text="AGENT", font=("roboto", 35),
                 text_color="#87CEEB").pack(pady=5, padx=5)

        nameAgent = CTkLabel(master, text="DAVID LUSENGE OSWALDE".upper(),
                             font=("arial", 20))
        nameAgent.pack(padx=5, pady=10)

        mailAgent = CTkLabel(master, text="davidlusengeoswalde@gmail.com".lower(),
                             font=("arial", 10))
        mailAgent.pack(padx=10)

        signaAgent = CTkLabel(master, text="adsafaefhxnvei234".lower(), font=("arial", 10),
                              text_color="black")
        signaAgent.pack(padx=10)

    def getUpdate(self):
        """
        :return: this fucntion must return the computer updated date in  string format
        """
        date = str(datetime.datetime.now().strftime("%d/%m/20%y")).split(" ")[0]
        return date

    def saveAchat(self, nameProd: CTkComboBox, trev: ttk.Treeview, dataFlux: list, quantProd: CTkEntry,
                  prixProd: CTkEntry, nomFournisseur: CTkEntry):
        name = functions.convert_user_string(str(nameProd.get()))
        name_fournisseur = functions.convert_user_string(nomFournisseur.get())
        quantity = functions.convert_user_string(quantProd.get())
        prixVente = functions.convert_user_string(prixProd.get())

        # verification si quantite est un nombre
        if name != "" and quantity != "" and prixVente != "" and name_fournisseur != "":

            if len(self.prod_file.getData()) == 0:
                messagebox.showinfo("ERREUR", f"Il y a pas de produit disponible dans la liste de produit")

            if quantity.isnumeric() and prixVente.isnumeric():

                prod = Produit(name.strip())

                if prod.is_produit_valid() is True:
                    if int(prod.get_price_vente()[0]) > int(prixVente):
                        data = f"{int(self.file.get_last_id()) + 1}_{functions.dateDuJour()}_{name}_" \
                               f"achat_{float(quantity)}_{float(prixVente)}_" \
                               f"{float(quantity) * float(prixVente)}_{name_fournisseur.lower()}"
                        self.file.saveData(data)
                        messagebox.showinfo("ACHAT REUSSI", f"Merci vous avez Acheter {name}")

                        # saving data in the file
                        trev.delete(*trev.get_children())
                        dataFlux.append(data)
                        self.aff(dataFlux, trev)
                    else:
                        if messagebox.askyesno("Risque perte", f"Il semble que votre prix d'achat {prixVente} est "
                                                               f"superieur a votre prix de vente {prod.get_price_vente()[0]}"
                                                               f". Vous riquez a accumuler des perte sur ce produit."
                                                               f"On vous suggere de modifier le prix du produit. "
                                                               f"\n voulez vous continuez avec l'achat ??"):
                            data = f"{int(self.file.get_last_id()) + 1}_{functions.dateDuJour()}_{name}_" \
                                   f"achat_{float(quantity)}_{float(prixVente)}_" \
                                   f"{float(quantity) * float(prixVente)}_{name_fournisseur.lower()}"
                            self.file.saveData(data)
                            messagebox.showinfo("ACHAT REUSSI", f"Merci vous avez Acheter {name}")

                            # saving data in the file
                            trev.delete(*trev.get_children())
                            dataFlux.append(data)
                            self.aff(dataFlux, trev)
                        else:
                            messagebox.showinfo("Contact interne", "Veuillez contactez l'admin pour modifier le prix")
                else:
                    messagebox.showerror("ERREUR DE PRODUIT", f"Le produit {name} n'existe pas")
            else:
                messagebox.showerror("ERREUR DE NOMBRE", "Le champs quantite ou prix de vente doivent etres des nombre")
        else:
            messagebox.showerror("ERREUR DE SAISIE", "Veuillez completez tout les champs")


from datetime import datetime
import datetime
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tkk
from classes.File import File
from classes.Produit import Produit
from PIL import Image
from view.functions import get_user_string, convert_user_string


class VenteFrame(CTkFrame):
    def __init__(self, master, product_file: File, file_flux_File: File):
        super().__init__(master)
        self.pack(padx=0, fill=BOTH, expand=True)

        # files objects
        self.product_file = product_file  # file produit
        self.fileFlux_file = file_flux_File  # file fluxFile

        self.product_list = product_file.getData()

        # general frame
        self.genFrame = CTkFrame(master=self)
        self.genFrame.pack(fill=BOTH, expand=True)

        self.titleSetting(self.genFrame, "FACTURATION (VENTE)")  # this is the title of the facturation

        self.selectedProd = tkk.StringVar()

        self.update_product_list()

        self.fram_agent()

        self.framFac()

    def update_product_list(self):
        if len(self.product_list) == 0:
            self.product_list.append("id_Pad de produit_typeProd_prixProd_dateAjout")
        else:
            self.product_list = self.product_file.getData()

    def fram_agent(self):
        """
        :return: this code only create one frame of the ventre facturation screen
        """
        fram = CTkFrame(master=self.genFrame)
        fram.pack(expand=True, side=LEFT, pady=5, padx=5, )
        self.agentInfo(fram)

        return fram

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

    def framFac(self):
        """
        :return: this code only create one frame of the ventre facturation screen
        """
        fram = CTkFrame(master=self.genFrame)
        fram.pack(fill=BOTH, expand=True, side=RIGHT)

        # inserting the facturation methode here
        self.facturationWigdet(fram)

        return fram

    def comboBox(self, rangeNumber: tuple, elements: list):
        pass

    def titleSetting(self, master, text_title: str):
        """
        :return: this function desing the tilte and its border according to the application
        """
        lab = CTkLabel(master=master, text=f"{text_title}", text_color="azure",
                       font=("robot", 25), bg_color="blue", corner_radius=0)
        lab.pack(side=TOP, fill=X, pady=0, padx=0)

    def facturationWigdet(self, master):

        # frame for entry and combo box
        fram_fac = CTkFrame(master, width=500)
        fram_fac.pack()

        # frame date
        CTkLabel(master=fram_fac, text="Date :", font=("arial", 15)).place(x=2, y=0)

        labShowDate = CTkLabel(master=fram_fac,
                               text=f"{datetime.datetime.now().strftime('%d - %m - %Y')}".upper(),
                               font=("arial", 17))
        labShowDate.place(x=100, y=0)

        # combo box
        CTkLabel(master=fram_fac, text="Produit : ", font=("arial", 15)).place(x=2, y=30)  # the label for the combobox

        productComboBox = CTkComboBox(master=fram_fac,  # the combox product
                                      values=[a.split("_")[1] for a in self.product_list],
                                      width=250,
                                      variable=self.selectedProd,  # taking the ttk object string var
                                      font=("arial", 15))
        productComboBox.place(x=150, y=30)
        productComboBox.set(f"{self.product_list[0].split('_')[1]}")
        # price
        data = []
        if len(self.product_file.getData()) == 0:
            data.append("-_-_-_")
        else:
            for i in self.product_file.getData():
                data.append(i)

        price = CTkLabel(master=fram_fac,
                         text=f"{[a.split('_')[2] for a in data][0]}",
                         font=("arial", 20))
        price.place(x=410, y=30)
        # dollar sin
        CTkLabel(master=fram_fac, text="$", font=("arial", 20)).place(x=450, y=30)

        # creating  a list of the number of pieces to buy

        CTkLabel(master=fram_fac, text="Nombre de Pieces :", font=("arial", 17)).place(x=2, y=60)  # the label for piece

        quant_acheter = CTkComboBox(master=fram_fac, values=[str(a / 2) for a in range(1, 201)], width=250)
        quant_acheter.place(x=150, y=60)

        # creating the reduction combo Box
        CTkLabel(master=fram_fac, text="Reduction de (%) : ", font=("arial", 17)).place(x=2,
                                                                                        y=90)  # the label for reduc

        reducClientCombo = CTkComboBox(master=fram_fac, width=250,
                                       values=[f"{str(a)}" for a in range(10)])
        reducClientCombo.place(x=150, y=90)

        # the name of the client

        CTkLabel(master=fram_fac, text="Nom du client : ", font=("arial", 17)).place(x=2, y=120)  # the label for client
        clientName = CTkEntry(master=fram_fac, placeholder_text="NOM DU CLIENT",
                              placeholder_text_color="white", width=250)
        clientName.place(x=150, y=120)

        # create the icon of the save button
        icon = CTkImage(Image.open("view/icons/save-file.png"), size=(20, 20))

        buttonVente = CTkButton(master=fram_fac, text="VENDRE", width=200, image=icon, font=("arial", 20),
                                command=lambda: self.save_vente(productComboBox, reducClientCombo, quant_acheter,
                                                                clientName, tabView))
        buttonVente.place(x=180, y=160)

        # treeview
        CTkLabel(master=master, text="VENTE DU JOUR ", corner_radius=2,
                 font=("arial", 25), fg_color="black").pack(padx=2, pady=2, fill=BOTH)

        tabView = ttk.Treeview(master)
        tabView.pack(padx=1, pady=1, fill=BOTH, expand=True)

        tabView["show"] = "headings"
        tabView["columns"] = ("1", "2", "3", "4", "5", "6")

        tabView.column("1", width=5, anchor="c")
        tabView.column("1", width=5, anchor="c")
        tabView.column("2", width=5, anchor="c")
        tabView.column("3", width=5, anchor="c")
        tabView.column("4", width=5, anchor="c")
        tabView.column("5", width=5, anchor="c")
        tabView.column("6", width=5, anchor="c")

        tabView.heading("1", text="NUMERO")
        tabView.heading("2", text="DATE DU JOUR")
        tabView.heading("3", text="NOM PRODUIT")
        tabView.heading("4", text="QUANTITE")
        tabView.heading("5", text="PRIX UNITAIRE")
        tabView.heading("6", text="PRIX TOTAL")

        self.vente_day_display(self.fileFlux_file.getDayData("vente"), tabView)

        self.selectedProd.trace("w", lambda *args: self.update_label(priceLabel=price))

    def save_vente(self, selectedProduit: CTkComboBox, reducClientCombo, quant_acheter,
                   clientName: CTkEntry, tabView: ttk.Treeview):
        prod = convert_user_string(selectedProduit.get())
        reduction = convert_user_string(reducClientCombo.get())
        quantity = convert_user_string(quant_acheter.get())
        name_client = convert_user_string(clientName.get())

        prod_objet = Produit(f"{prod.lower()}")

        if prod_objet.is_produit_valid() is True:
            if name_client != "" and quantity != "":
                if prod_objet.is_operation_valid(quantity) is True:
                    prod_objet.save_operation("vente", float(quantity), prod_objet.get_price_vente()[0], f"{reduction}",
                                              f"{name_client}")
                    tabView.delete(*tabView.get_children())
                    data_day_vente = self.fileFlux_file.getDayData("vente")  # getting day data from flux file
                    self.vente_day_display(data_day_vente, tabView)
                    messagebox.showinfo("OPERATION REUSSI", f"Vente de {prod} est fait deja")
                else:
                    messagebox.showerror("Insufissance de Produit", f"Il y a insuffisance de {prod} dans le stock,"
                                                                    f"il ne reste que {prod_objet.get_name()} dans le stock. veuiller "
                                                                    f"contactez le service d'achat")
            else:
                messagebox.showerror("Echec d'enregistrement de l'operation", "Vous devez remplir tout les champs")
        else:
            messagebox.showerror("Echec d'enregistrement de l'operation",
                                 f"Le produit {prod} n'existe pas dans notre liste des produit"
                                 "veuillez contactez l'admin pour l'ajout du produit")

    def trevWidget(self, master):
        """
        :param master: this must be the master passed in the __init__ function
        :return: this function returns a widget that manage the displaying of the (Vente) activite
        """

    def vente_day_display(self, data, tabWidget):
        num = 1
        for lines in data:
            tabWidget.insert("", "end", text=f"{num}",
                             values=(f"{get_user_string(str(num))}", f"{get_user_string(lines.split('_')[1])}",
                                     f"{get_user_string(lines.split('_')[2])}",
                                     f"{get_user_string(lines.split('_')[4])}",
                                     f"{get_user_string(lines.split('_')[5])} $",
                                     f"{get_user_string(lines.split('_')[6])} $"))
            num += 1

    # the update method
    def update_label(self, priceLabel: CTkLabel, *args):
        prod = Produit(f"{self.selectedProd.get()}").get_price_vente()
        priceLabel.configure(text=prod)

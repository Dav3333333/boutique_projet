from customtkinter import *
from classes import File, Produit
from PIL import Image
from view.ajoutProduit import Add_Product
from view.admin_report_opp import Rapport_View
from view.SuppressionProduit import DeletProduit, messagebox
import view.functions as functions


# import customtkinter as ctk
# from PIL import Image, ImageTk
#
# # Créer l'application CTk
# root = ctk.CTk()
#
# # Charger l'image GIF
# gif_image = Image.open("animated_image.gif")
#
# # Convertir l'image GIF en CTkImage
# ctk_image = ctk.CTkImage(light_image=gif_image, size=(200, 200))
#
# # Créer un CTkLabel avec l'image GIF animée
# label = ctk.CTkLabel(master=root, image=ctk_image)
# label.grid(row=0, column=0)
#
# # Mettre à jour l'image du label à chaque frame du GIF
# def update_image():
#     try:
#         gif_image.seek(gif_image.tell() + 1)
#     except EOFError:
#         gif_image.seek(0)
#     ctk_image.configure(light_image=gif_image)
#     label.after(int(1000/gif_image.info['duration']), update_image)
#
# # Lancer l'animation
# update_image()


def update_image(gif_image, ctk_image, label):
    try:
        gif_image.seek(gif_image.tell() + 1)
    except EOFError:
        gif_image.seek(0)
    ctk_image.configure(light_image=gif_image)
    label.after(int(1000 / gif_image.info['duration']), lambda: update_image(gif_image, ctk_image, label))


class Admin(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True)

        self.product_file = File.File("files/flux/produit")
        self.products = File.File('files/flux/produit').getData()

        if len(self.products) == 0:
            self.products.append("_Pas de produit_ Pas de produit_ pas de produit _Pas de produit")

        self.topFrame()

        self.leftFrame()

        self.rigthFrame()

    def topFrame(self):
        frame = CTkFrame(self, fg_color="blue")
        frame.pack(fill=X, side=TOP)
        #  buttons
        btnRapport = CTkButton(master=frame, text="Rapport des activites", font=("arial", 17),
                               text_color="black",
                               fg_color="white",
                               corner_radius=0,
                               hover_color="light blue",
                               command=lambda: self.call_report())
        btnRapport.grid(row=0, column=0, padx=5, pady=1)

        btnAddProd = CTkButton(master=frame, text="Ajouter Produit", font=("arial", 17), border_width=0,
                               text_color="black",
                               fg_color="white",
                               corner_radius=0,
                               hover_color="light blue",
                               command=lambda: self.call_product())
        btnAddProd.grid(row=0, column=1, padx=5, pady=1)

        if len(self.product_file.getData()) > 0:
            btnSuppProd = CTkButton(master=frame, text="Supprimer Produit", font=("arial", 17), border_width=0,
                                    text_color="black",
                                    fg_color="white",
                                    corner_radius=0,
                                    hover_color="light blue",
                                    command=lambda: self.call_deleteProd())
            btnSuppProd.grid(row=0, column=2, padx=5, pady=1)

    def call_product(self):
        Add_Product(master=self)

    def call_report(self):
        Rapport_View(self)

    def call_deleteProd(self):
        DeletProduit(self)

    def leftFrame(self):
        frameContent = CTkFrame(master=self)
        frameContent.pack(fill=BOTH, expand=True, side=LEFT)

        # open the gif image
        gif = Image.open("view/icons/logo_market_stall.jpg")
        # convert it into a gif image
        ctk_image = CTkImage(light_image=gif, dark_image=gif, size=(700, 600))

        # create a label that should contain the gif animated
        logo_label = CTkLabel(master=frameContent, image=ctk_image, text="")
        logo_label.pack(fill=BOTH, expand=True)

        # calling a static function for updating image
        # update_image(gif, ctk_image, logo_label)

    def rigthFrame(self):
        # content frame side right
        contentFrame = CTkFrame(master=self, width=int(self.winfo_screenheight() / 2))
        contentFrame.pack(fill=BOTH, side=RIGHT, expand=True)

        # adding the statistique prod widget here
        self.statistique_prod_command(contentFrame)

        # adding the price manager prod widget here
        self.price_manager_prod(contentFrame)

        return contentFrame

    def statistique_prod_command(self, master):
        # statistique product
        frame = CTkFrame(master=master)
        frame.pack(fill=BOTH, expand=True)
        produit = Produit.Produit([a.split('_')[1] for a in self.products][0].upper())

        CTkLabel(master=frame, text="Performance produit", font=("arial", 20),
                 text_color="light green").grid(row=0, column=1, pady=10, padx=10)

        CTkLabel(master=frame, text="Produit  :  ").grid(row=1, column=0, pady=10, padx=10)

        combo_Produit = CTkComboBox(master=frame,
                                    values=[functions.get_user_string(a.split("_"
                                                                              "")[1]) for a in self.products],
                                    width=375, height=30)
        combo_Produit.grid(row=1, column=1, pady=10, padx=10)

        title_stat = CTkLabel(master=frame,
                              text=f"STATISTIQUE DE {functions.get_user_string(str(produit.get_name().upper()))}",
                              width=400, height=30, text_color="light blue")

        achat_pieces = CTkLabel(master=frame,
                                text=f"{produit.get_achat_total_pieces()}"
                                     f" pieces a {functions.get_user_string(str(produit.get_achat_total_price()))}"
                                     f"  $", font=("arial", 15), height=30)

        vente_pieces = CTkLabel(master=frame,
                                text=f"{produit.get_vente_total_pieces()} pieces a {produit.get_vente_total_price()}"
                                     f"  $", font=("arial", 15), height=30)

        partial_benefits = CTkLabel(master=frame,
                                    text=f"{produit.get_real_benefits()}",
                                    font=("arial", 15), height=30)

        benefits = CTkLabel(master=frame,
                            text=f"{produit.get_general_benefit()}",
                            font=("arial", 15), height=30)

        btn_statistique = CTkButton(master=frame, text="VOIR LES STATISTIQUE",
                                    command=lambda: self.statitics_info(title_stat, combo_Produit, achat_pieces,
                                                                        vente_pieces,
                                                                        benefits),
                                    height=30)
        btn_statistique.grid(row=2, column=1, pady=20, padx=2)

        title_stat.grid(row=3, column=1, pady=10, padx=10)

        CTkLabel(master=frame, text="Total Achat : ", font=("arial", 15), height=30).grid(row=4, column=0, padx=2,
                                                                                          pady=10)
        achat_pieces.grid(row=4, column=1, pady=10, padx=10)

        CTkLabel(master=frame, text="Total Vente : ", font=("arial", 15), height=30).grid(row=5, column=0, padx=5,
                                                                                          pady=10)
        vente_pieces.grid(row=5, column=1, pady=10, padx=10)

        CTkLabel(master=frame, text="Benefice :", font=("arial", 15), height=30).grid(row=6, column=0, padx=5, pady=10)
        partial_benefits.grid(row=6, column=5, pady=10, padx=10)
        CTkLabel(master=frame, text="Benefice total :", font=("arial", 15), height=30).grid(row=7, column=0, padx=5,
                                                                                            pady=10)
        benefits.grid(row=7, column=1, pady=10, padx=10)

    def price_manager_prod(self, master):
        # price manage space
        frame_price_manage = CTkFrame(master=master)
        frame_price_manage.pack(fill=BOTH, expand=True)

        # price manage widgets
        CTkLabel(master=frame_price_manage, text="Gestion des prix", font=("roboto", 20),
                 text_color="light green").grid(row=0, column=1, padx=10)

        prod_name = CTkComboBox(master=frame_price_manage,
                                values=[functions.get_user_string(a.split("_")[1]) for a in self.products],
                                width=375, height=30)
        prod_name.grid(row=1, column=1, pady=2, padx=2, )

        entry_new_price_manager = CTkEntry(master=frame_price_manage, placeholder_text="Entrer le nouveau prix",
                                           font=("roboto", 13), height=30, width=375)
        entry_new_price_manager.grid(row=2, column=1, pady=2, padx=2)

        btn_price_manager = CTkButton(master=frame_price_manage, text="modifier", font=("roboto", 15),
                                      height=20,
                                      command=lambda: self.setprice(prod_name.get(), entry_new_price_manager.get()))
        btn_price_manager.grid(row=3, column=1)

    def setprice(self, nameProduct: str, newPrice: str):
        if functions.is_not_empty_string(nameProduct, newPrice):
            prod = Produit.Produit(nameProduct)
            if prod.is_produit_valid():
                if newPrice.isnumeric():
                    precedent_price = prod.get_price_vente()[0]
                    prod.set_price(int(newPrice))
                    messagebox.showinfo("Changement reussi", f"Le prix {precedent_price} du produit "
                                                             f"{prod.get_name()} a ete changer en {newPrice}")
                else:
                    messagebox.showerror("Erreur de valeur", f"Le champs {newPrice} doit etre un nombre")
            else:
                messagebox.showerror("Produit non existant", "Impossible de changer le prix d'un produit qui n'existe"
                                                             "pas")
        else:
            messagebox.showerror("Formulaire incomplet", "Veuiller complete tout les champs")

    def statitics_info(self, title_stat, combo_Produit, achat_pieces, vente_pieces, benefits):
        """
        :param combo_Produit:the combo box that has the product
        :param achat_pieces: the label of buyed pieces
        :param vente_pieces: the label of the selled pieces
        :param benefits: the label of the benefits dispal
        :return: this function displays some information according to a product in the given labels which are the param
        """
        prod = Produit.Produit(combo_Produit.get())
        title_stat.configure(text=f"Statistique de {functions.get_user_string(prod.get_name())}")
        achat_pieces.configure(text=f"{functions.get_user_string(prod.get_achat_total_pieces())} pices a "
                                    f"{functions.get_user_string(prod.get_achat_total_price())} Dollares")
        vente_pieces.configure(text=f"{functions.get_user_string(prod.get_vente_total_pieces())} pieces a "
                                    f"{functions.get_user_string(prod.get_vente_total_price())} dollares")
        benefits.configure(text=f"{prod.get_general_benefit()}")

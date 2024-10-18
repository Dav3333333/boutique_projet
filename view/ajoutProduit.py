import customtkinter
from customtkinter import *
from classes.File import File
from tkinter import messagebox
import view.functions as extern_func


class Add_Product(CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.transient(master)

        self.prod_file = File("files/flux/produit")

        self.products_list = [extern_func.get_user_string(a.split("_")[1]) for a in self.prod_file.getData()]

        self.geometry("900x500+0+0")
        self.title("AJOUT PRODUIT")

        self.tit = CTkLabel(master=self, text="PRODUIT", font=("arial", 20), bg_color="white",
                            fg_color="blue")
        self.tit.pack(padx=10, pady=10, fill=customtkinter.X)

        # creation of the frame that will the field widget for the adding product
        self.princFrame = customtkinter.CTkFrame(master=self)
        self.princFrame.pack(padx=2, pady=2, expand=True)

        self.frame_add()

        self.grab_set()  # restraint the communication with other windows
        self.wait_window()  # wait the top level be closed before continue

    def frame_add(self):
        frame = CTkFrame(self.princFrame)
        frame.pack(fill=BOTH, expand=True, side=LEFT)

        # ***creation of the widget of the systeme
        # form label
        CTkLabel(master=frame, text="CREE (AJOUTER)", font=("arail", 25), anchor="w").pack(padx=10, pady=10)
        # name
        nom = CTkEntry(master=frame, placeholder_text="NOM DU PRODUIT", font=("roboto", 15), width=475)
        nom.pack(padx=10, pady=10)

        # initial price
        initPrace = CTkEntry(master=frame, placeholder_text="PRIX DE VENTE DU PRODUIT", font=("roboto", 15),
                             width=475)
        initPrace.pack(padx=10, pady=10)

        btnSubmit = CTkButton(master=frame, text="Creer", font=("roboto", 15), width=335,
                              fg_color="blue",
                              command=lambda: self.add_product(nom, initPrace))
        btnSubmit.pack(padx=10, pady=10)

    def add_product(self, nom: CTkEntry, prix: CTkEntry):
        nom = extern_func.convert_user_string(nom.get().strip()).lower()
        prix = extern_func.convert_user_string(prix.get().strip()).lower()
        id = int(self.prod_file.get_last_id()) + 1
        if extern_func.is_not_empty_string(nom, prix):
            if not prix.isnumeric():
                messagebox.showerror("Erreur de completion", "Vous avez tentez de passez un text comme prix,"
                                                             "veuillez entrer un nombre")
            else:
                if len(self.prod_file.getData()) > 0:
                    if nom.strip() in self.products_list:
                        messagebox.showerror("Product inexistant", "Le produit que vous tentez ajouter existe deja")
                    else:
                        self.prod_file.saveData(f"{id}_{nom}_{prix}_{extern_func.dateDuJour()}")
                        messagebox.showinfo("Produit ajouter", f"Ajout reussi")
                        self.products_list.append(nom)
                else:
                    self.prod_file.saveData(f"{1}_{nom}_{prix}_{extern_func.dateDuJour()}")
                    messagebox.showinfo("Produit ajouter", f"Ajout reussi")
                    self.products_list.append(nom)
        else:
            messagebox.showerror("Formulaire incomplet", "Veuillez completez tout le formulaire")

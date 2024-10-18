from view.ajoutProduit import *
from classes.Produit import Produit
from tkinter import StringVar


class DeletProduit(Add_Product):
    def __init__(self, master):
        super().__init__(master)
        self.radio_button = None

    def frame_add(self):
        frame = CTkFrame(self.princFrame)
        frame.pack(fill=BOTH, expand=True, side=RIGHT)

        # ***creation of the widget of the systeme
        # form label
        CTkLabel(master=frame, text="SUPPRIMER", font=("arail", 25), anchor="w").pack(padx=10, pady=10)
        # name
        typeFrame = CTkFrame(master=frame, width=475)
        typeFrame.pack(padx=10, pady=10)

        if len(self.products_list) > 0:
            CTkLabel(master=typeFrame, text="NOM DU PRODUIT : ", font=("roboto", 15)).grid(row=0, column=0)
            name_prod = CTkComboBox(master=typeFrame,
                                    values=self.products_list,
                                    font=("roboto", 15), width=335)
            name_prod.grid(row=0, column=1, padx=2)

            # supprimer_operations
            CTkLabel(master=frame, text="Voulez-vous supprimer meme les operations liees au produit?").pack()

            radio_str_var = StringVar(value="")

            ans_yes = CTkRadioButton(master=frame, text="OUI", fg_color="red",
                                     variable=radio_str_var, value="1",
                                     command=lambda: self.radio_button_manager())
            ans_yes.pack()
            ans_no = CTkRadioButton(master=frame, text="NON", fg_color="green",
                                    variable=radio_str_var, value="0",
                                    command=lambda: self.radio_button_manager())
            ans_no.pack()

            btnSubmit = CTkButton(master=frame, text="DELETE", font=("roboto", 15), width=335,
                                  fg_color="blue",
                                  command=lambda: self.delete_product(name_prod.get(), radio_str_var.get()))
            btnSubmit.pack(padx=10, pady=10)
        else:
            typeFrame.destroy()
            CTkLabel(frame, text="Il y pas de produit disponible dans le stock pour l'instant.",
                     font=("arial", 20), text_color="red", fg_color=("white", "white")).pack(padx=20, pady=20)

    def radio_button_manager(self):
        pass

    def delete_product(self, nom: str, choice: str):
        if extern_func.is_not_empty_string(nom, choice):
            if nom.strip() in self.products_list:
                prod = Produit(nom)
                ans = messagebox.askyesno("Suppression produit", f"Voulez vous vraiment supprimer {nom} ?")
                if ans is True:
                    if choice.strip() == "0":
                        prod.delete_product()
                        messagebox.showinfo("Suppression produit", f"{nom} Supprimer")
                    elif choice.strip() == "1":
                        prod.delete_all_operations()
                        prod.delete_product()
                        messagebox.showinfo("Suppression produit", f"{nom} Supprimer")
                else:
                    messagebox.showinfo("Suppression produit", f"{nom} N'a pas ete suppimer ")
            else:
                messagebox.showinfo("Suppression produit", f"Le produit {nom} n'existe pas")
        else:
            messagebox.showerror("Suppression produit", f"Le formulaire doit etre remplit au complet")

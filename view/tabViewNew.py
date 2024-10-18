import tkinter
import customtkinter
import classes.File as File

from view.achat import AchatFrame
from view.vente_oop import VenteFrame
from view.admin import Admin


class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")
        self.title("STALL TOOL")
        self.iconbitmap("view/icons/Main_logo.ico")

        self.__screen_width = self.winfo_screenwidth()
        self.__screen_height = self.winfo_screenheight()

        self.geometry(f"{self.__screen_width}x{self.__screen_height}+0+0")
        self.resizable(True, True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.onglet = ['VENTE', "ACHAT", 'GESTION']
        self.opened_onglet = None

        self.menu_frame = customtkinter.CTkFrame(master=self)
        self.menu_frame.pack(side="top")

        self.content_frame = customtkinter.CTkFrame(master=self)
        self.content_frame.pack(fill=customtkinter.BOTH, expand=True)

        """initialization of files used in each class """
        self.identif_product_type_file = File.File("files/flux/identifTypeProduit")
        self.product_file = File.File("files/flux/produit")  # product file
        self.file_flux_file = File.File("files/flux/fluxfile")  # products flux file

        if len(self.product_file.get_All_Data()) == 0:
            self.product_file.saveData("id_nomProd_typeProd_prixProd_dateAjout")

        if len(self.identif_product_type_file.get_All_Data()) == 0:
            self.identif_product_type_file.saveData("id_nomProduit_dateCreation")

        if len(self.file_flux_file.get_All_Data()) == 0:  # verififying if there is data in the file
            self.file_flux_file.saveData(
                "id_dateActitive_nomProduit_libelle_quantite_prixVenteUnitaire_prixtot_nomFsseurouClient")

        self.createTables()

        if self.opened_onglet is None:
            onglet = self.menu_frame.winfo_children()[0]
            onglet.configure(fg_color="blue")

        self.get_onglet_content(0)

    def createTables(self):
        for i, ong in enumerate(self.onglet):
            onglet = customtkinter.CTkButton(master=self.menu_frame, text=f"{ong}",
                                             width=int(self.__screen_width / len(self.onglet) / 2),
                                             border_width=0,
                                             corner_radius=0,
                                             font=("roboto", 18),
                                             fg_color="grey",
                                             command=lambda idx=i: self.get_onglet_content(idx, button=(onglet)))
            onglet.grid(row=0, column=i)

    def get_onglet_content(self, index, button: customtkinter.CTkButton = None):
        if self.opened_onglet is not None:
            self.clear_onglet_content()
            for onglet in self.menu_frame.winfo_children():
                if onglet.cget("text") == self.onglet[index]:
                    onglet.configure(fg_color="blue")
                else:
                    onglet.configure(fg_color="gray")

        self.opened_onglet = index
        self.frame = customtkinter.CTkFrame(self.content_frame)
        self.frame.pack(fill="both", expand=True)

        # add content for each table

        if index == 0:
            VenteFrame(self.frame,
                       product_file=self.product_file,
                       file_flux_File=self.file_flux_file)
        elif index == 1:
            AchatFrame(self.frame,
                       fluxFile=self.file_flux_file,
                       products_file=self.product_file,
                       identif_prod_file=self.identif_product_type_file)
        elif index == 2:
            Admin(self.frame)

    def clear_onglet_content(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        fenGeneral = self
        # fenGeneral.geometry("2000x1000+0+0")

        screen_width = fenGeneral.winfo_screenwidth()
        screen_height = fenGeneral.winfo_screenheight()

        fenGeneral.geometry(f"{screen_width}x{screen_height}+{0}+{0}")

        fenGeneral.resizable(True, True)

        fenGeneral.grid_rowconfigure(0, weight=1)
        fenGeneral.grid_columnconfigure(0, weight=1)

        # Creation of the tab view widget
        tabView = customtkinter.CTkTabview(fenGeneral, width=200)
        tabView.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)

        # adding the layer to the tabView object
        tabView.add("VENTE")
        tabView.add("ACHAT")
        # tabView.add("CAISSE")
        tabView.add("GESTION")

        # setting the defalt tab view
        tabView.set("VENTE")

        tabView.segmented_button.configure(font=("roboto", 20))

        """initialization of files used in each class """
        identif_product_type_file = File.File("files/flux/identifTypeProduit")
        product_file = File.File("files/flux/produit")  # product file
        file_flux_file = File.File("files/flux/fluxfile")  # products flux file

        if len(product_file.get_All_Data()) == 0:
            product_file.saveData("id_nomProd_typeProd_prixProd_dateAjout")

        if len(identif_product_type_file.get_All_Data()) == 0:
            identif_product_type_file.saveData("id_nomProduit_dateCreation")

        if len(file_flux_file.get_All_Data()) == 0:  # verififying if there is data in the file
            # file_flux_file.saveData(
            #     "id_dateActitive_nomProduit_libelle_quantite_prixVenteUnitaire_prixtot_nomFsseurouClient")
            pass

        """ giving every objet to its tab in the tab view """
        AchatFrame(tabView.tab("ACHAT"),
                   fluxFile=file_flux_file,
                   products_file=product_file,
                   identif_prod_file=identif_product_type_file)

        VenteFrame(tabView.tab("VENTE"),
                   product_file=product_file,
                   file_flux_File=file_flux_file)

        Admin(master=tabView.tab("GESTION"))


"""
task i have to do for all the app is  : 
* Admin :
    - to solve the problem of solving un exist product in the store of the app (done)
    - to finish the screen of the rapport (one part is done only the desing) (done in an other way)
    - to finish the screen of add product screen 
    - to finish the screen the screen of manage agent
    - to finish all the top level screen and link every to its button 
    - to finish the pdf generator of repport
"""

"""
Task for the screen in admin pacakge specificaly the screen of rapport in poo: 
- start to desing the interface
- do the logic of the application
- put functionalities in all the buttons of the interface
"""

"""
Task for the screen in admin package the add_product screen:

"""

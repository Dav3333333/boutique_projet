import calendar
import datetime
from customtkinter import *
from tkcalendar import Calendar
from tkinter import ttk, messagebox
import classes.Produit as prod
from classes.Rapport import Rapport
from classes.My_Pdf import My_Pdf
import os


def is_not_empty_data(data: list):
    if len(data) > 0:
        return True
    else:
        return messagebox.showinfo("Donne vide", "Il y a pas de donne pour cette periode")


def get_month_name(month_number: int):
    if 1 <= month_number <= 12:
        return calendar.month_name[month_number]
    else:
        return calendar.month_name[1]


class Rapport_View(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.transient(master)  # link the top level to its master

        # The title
        CTkLabel(master=self, text="RAPPORT DES ACTIVITES", font=("roboto", 30),
                 bg_color="#14469E").pack(padx=0, pady=1, fill=X)

        self.title("RAPPORT DES ACTIVITES")
        self.geometry("2000x700+0+0")

        """Frames of my admin report"""
        self.frame1Buttons = CTkFrame(master=self)
        self.frame1Buttons.pack(padx=1, pady=1, fill=X)

        self.frame2Content = CTkFrame(master=self)
        self.frame2Content.pack(fill=BOTH, expand=True, pady=1, padx=1)

        self.frame3TeeveDisplay = CTkFrame(master=self.frame2Content)
        self.frame3TeeveDisplay.pack(fill=BOTH, expand=True, )

        # call the two parts of our program
        self.menu_buttons(master=self.frame1Buttons)
        self.trev = self.treev_object(self.frame3TeeveDisplay)

        self.grab_set()  # restraint the communication with other windows
        self.wait_window()  # wait the top level be closed before continue

    """frames of the report section"""

    # frame for treev display
    def menu_buttons(self, master):
        selected_option = StringVar()
        selected_option.set("Jour")
        # buttons widget and functionnalities of heads
        btnDownload = CTkButton(master=master, text="IMPRIMER", fg_color="green",
                                font=("arial", 20))
        btnDownload.grid(row=0, column=0, padx=100, pady=10)

        separtorLab = CTkLabel(master=master, text="|", font=("arial", 30))
        separtorLab.grid(row=0, column=2, padx=10, pady=10)

        CTkLabel(master=master, text="Rapport par : ", font=("arial", 15)).grid(row=0, column=3,
                                                                                padx=2, pady=2)

        comboBoxAnneeChoice = CTkComboBox(master=master, values=["Jour", "Mois", "Annee"],
                                          font=("arial", 20), variable=selected_option)
        comboBoxAnneeChoice.grid(row=0, column=4, padx=5, pady=10)

        # calender object calender
        comboBoxChoice = Calendar(master=master, selectmode="day",
                                  year=int(datetime.datetime.now().strftime("%Y")),
                                  month=int(datetime.datetime.now().strftime("%m")),
                                  day=int(datetime.datetime.now().strftime("%d")))
        comboBoxChoice.grid(row=0, column=6)

        btnPrint = CTkButton(master=master, text="TELECHARGER", fg_color="green", font=("arial", 20),
                             command=lambda: self.downloadPdf(comboBoxChoice, selected_option))
        btnPrint.grid(row=0, column=1, padx=100, pady=10)

        btnSetChoice = CTkButton(master=master, text="AFFICHER", font=("arial", 20),
                                 fg_color="#C68E17", command=lambda: self.affRapport(selected_option, comboBoxChoice,
                                                                                     self.trev))
        btnSetChoice.grid(row=0, column=7, padx=1, pady=10)

        selected_option.trace("w", lambda *args: self.control_combo_box(selected_option, comboBoxChoice))

    def treev_object(self, master):
        # creating the trev
        tab = ttk.Treeview(master, selectmode="browse")
        tab.pack(padx=20, pady=20, fill=BOTH, expand=True)

        # creating the treev's scrollBar
        trevSCrollBar = ttk.Scrollbar(tab, orient="vertical", command=tab.yview)
        trevSCrollBar.pack(side="right", fill=Y)

        # configure the treev
        tab.configure(yscrollcommand=trevSCrollBar.set)
        tab["columns"] = ("1", "2", "3", "4", "5", "6")

        tab["show"] = "headings"

        tab.column("1", width=10, anchor="c")
        tab.column("2", width=90, anchor="c")
        tab.column("3", width=90, anchor="c")
        tab.column("4", width=90, anchor="c")
        tab.column("5", width=90, anchor="c")
        tab.column("6", width=90, anchor="c")

        tab.heading("1", text="NUMERO")
        tab.heading("2", text="CODE PRODUIT")
        tab.heading("3", text="LIBELLE")
        tab.heading("4", text="QUANTITE")
        tab.heading("5", text="PRIX")
        tab.heading("6", text="PRIX TOT")

        return tab

    def affRapport(self, selected_option: StringVar, comboBoxChoice, tab: ttk.Treeview):
        """
        :return: this function display repport according to the user enters
        """
        rap = Rapport("files/flux/")
        option = selected_option.get()

        # the variable that store the date
        option_val_seleted = datetime.datetime.strptime(comboBoxChoice.get_date(), "%m/%d/%y").strftime("%d/%m/%Y")
        if isinstance(comboBoxChoice, Calendar) and option.lower() == "jour":
            report = rap.dailly_rapport(option_val_seleted)
            tab.delete(*tab.get_children())
            if is_not_empty_data(report):
                compteur = 1
                for i in range(len(report)):
                    tab.insert("", "end", text="1",
                               values=(f"{compteur}", f"{report[i].split('_')[2]}", f"{report[i].split('_')[3]}"
                                       , f"{report[i].split('_')[4]}", f"{report[i].split('_')[5]}",
                                       f"{report[i].split('_')[6]}"))
                    compteur += 1

        elif isinstance(comboBoxChoice, Calendar) and option.lower() == "mois":
            report = rap.month_rapport(get_month_name(int(option_val_seleted.split("/")[-2])))
            tab.delete(*tab.get_children())
            if is_not_empty_data(report):
                compteur = 1
                for i in range(len(report)):
                    tab.insert("", "end", text="1",
                               values=(f"{compteur}", f"{report[i].split('_')[2]}", f"{report[i].split('_')[3]}"
                                       , f"{report[i].split('_')[4]}", f"{report[i].split('_')[5]}",
                                       f"{report[i].split('_')[6]}"))
                    compteur += 1

        elif isinstance(comboBoxChoice, Calendar) and option.lower() == "annee":
            report = rap.year_repport(int(option_val_seleted.split("/")[-1]))  # getting data from the year from the
            # date
            tab.delete(*tab.get_children())
            if is_not_empty_data(report):
                compteur = 1
                for i in range(len(report)):
                    tab.insert("", "end", text="1",
                               values=(f"{compteur}", f"{report[i].split('_')[2]}", f"{report[i].split('_')[3]}"
                                       , f"{report[i].split('_')[4]}", f"{report[i].split('_')[5]}",
                                       f"{report[i].split('_')[6]}"))
                    compteur += 1

    def service_years(self):
        first_year = int(prod.File("files/dataBase/flux_date_app").getData()[0].split("_")[2])
        actual_year = int(datetime.datetime.now().strftime("%Y"))
        list_years = [str(first_year)]
        if first_year < actual_year:
            for i in range(first_year, actual_year + 1):
                list_years.append(str(i))
            return list_years
        elif first_year == actual_year:
            return list_years
        return list_years

    def control_combo_box(self, selected_option: StringVar, *args):
        disp = selected_option.get()
        if disp.lower().strip() == "mois":
            messagebox.showinfo(title="Rassurrez-vous", message="Rassurrez-vous que vous allez selectionner un jour "
                                                                "dans le mois voulu")
        elif disp.lower().strip() == "jour":
            messagebox.showinfo(title="Rassurrez-vous", message="Rassurrez-vous que vous allez selectionner un jour")
        elif disp.lower().strip() == "annee":
            messagebox.showinfo(title="Rassurrez-vous", message="Rassurrez-vous que vous allez selectionner un jour "
                                                                "dans l'annee voulu")

    def __value_date_returned(self, date_str: str, value: str):
        """
        :param date_str: this is the date string to be cheked
        :param value: this is the type of value to be return (annee, mois, jour)
        :return: return a value according to the given value
        """
        if "/" in date_str and len(date_str.split("/")) == 3:
            value = value.strip().lower()
            date_str = date_str.strip()
            if value == "jour":
                return date_str
            elif value == "mois":
                return get_month_name(int(date_str.split("/")[-2]))
            elif value == "annee":
                return date_str.split("/")[-1]

    def downloadPdf(self, comboBoxChoice, selected_option):
        """
        :return: this function display repport according to the user enters
        """
        pdf = self.__make_pdf(comboBoxChoice, selected_option)
        if isinstance(pdf, My_Pdf):
            pdf.saveFile()
        elif pdf is None:
            messagebox.showinfo("Erreur document", "Le document est vide")

    def __make_pdf(self, comboBoxChoice, selected_option) -> My_Pdf:
        rap = Rapport()
        value = datetime.datetime.strptime(comboBoxChoice.get_date(), "%m/%d/%y").strftime("%d/%m/%Y")

        option = self.__value_date_returned(value, selected_option.get()).strip()

        data = rap.getRapport(option)

        if is_not_empty_data(data):
            pdf = My_Pdf(data)
            pdf.write_body()
            return pdf
            # pdf.saveFile()

    def printPdf(self, comboBoxChoice, selected_option):
        pdf = self.__make_pdf(comboBoxChoice, selected_option)
        if isinstance(pdf, My_Pdf):
            file = pdf.get_temp_file_pdf()



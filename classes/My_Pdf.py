from tkinter import filedialog
from fpdf import FPDF
import tempfile


class My_Pdf(FPDF):
    def __init__(self, data: list):
        super().__init__()
        self.temp_file = ""
        self.cause = "Rapport"
        self.data = data

    def header(self):

        """
        :return: write automatically the head on the pdf when the object is instanced
        """
        pass

    def footer(self):
        pass

    def write_foot(self):
        """
        :return: write automatically the footer where the object is instanced in the pdf format
        """
        pass

    def write_body(self):
        """
        :return:
        """
        # adding a page first
        self.add_page()
        # logo
        # self.image("pdf reading/Capture.PNG", 10, 8, 25)
        # font
        self.set_font("helvetica", "B", 15)
        # padding
        self.cell(20)
        # title
        """ all so here we must use the """
        html = ("<table border='1'>"
                "<tr><td>DAVID LUSENGE ETS </td></tr>"
                "<tr><td>ADRESSE: BENI/KANZULI/AV NYESHA NUMERO 1234/ GALERIE OKAY </td></tr>"
                "<tr><td>RAPPORT NUMERO: - 1900 </td></tr>"
                "</table>")

        self.write_html(html)
        # line break
        self.set_font("helvetica", "B", 10)
        self.ln()

        for row in self.data:
            for element in row:
                self.cell(35, 10, f"{element}", border=1, align="c")
            self.ln()

    def saveFile(self):
        """
        :return: save the pdf on users path desired
        """
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf*")])
        if file:
            self.output(f"{file}")

    def get_temp_file_pdf(self):
        """
        :return: save the out put in a temporary file
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as file:
            self.output(file.name)
            return file

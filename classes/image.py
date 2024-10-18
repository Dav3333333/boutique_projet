from tkinter import PhotoImage, Tk, Button


class Button_Image:
    def __int__(self, master, path):
        self.pather = path
        self.masters = master

    def add_to_button(self):
        """
        :return: add image to a button
        """
        image = PhotoImage(file=r"{}".format(self.pather), master=self.masters)
        im = image.subsample(20, 30)
        return im


class Dav:
    def __int__(self, name: str):
        self.nam = name

    def print_name(self):
        print(self.nam)



# fen = Tk
# img = Button_Image()
# but = Button(fen, image=)

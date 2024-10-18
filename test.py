# import tkinter, tkcalendar
# import calendar


# def aff():
#     global cal
#     ans = cal.selection_get()
#     print(ans, cal.get_displayed_month())
#     print(get_month_name(cal.get_displayed_month()[0]))
#
#
#
#
# def get_month_name(month_number):
#     if 1 <= month_number <= 12:
#         return calendar.month_name[month_number]
#     else:
#         return calendar.month_name[1]
#
#
# root = tkinter.Tk()
#
# cal = tkcalendar.Calendar(root)
# cal.pack()
#
# btn = tkinter.Button(root, text="get", command=aff)
# btn.pack()
#
# root.mainloop()


# import tkinter, tkcalendar
# from tkinter import ttk
#
#
# def voir(trev:ttk.Treeview):
#     if trev.selection():
#         element = trev.item(trev.selection()[0])
#         print(element)
#
#
#
#
# root = tkinter.Tk()
#
# trev = ttk.Treeview(root)
#
# trev["columns"] = ("1", "2")
# trev["show"] = "headings"
#
# trev.column("1", width=100, minwidth=50)
# trev.column("2", width=100, minwidth=50)
#
# trev.heading("1", text="Titre", image="Capture.PNG", anchor="c", command="...")
# trev.heading("2", text="Nom", image="Capture.PNG", anchor="c", command="...")
#
# trev.insert("", "end", text=f"{1}", values=("La vie", "j'aime vivre"))
# trev.insert("", "end", text=f"{1}", values=("La vie et la mort", "la mort est pour tous"))
#
# trev.pack()
#
# btn_trev = tkinter.Button(root, text="VOIR", command=lambda : voir(trev))
# btn_trev.pack()
#
# root.mainloop()
#
# with open("david.txt","") as f:
#     print(f.read().split("\n"))


# from tkinter import *
#
# root = Tk()
#
# btn2 = Button(root, text="prince")
# btn2.pack()
#
# btn = Button(root, text='david', height=int((root.winfo_screenheight()*0.01)), bg="red")
# btn.pack(side=BOTTOM, fill=X)
#
# root.mainloop()

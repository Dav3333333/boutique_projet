import cx_Freeze
import sys
import customtkinter
import tkinter

base = None

if sys.platform == "win32":
    base = "Win32GUI"

# Liste des modules à inclure
includefiles = []

# "App/classes/_save_icon.png",  "","App/view/icon"
# "App/classes/Agent.py", "App/classes/File.py", "App/classes/image.py",
#                 "App/classes/My_pdf.py", "App/classes/produit.py", "App/classes/Rapport.py",
#                 "App/files/flux/fluxFile.txt","App/files/flux/flux_date_app.txt","App/files/flux/produit.txt",
#                 "App/files/flux/identifTypeProduit", "App/view/achat.py", "App/view/addAgent.py","App/view/admin.py"

# Options de construction
options = {
    'build_exe': {
        'packages': ["customtkinter", "tkinter", "PIL", "datetime"],
        'includes': includefiles
    }
}

# Exécutable
executables = [
    cx_Freeze.Executable('main.py',
                         base=base,
                         icon="App/Capture.PNG")
]

cx_Freeze.setup(
    name="INventorier",
    version="0.1",
    description="Une application créée avec cx_freeze",
    options=options,
    executables=executables
)

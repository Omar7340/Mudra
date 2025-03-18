# Objectif : Generer un dataset de coordonnees pour une suite de position de main
# Etapes
# 1. Demander a l'utilisateur le label de la position de main
# 2. Demander a l'utilisateur de positionner sa main
# 3. Capturer la position de la main
# 4. Sauvegarder la position de la main dans un json ou csv
# 5. Repeter les etapes 1 a 4 jusqu'a ce que l'utilisateur decide d'arreter
# 6. Fermer la fenetre de capture
# 7. Sauvegarder le dataset dans un fichier

import customtkinter

positions = []

WIDTH = 500
HEIGHT = 400

class AddPosition(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Add position")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Give a label to the position (if blank the position will have index as label)")
        self.label.grid(row=0, column=0, sticky="ew")

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry(str(HEIGHT) + "x" + str(WIDTH))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="List of position")
        self.label.grid(row=0, column=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Some example text!\n" * 50)

        self.button = customtkinter.CTkButton(self, text="Capture position", command=self.capture_position)
        self.button.grid(row=2, column=0, sticky="ew")
    
        self.capture_window = None
    
    def print_positions(self):
        i = 0
        for position in positions:
            i += 1
            self.textbox.insert("end", str(i) + ". " + position + "\n")

    def capture_position(self):
        if self.capture_window is None or not self.capture_window.winfo_exists():
            self.capture_window = AddPosition(self)  # create window if its None or destroyed
        self.capture_window.focus()  # if window exists focus it


app = App()
app.mainloop()
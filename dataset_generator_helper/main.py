# Objectif : Generer un dataset de coordonnees pour une suite de position de main
# Etapes
# 1. Demander a l'utilisateur le label de la position de main
# 2. Demander a l'utilisateur de positionner sa main
# 3. Capturer la position de la main
# 4. Sauvegarder la position de la main dans un json ou csv
# 5. Repeter les etapes 1 a 4 jusqu'a ce que l'utilisateur decide d'arreter
# 6. Fermer la fenetre de capture
# 7. Sauvegarder le dataset dans un fichier

import customtkinter as ctk
from opencv_frame import OpenCVFrame
from position_manager import PositionManager
from scrollable_label import ScrollableLabels
positions = [
{'label': '1', 'position': ""},
{'label': '2', 'position': ""},
{'label': '3', 'position': ""},
{'label': '4', 'position': ""}
    ]

WIDTH = 500
HEIGHT = 400




class AddPosition(ctk.CTkFrame):
    def __init__(self, master, position_manager : PositionManager, **kwargs):
        super().__init__(master, **kwargs)

        self.pm = position_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.canvas = OpenCVFrame(master=self)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.take_snapshot_btn = ctk.CTkButton(self, text="Take snapshot", command=self.take_snapshot)
        self.take_snapshot_btn.grid(row=3, column=0, sticky="nsew")

    def take_snapshot(self):
        global positions

        self.canvas.freeze_frame()
        current_pos = self.canvas.get_current_position()

        if current_pos is not None:
            img, pos = current_pos
            label = "pos-{}".format(self.pm.len()+1)
            # TODO fix error remove 
            self.pm.add_position(label, pos)
            print("Position saved")
            print(label)
            print(pos)
        else:
            print("No position to save")

    def destroy(self): # TODO: implement destroy method
        self.canvas.clean_up()
        super().destroy()

class PositionFrame(ctk.CTkFrame):
    def __init__(self, master, position_manager, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="List of position")
        self.label.grid(row=0, column=0, sticky="ew")

        self.label_positions = ScrollableLabels(master=self, position_manager=position_manager)
        self.label_positions.grid(row=1, column=0, sticky="nsew")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dataset Generator Helper")
        self.minsize(WIDTH, HEIGHT)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.pm = PositionManager()

        self.positions_frame = PositionFrame(master=self, position_manager=self.pm)
        self.positions_frame.grid(row=0, column=0, sticky="nsew")

        self.capture_frame = AddPosition(master=self, position_manager=self.pm)
        self.capture_frame.grid(row=0, column=1, sticky="nsew")

app = App()
app.mainloop()

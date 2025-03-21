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
from configs import *

import re
import os
import json

class AddPosition(ctk.CTkFrame):
    def __init__(self, master : ctk.CTk, position_manager : PositionManager, **kwargs):
        super().__init__(master, **kwargs)

        self.pm = position_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.canvas = OpenCVFrame(master=self)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.take_snapshot_btn = ctk.CTkButton(self, text="Take snapshot (or press X)", command=self.take_snapshot)
        self.take_snapshot_btn.grid(row=3, column=0, sticky="nsew")

        master.bind(TAKE_SNAPSHOT_SHORTCUT, lambda e : self.take_snapshot())

    def take_snapshot(self):

        current_pos = self.canvas.get_current_position()

        if current_pos is not None:
            self.pm.add_position(current_pos)
            print("Position saved")
        else:
            print("No position to save")

    def destroy(self):
        self.canvas.clean_up()
        super().destroy()

class PositionFrame(ctk.CTkFrame):
    def __init__(self, master, position_manager, **kwargs):
        super().__init__(master, **kwargs)

        self.root = master

        self.pm = position_manager

        self.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="List of position")
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.label_positions = ScrollableLabels(master=self, position_manager=position_manager)
        self.label_positions.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.save_img_check = ctk.CTkCheckBox(self, text="Include Image")
        self.save_img_check.grid(row=2, column=0, pady=10)
        
        self.save_coord_check = ctk.CTkCheckBox(self, text="Include Landmark Coordinates")
        self.save_coord_check.grid(row=2, column=1, pady=10)


        self.save_btn = ctk.CTkButton(self, text="Save", command=self.save_handler)
        self.save_btn.grid(row=3, column=0, padx=(0, 10))

        self.quit_btn = ctk.CTkButton(self, text="Quit", command= lambda: self.root.destroy())
        self.quit_btn.grid(row=3, column=1)
    
    def save_handler(self):

        self.save_dialog = ctk.CTkInputDialog(text="Type the name of this dataset (it will be saved at {})".format(SAVE_PATH), title="Save Dataset")
        
        dataset_name = self.save_dialog.get_input()

        if dataset_name is None:
            return

        # Sanitize filename by removing invalid characters and ensure .json extension
        sanitized = re.sub(r'[<>:"/\\|?*]', '', dataset_name)

        if self.save_coord_check.get() == 1:
            self.save_positions(sanitized)
        
        if self.save_img_check.get() == 1:
            self.save_img(sanitized)
    
    def save_img(self, directory_name):
        imgs = self.pm.get_positions(include_coord=False)

        path = os.path.join(SAVE_PATH, directory_name + '/')
        os.makedirs(path, exist_ok=True)

        i = 1
        for item in imgs.values():
            filename = os.path.join(path, str(i) + '.jpg')
            item["img"].save(filename)
            i += 1
    
    def save_positions(self, filename):
        positions = self.pm.get_positions(include_img=False)

        if filename:
            if not filename.endswith('.json'):
                filename += '.json'
            
            # Create save directory if it doesn't exist
            os.makedirs(SAVE_PATH, exist_ok=True)
            
            # Save positions to JSON file
            save_file = os.path.join(SAVE_PATH, filename)
            with open(save_file, 'w') as f:
                json.dump(positions, f)
                print(f"Saved positions to {save_file}")

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
        self.positions_frame.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

        self.capture_frame = AddPosition(master=self, position_manager=self.pm)
        self.capture_frame.grid(row=1, column=1, sticky="nsew")
        

app = App()
app.mainloop()

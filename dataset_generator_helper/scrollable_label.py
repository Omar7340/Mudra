import customtkinter as ctk
from position_manager import PositionManager

class ScrollableLabels(ctk.CTkScrollableFrame):
    def __init__(self, master, position_manager : PositionManager, **kwargs):
        super().__init__(master, **kwargs)

        self.pm = position_manager
        self.pm.add_observer(self)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.list = []
    
    def clean(self):
        for i in self.list:
            i[0].destroy()
            i[1].destroy()
    
    def update_positions(self, positions : dict):
        self.clean()

        row = 0
        for k in positions.keys():
            label = ctk.CTkLabel(self, text=k)
            remove_btn = ctk.CTkButton(self, text="Remove", command= lambda: self.pm.remove_position(k))

            label.grid(row=row, column=0, sticky="nsew")
            remove_btn.grid(row=row, column=1, sticky="nsew")

            self.list.append((label, remove_btn))
            row += 1
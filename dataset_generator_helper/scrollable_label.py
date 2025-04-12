import customtkinter as ctk
from position_manager import PositionManager
from configs import PREVIEW_POS_H, PREVIEW_POS_W
from PIL import Image


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
        for k,v in positions.items():
            label = remove_btn = image = frame_img = None

            image = ctk.CTkImage(dark_image=v['img'], size=(PREVIEW_POS_W,PREVIEW_POS_H))
            frame_img = ctk.CTkLabel(self, image=image, text="")

            label = ctk.CTkLabel(self, text=k)
            remove_btn = ctk.CTkButton(self, text="Remove", command= lambda x=k: self.pm.remove_position(x))

            frame_img.grid(row=row, column=0, sticky="nsew", pady=4)
            label.grid(row=row, column=1, sticky="nsew", pady=4)
            remove_btn.grid(row=row, column=2, sticky="nsew", pady=4)

            self.list.append((frame_img, label, remove_btn))
            row += 1
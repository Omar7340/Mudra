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
import cv2
from PIL import Image

positions = []

WIDTH = 500
HEIGHT = 400

VIDEO_CAPTURE = 1  # 0 for default or back camera, 1 for external or front camera

FPS = 30
TIK = 1000 // FPS

class OpenCVFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cap = cv2.VideoCapture(VIDEO_CAPTURE)

        self.frame = customtkinter.CTkLabel(self, text="Loading...")
        self.frame.pack(fill="both", expand=True)

        self.bind("<KeyPress-space>", self.freeze_frame)

        self.video_stream()
    
    def freeze_frame(self, event):
        pass
    
    def video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = Image.fromarray(frame)
            
            image = customtkinter.CTkImage(dark_image=frame, size=(frame.width, frame.height))
            
            self.frame.image = image
            self.frame.configure(image=image, text="")
        else:
            self.frame.configure(text="No frame")
        
        self.frame.pack(fill="both", expand=True)
        self.after(TIK, self.video_stream)
    
    def clean_up(self):
        self.cap.release()
        cv2.destroyAllWindows()
    

class AddPosition(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x800")
        self.title("Add position")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(
            self,
            text="Give a label to the position (if blank the position will have index as label)"
        )
        self.label.grid(row=0, column=0, sticky="ew")

        self.canvas = OpenCVFrame(self)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.entry = customtkinter.CTkEntry(self)
        self.entry.grid(row=2, column=0, sticky="ew")

        self.button = customtkinter.CTkButton(
            self, 
            text="Save position", 
            command=self.save_position
        )
        self.button.grid(row=3, column=0, sticky="ew")

    def save_position(self): # TODO: implement save_position method
        pass

    def destroy(self): # TODO: implement destroy method
        super().destroy()
        self.canvas.clean_up()



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry(str(HEIGHT) + "x" + str(WIDTH))
        self.title("Dataset Generator Helper")
        self.minsize(WIDTH, HEIGHT)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="List of position")
        self.label.grid(row=0, column=0, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(
            master=self, width=400, corner_radius=0)
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Some example text!\n" * 50)

        self.button = customtkinter.CTkButton(
            self, text="Capture position", command=self.capture_position)
        self.button.grid(row=2, column=0, sticky="ew")

        self.capture_window = None

    def print_positions(self):
        i = 0
        for position in positions:
            i += 1
            self.textbox.insert("end", str(i) + ". " + position + "\n")

    def capture_position(self):
        if self.capture_window is None or not self.capture_window.winfo_exists():
            # create window if its None or destroyed
            self.capture_window = AddPosition(self)
        self.capture_window.focus()  # if window exists focus it


app = App()
app.mainloop()

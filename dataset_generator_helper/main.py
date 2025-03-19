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
import mediapipe as mp
import time

positions = []

WIDTH = 500
HEIGHT = 400

VIDEO_CAPTURE = 1  # 0 for default or back camera, 1 for external or front camera

FPS = 30
TIK = 1000 // FPS

class OpenCVFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # FPS metrics
        self.ptime = 0
        self.ctime = 0

        self.fps = 0

        self.fps_label = customtkinter.CTkLabel(self, text="FPS: "+str(self.fps))
        self.fps_label.pack(fill="both", expand=True)

        # Video capture
        self.cap = cv2.VideoCapture(VIDEO_CAPTURE)

        self.frame = customtkinter.CTkLabel(self, text="Loading...")
        self.frame.pack(fill="both", expand=True)

        # Video controls
        self.paused = False
        self.pause_btn = customtkinter.CTkButton(self, text="Pause", command=self.freeze_frame)
        self.pause_btn.pack(fill="both", expand=True)

        self.take_snapshot_btn = customtkinter.CTkButton(self, text="Take snapshot", command=self.take_snapshot)
        self.take_snapshot_btn.pack(fill="both", expand=True, pady=10)

        self.video_stream()
    
    def take_snapshot(self):
        self.freeze_frame()

        img = self.frame.image
        pos = self.actual_position

        if img is not None and pos is not None:
            positions.append(pos)
            print("Position saved")
            print(pos)
        else:
            print("No position to save")
    
    def freeze_frame(self):
        self.paused = not self.paused
        print("Paused" if self.paused else "Playing")

        if self._job is not None:
            self.after_cancel(self._job)
        self._job = None

        if not self.paused:
            self.video_stream()
    
    def video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = self.mediapipe_process(frame)

            frame = Image.fromarray(frame)
            
            image = customtkinter.CTkImage(dark_image=frame, size=(frame.width, frame.height))
            
            self.frame.image = image
            self.frame.configure(image=image, text="")
        else:
            self.frame.configure(text="No frame")
        
        self.frame.pack(fill="both", expand=True)

        self.ctime = time.time()
        self.fps = 1 / (self.ctime - self.ptime)
        self.ptime = self.ctime

        self.fps_label.configure(text="FPS: "+str(int(self.fps)))

        self._job = self.after(TIK, self.video_stream)
    
    def mediapipe_init(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
    
    def mediapipe_process(self, frame):
        if not hasattr(self, "hands"):
            self.mediapipe_init()
        
        self.actual_position = None
        self.frame.image = None
        
        frame = cv2.flip(frame, 1)
        results = self.hands.process(frame)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    if id == 4 :
                        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    if id == 8 :
                        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    if id == 12 :
                        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    if id == 16 :
                        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    if id == 20 :
                        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
            self.actual_position = results.multi_hand_landmarks
        
        return frame
    
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

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

        self.video_stream()
    
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
    
    def get_current_position(self):
        pos = [self.frame.image, self.actual_position]
        if pos[0] is not None and pos[1] is not None:
            return pos
        return None
    
    def clean_up(self):
        self.cap.release()
        cv2.destroyAllWindows()    

class AddPosition(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.canvas = OpenCVFrame(master=self)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.take_snapshot_btn = customtkinter.CTkButton(self, text="Take snapshot", command=self.take_snapshot)
        self.take_snapshot_btn.grid(row=3, column=0, sticky="nsew")

    def take_snapshot(self):
        self.canvas.freeze_frame()
        current_pos = self.canvas.get_current_position()

        if current_pos is not None:
            img, pos = current_pos
            data_item = {
                "label": str(len(positions)+1),
                "image": img,
                "position": pos
            }

            positions.append(data_item)
            print("Position saved")
            print(data_item)
        else:
            print("No position to save")

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

        self.capture_frame = AddPosition(master=self)
        self.capture_frame.grid(row=1, column=1, sticky="nsew")

app = App()
app.mainloop()

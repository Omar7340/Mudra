import customtkinter as ctk
import cv2
import mediapipe as mp
from PIL import Image
import time
from configs import *

class OpenCVFrame(ctk.CTkFrame):
    def __init__(self, master, video_capture=VIDEO_CAPTURE, **kwargs):
        super().__init__(master, **kwargs)

        # FPS metrics
        self.ptime = 0
        self.ctime = 0

        self.fps = 0

        self.fps_label = ctk.CTkLabel(self, text="FPS: "+str(self.fps))
        self.fps_label.pack(fill="both", expand=True)

        # Video capture
        self.cap = cv2.VideoCapture(video_capture)

        self.frame = ctk.CTkLabel(self, text="Loading...")
        self.frame.pack(fill="both", expand=True)

        self.video_stream()
    
    def video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ## save image before processing
            self.frame.image = Image.fromarray(frame)

            frame = self.mediapipe_process(frame)
            
            image = ctk.CTkImage(dark_image=frame, size=(frame.width, frame.height))
            
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
        
        frame = cv2.flip(frame, 1)
        results = self.hands.process(frame)

        h, w, c = frame.shape

        # init at the extreme point
        x_left = w
        y_top = h

        x_right = 0 
        y_bottom = 0

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    # Check if this landmark is the closest to the limit of the frame
                    # needed for cropping the frame on the hand
                    if cx < x_left:
                        x_left = cx
                    
                    if cx > x_right:
                        x_right = cx
                    
                    if cy < y_top:
                        y_top = cy
                    
                    if cy > y_bottom:
                        y_bottom = cy
                    
                    # Draw landmarks

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
        
        ## Crop frame
        frame = Image.fromarray(frame)

        x_right += MARGIN_CROP
        y_bottom += MARGIN_CROP

        x_left -= MARGIN_CROP
        y_top -= MARGIN_CROP
        
        if x_left < x_right and y_top < y_bottom:
            frame = frame.crop((x_left, y_top, x_right, y_bottom))
        
        return frame
    
    def get_current_position(self):
        pos = {
            "img": self.frame.image,
            "pos": self.actual_position
        }

        if pos["img"] is None or pos["pos"] is None:
            return None

        return pos
    
    def clean_up(self):
        self.cap.release()
        cv2.destroyAllWindows()    

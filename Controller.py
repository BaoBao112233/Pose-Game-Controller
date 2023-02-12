import cv2
import pyautogui as pg
from Pose_Controller import Pose_Controller as PC

class Game:
    def __init__ (self):
        self.pose = PC()
        self.game_started = False
        self.x_position = 1 # 0: Left, 1: Center, 2: Right
        self.y_position = 1 # 0: Down, 1: Stand. 2: Jump
        self.clap_duration = 0 # Number frame of clap

    def move_LRC(self, LRC):
        if LRC == "L":
            for _ in range(self.x_position):
                pg.press("left")
            
            self.x_position = 0
        elif LRC == "R":
            for _ in range(2,self.x_position,-1):
                pg.press("right")
            
            self.x_position = 2
        else:
            if self.x_position == 0:
                pg.press("right")
            elif self.x_position == 2:
                pg.press("left")
            
            self.x_position == 1
        
        return
    
    def move_UDC(self, UDC):
        if UDC == "U" and self.y_position == 1:
            pg.press("up")
            self.y_position = 0
        elif UDC == "D" and self.y_position == 1:
            pg.press("down")
            self.y_position = 2
        elif UDC == "C" and  self.y_position != 1:
             self.y_position == 1
        
        return
    
    def play(self):

        # Camera
        cap = cv2.VideoCapture(0)

        cap.set(3,1280)
        cap.set(4,960)

        while True:
            ret, img = cap.read()

            if ret:
                cv2.imshow("Game", img)
            
            if cv2.waitKey(1) == ord("q"):
                break

        
        cap.release()
        cap.destroyAllWindows()
    

game = Game().play()
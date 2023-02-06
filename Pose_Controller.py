import mediapipe as mp
import cv2 

class Pose_Controller:
    def __init__(self):
        self.mp_pose = mp.solotions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        # Lưu lại vị trí của người dùng khi vỗ tay để bắt đầu game
        self.shouder_line_y = 0

    def detectPose(self, img):
        # Chuyển ảnh sang RGB
        imgRGB = cv2.cvt(img,cv2.COLER_BGR2RGB)

        # Lấy kết quả đầu ra qua model
        results = self.pose.process(imgRGB)
        
        # Kiểm tra
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(img, landmark_list = results.pose_landmarks, connections= self.pose.POSE_CONNECTIONS,
                                            landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,255,255),thickness=3,circle_radius=3)
                                            connection_drawing_spec = self.mp_drawing.DrawingSpec(color))
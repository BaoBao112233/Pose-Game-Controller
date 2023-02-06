import mediapipe as mp
import cv2 

class Pose_Controller:
    def __init__(self):
        self.mp_pose = mp.solotions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        # Lưu lại vị trí của người dùng khi vỗ tay để bắt đầu game
        self.shoulder_line_y = 0

    def detectPose(self, img):
        # Chuyển ảnh sang RGB
        imgRGB = cv2.cvt(img,cv2.COLER_BGR2RGB)

        # Lấy kết quả đầu ra qua model
        results = self.pose.process(imgRGB)
        
        # Kiểm tra
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(img, landmark_list = results.pose_landmarks, connections= self.pose.POSE_CONNECTIONS,
                                            landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(255,255,255), thickness=3, circle_radius=3)
                                            connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(0,0,255), thickness=2))
        
        return img, results
    

    def checkPose_LRC(self, img, results):

        # Lấy kích thước của ảnh
        img_height, img_width, _ = img.shape

        img_mid_width = img_wigth//2

        leftShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * img_width)
        rightShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * img_width)

        if leftShoulder_x < img_mid_width and rightShoulder_x < img_mid_width:
            LRC = "L"
        elif leftShoulder_x > img_mid_width and rightShoulder_x > img_mid_width:
            LRC = "R"
        else:
            LRC = "C"
        
        # Vẽ thêm chữ LRC
        cv2.putText(img, LRC, (5, img_height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),3)
        cv2.line(img,(img_mid_width, 0), (img_mid_width, img_height), (255,255,255),2)

        return LRC, img


    def checkPose_UDC(self, img, results):

        # Lấy kích thước của ảnh
        img_height, img_width, _ = img.shape

        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * img_height)
        rightShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * img_height)

        centerShoulder_y = abs(leftShoulder_y + rightShoulder_y)//2

        jump_threshold = 30
        down_threshold = 15

        if centerShoulder > self.shoulder_line_y + down_threshold:
            UDC = "D"
        elif centerShoulder < self.shoulder_line_y - jump_threshold:
            UDC = "U"
        else:
            UDC = "C"
        
        # Vẽ thêm chữ UDC
        cv2.putText(img, UDC, (5. img_height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255),3)
        cv2.line(img,(0, self.shoulder_line_y), (img_width,self.shoulder_line_y), (255,255,255),2)

        return LRC, img
    
    def checkClap(self, img, results):
        
        # Lấy kích thước của ảnh
        img_height, img_width, _ = img.shape

        left_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * img_width,
                    results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * img_height)
        
        right_hand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * img_width,
                    results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * img_height)

        distance = int(math.hypot(left_hand[0] - right_hand[0], left_hand[1] - right_hand[1])) # 30:33


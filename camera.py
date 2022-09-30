import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
from yolov3_opencv.yolo_od_utils import yolo_object_detection

# set filenames for the model
coco_names_file = "yolov3files/coco.names"
yolov3_weight_file = "yolov3files/yolov3.weights"
yolov3_config_file = "yolov3files/yolov3.cfg"

# read coco object names
LABELS = open(coco_names_file).read().strip().split("\n")

# assign rondom colours to the corresponding class labels
np.random.seed(45)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# read YOLO network model
net = cv2.dnn.readNetFromDarknet(yolov3_config_file, yolov3_weight_file)


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        cv2.flip(frame, 1, frame)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        # frame = yolo_object_detection(frame, net, 0.5, 0.5, LABELS, COLORS)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def infer_single_img(self, filepath):
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        img = yolo_object_detection(img, net, 0.5, 0.5, LABELS, COLORS)

        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()



if __name__ == '__main__':
    print('aaa')

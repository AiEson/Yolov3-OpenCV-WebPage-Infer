import os

from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
from werkzeug.utils import secure_filename

app = Flask(__name__)
# -*-coding:utf-8-*-
import datetime
import random


class Pic_str:
    def create_uuid(self):  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')


def infer_single(camera: VideoCamera, filepath):
    frame = camera.infer_single_img(filepath)
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame +
           b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; '
                                                 'boundary=frame')


basedir = './upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename))

        return Response(infer_single(VideoCamera(), os.path.join(file_dir, new_filename)), mimetype='multipart/x-mixed-replace; '
                                                 'boundary=frame')
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

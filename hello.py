from aip import AipSpeech
import face_recognition
import cv2,random
import os,time
from playsound import playsound

""" 百度语音合成信息 """
APP_ID = '21418394'
API_KEY = 'dKQTAtAHrf2w12FY3uRdbn17'
SECRET_KEY = 't9yZYlobnnFh3usAcUo8QiOgBR9wS9K6'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# https://ai.baidu.com/ai-doc/SPEECH/Gk4nlz8tc
def say_hello(name):
    sentence=[
        "{},{},您来了".format(name,name),
        "{}，欢迎您".format(name),
        "{}，你好可爱吆~".format(name),
        "{}，你也太帅了吧".format(name),
        "{},{},{},{},{}".format(name,name,name,name,name)
    ]
    readers=[0,1,3,4]

    words = random.choice(sentence)
    reader = random.choice(readers)

    result  = client.synthesis(words, 'zh', 1, {
        'vol': 10,
        'per': reader
    })
    print("调用百度合成完毕，长度：",len(result))

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audios/output.mp3', 'wb') as f:
            f.write(result)
        playsound('audios/output.mp3')


def facedb_load(facedb_path):
    # 存储知道人名列表
    known_names = []
    # 存储知道的特征值
    known_encodings = []
    for image_name in os.listdir(facedb_path):
        load_image = face_recognition.load_image_file(os.path.join(facedb_path, image_name))  # 加载图片
        image_face_encoding = face_recognition.face_encodings(load_image)[0]  # 获得128维特征值
        known_names.append(image_name.split(".")[0])
        print("加入人脸库：", image_name.split(".")[0])
        known_encodings.append(image_face_encoding)
    return known_names, known_encodings


def face_rec(known_names, known_encodings):
    # 打开摄像头，0表示内置摄像头
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        print("读取摄像头")
        # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)  # 获得所有人脸位置
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # 获得人脸特征值
        face_names = []  # 存储出现在画面中人脸的名字
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            print("识别完毕")
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                print("识别出：",name)
                face_names.append(name)
            else:
                print("不认识这个人")

        for name in face_names:
            print("你是:",name)
            say_hello(name)
            #playsound(os.path.join("audios","{}.mp3".format(name)))

        time.sleep(5)


    video_capture.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    known_names, known_encodings = facedb_load("./facedb")
    face_rec(known_names, known_encodings)
    # say_hello()
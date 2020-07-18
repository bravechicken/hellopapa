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
        "{}大魔王,我最服您，最服您！".format(name),
        "{}，你是猴子请来的救兵么".format(name),
        "黑猫警长，你休要猖狂，我找{}吃猫鼠去".format(name),
        "爷爷,爷爷,葫芦娃的死敌{}来了".format(name),
        "{},酶惹佛死位置有".format(name),
        "{}，我的儿，快快交出唐僧来！".format(name),
        "{},海谁课亮课亮了".format(name),
        "为了防止世界被破坏，为了保护世界的和平，贯彻爱与真实的邪恶，可爱又迷人的反派角色，武藏,小次郎,和{}".format(name, name),
        "{},{},您来了，您吃点啥？好嘞！二两烧酒，一斤牛肉，得嘞！您晴好吧~".format(name,name),
        "累了，累了，{}，请快点毁灭地球吧".format(name),
        "{}，欢迎你，有梦想谁都了不起，有勇气就会有奇迹".format(name),
        "哆啦A梦，{}又欺负我了，快快救我，呜呜呜呜呜呜".format(name),
        "我是海贼王，我是{}，不打败你，我就什么也守护不了！".format(name),
        "就算颠覆整个宇宙，我也要把{}找回来".format(name),
        "不相信{}的人，连努力的价值都没有".format(name),
        "我是大力{}，我喜欢吃菠菜，因此我力大无比".format(name),
        "{}有水样干净透明的气质，神带给大家是永远的执着感动，对自己的梦想永不言弃".format(name),
        "汽车人，发动引擎，变形出发！kikikuku！{}们，撤退，快撤退！".format(name),
        "在那山的那边海的那边有一群蓝{}，它们活泼又聪明，它们调皮又伶俐".format(name),
        "{} will be back！我{} 又回来了！".format(name,name),
        "赐予我力量吧！我是{}".format(name),
        "{}，{},你的鼻子为什么那么长".format(name,name),
        "把你们的力量结合起来,就是{}，地球超人".format(name),
        "啊，漂亮姐姐！ 您好，我叫野原新之{}，今年5岁，最喜欢的内裤是动感超人的喔".format(name),
        "西米够 米够米够米够 变~~，变成{}".format(name),
        "我是个大盗贼{}，什么也不怕".format(name),
        "{}是爱与正义的化身 {}要替天行道，警恶惩奸".format(name,name),
        "是我,是我，我是{}，我要代表月亮惩罚你".format(name),
        "麻烦{}，来碗鱼丸粗面。对不起，木有鱼丸~ 木有粗面~".format(name),
        "{}，燃烧吧！燃烧你的小宇宙".format(name),
        "{}，为师错怪你了".format(name),
        "野爷~野爷~~野爷~~野爷~~，我是樱桃小{}".format(name),
        "妖精，还我爷爷，还我{}".format(name),
        "滨不露邦不露帮不啃，我{}".format(name),
        "舒克舒克舒克舒克舒克舒克，开飞机滴舒克！{},{},{},{},{},{},{},开坦克滴{}".format(name,name,name,name,name,name,name,name,),
        "我是要成为海贼王的男人,{}".format(name),
        "{},这个鱼盆是我们滴~ 不是你们滴~".format(name),
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
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
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
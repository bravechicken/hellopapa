# hellopapa - 人脸识别爸爸妈妈

## 运行前环境准备

运行环境：python3

安装需要的包：pip install -r requirements.txt

## 运行前数据准备

把需要识别的脸，放到facedb目录中，名字为这个人的中文名字.jpg。

一定要使用中文名字，这个名字会被朗诵出来。

图片不一定是jpg，也可以是png，jepg，bmp等图片后缀。

## 如何运行

bin/run.sh

运行后，摄像头会自动打开，每隔3秒，就会喊出被识别出来的对象的名字。
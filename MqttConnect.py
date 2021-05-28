import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import MyCamera
from threading import Thread
from pir import Pir
import base64
from time import sleep
import datetime


class MyMqtt():
    thread1 = None
    thread2 = None

    def __init__(self, topic, value):
        super().__init__()
        client = mqtt.Client()
        self.camera = MyCamera.MyCamera()
        client.connect("192.168.0.55", 1883, 60)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        self.pir = Pir()
        self.pir.start()
        MyMqtt.thread1 = Thread(target=self.videostreaming)
        MyMqtt.thread1.start()
        print('프레임 생성 스레드 시작')
        MyMqtt.thread2 = Thread(target=self.takepicture)
        MyMqtt.thread2.start()
        print('jpg 파일 생성 스레드 시작')
        self.frame = None
        client.loop_forever()

    def videostreaming(self):
        while True:
            self.frame = self.camera.getStreaming()


    def takepicture(self):
        while True:
            now = datetime.datetime.now()
            now = str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
            if self.pir.value == 'on':
                print('jpg 파일 생성 시작')
                # 파일저장
                filename = '%s.jpg' % now
                if self.frame != None:
                    f = open('/home/pi/Pictures/' + filename, "wb")
                    f.write(self.frame)
                    f.close()
                time.sleep(2)
                print(filename+'파일 생성 완료')
                data = str([self.frame,filename])
                publish.single("mydata/whoareyou/getimage", data, hostname="192.168.0.55")
                print(filename + '파일 publish 완료')
        
    def on_connect(self, client, userdata, flags, rc):
            print("connect.." + str(rc))
            if rc == 0:
                client.subscribe("sensor")
            else:
                print("연결실패")

    def on_message(self, client, userdata, msg):
        myval = msg.payload.decode("utf-8")
        print(myval)
        print(msg.topic + "----" + str(myval))
        if myval == "start":
            print('클라우드에 비디오 스트리밍 시작')
            while True:
                publish.single("web", self.frame, hostname="192.168.0.55")
        else:
            pass





if __name__ == "__main__":
    try:
        mymqtt = MyMqtt("sensor", "test")

    except KeyboardInterrupt:
        print("종료")

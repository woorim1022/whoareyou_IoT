import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import MyCamera
from threading import Thread
from pir import Pir
from mpu6050_i2c import mpu
from pressure import Pressure
import base64
from time import sleep
import datetime
from pyfirmata import Arduino, util
import msadb


class MyMqtt():
    thread1 = None
    thread2 = None
    thread3 = None
    thread4 = None

    pir = None

    def __init__(self, topic, value):
        super().__init__()
        client = mqtt.Client()
        self.host = "192.168.0.17"
        
        self.camera = MyCamera.MyCamera()
        client.connect(self.host, 1883, 60)
        
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        self.pir = Pir()
        self.pir.start()
        self.pressure = Pressure()
        self.pressure.start()
        self.mpu = mpu()
        self.mpu.start()

        self.frame = None

        self.flag_x = 0
        self.flag_y = 0
        self.flag_z = 0

        self.board = Arduino('/dev/ttyACM0')
        self.pin10 = self.board.get_pin('d:10:p')
        self.pin11 = self.board.get_pin('d:11:p')
        
        MyMqtt.thread1 = Thread(target=self.videostreaming)
        MyMqtt.thread1.start()
        print('프레임 생성 스레드 시작')
        
        MyMqtt.thread2 = Thread(target=self.takepicture)
        MyMqtt.thread2.start()
        print('프레임 jpg 파일로 저장하는 스레드 시작')

        MyMqtt.thread3 = Thread(target=self.keypad_doorhandle)
        MyMqtt.thread3.start()
        print('압력센서, 자이로센서 값 받는 스레드 시작')

        MyMqtt.thread4 = Thread(target=self.led_light)
        MyMqtt.thread4.start()
        print('조명 제어하는 스레드 시작')


        client.loop_forever()

    def led_light(self):
        while True:
            #print('now hour : '+ str(datetime.datetime.now().hour))
            #print('self.pir.value : '+ self.pir.value)
            if datetime.datetime.now().hour > 11 and MyMqtt.pir == 'on':
                print('light on')
                self.board.digital[13].write(1)
                self.board.digital[12].write(1)
                self.pin10.write(0.6)
                self.pin11.write(0.6)
                time.sleep(10)
            else:
                #print('light off')
                self.board.digital[13].write(0)
                self.board.digital[12].write(0)
                self.pin10.write(0.6)
                self.pin11.write(0.6)
                time.sleep(1)



    def keypad_doorhandle(self):
        while True:
            if self.pressure.value == 'pressure detected':
                print('키패드값 publish 완료')
                now = datetime.datetime.now()
                now = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)
                data = str(['keypad touched', now])
                publish.single("mydata/whoareyou/getkeypad", data, hostname=self.host)

            if self.mpu.value:
                if abs(self.mpu.value[0]-self.flag_x) > 50.0 or abs(self.mpu.value[1]-self.flag_y) > 50.0 or abs(self.mpu.value[2]-self.flag_z) > 50.0:
                    self.flag_x = self.mpu.value[0]
                    self.flag_y = self.mpu.value[1]
                    self.flag_z = self.mpu.value[2]
                    print('문고리 x축 기울기'+ str(self.flag_x))
                    print('문고리 y축 기울기'+ str(self.flag_y))
                    print('문고리 z축 기울기'+ str(self.flag_z))
                    print('문고리값 publish 완료')
                    now = datetime.datetime.now()
                    now = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second)
                    data = str(['doorhandle touched', now])
                    publish.single("mydata/whoareyou/getdoorhandle", data, hostname=self.host)


    def videostreaming(self):
        while True:
            self.frame = self.camera.getStreaming()

    def takepicture(self):
        while True:
            now = datetime.datetime.now()
            now = str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
            if self.pir.value == 'on':
                # pir이 on이 감지되는 지속시간을 구해서 pub하자0
                MyMqtt.pir = self.pir.value
                #print('jpg 파일 생성 시작')
                # 파일저장
                filename = '%s.jpg' % now
                if self.frame != None:
                    f = open('/home/pi/Pictures/' + filename, "wb")
                    f.write(self.frame)
                    f.close()
                time.sleep(2)
                #print(filename+'파일 생성 완료')
                data = str([self.frame,filename])
                publish.single("mydata/whoareyou/getimage", data, hostname=self.host)
                print(filename + '파일 publish 완료')
                MyMqtt.pir = None
        
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
                publish.single("web", self.frame, hostname=self.host)
        else:
            pass





if __name__ == "__main__":
    try:
        mymqtt = MyMqtt("sensor", "test")

    except KeyboardInterrupt:
        print("종료")

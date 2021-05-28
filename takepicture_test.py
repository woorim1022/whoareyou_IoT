import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import MyCamera
import base64



camera = MyCamera.MyCamera()




if __name__ == "__main__":
    try:
      while True:
        frame = camera.getimagefile()
        print(frame)
        #publish.single("web", frame, hostname="192.168.0.55")



    except KeyboardInterrupt:
        print("종료")

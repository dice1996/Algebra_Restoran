from threading import Thread
import paho.mqtt.client as mqtt
from time import sleep as delay
from collections import deque


class MqttClient(Thread):
    def __init__(self, host, port, topic):
        super(MqttClient, self).__init__()
        self.mqtt = mqtt.Client()
        self.host = host
        self.port = port
        self.topic = topic
        self.queue = deque()

    def run(self):
        self.mqtt.on_connect = self.on_connect
        self.mqtt_on_disconnect = self.on_disconnect
        self.mqtt.on_subscribe = self.on_subscribe
        self.mqtt.on_message = self.on_message
        self.mqtt.connect(self.host, self.port)
        self.mqtt.loop_forever()

    def on_connect(self, mqtt_client, userdata, flags, rc):
        print("Connected to mqtt server!")
        self.mqtt.subscribe(topic = self.topic, qos = 0)

    def on_disconnect(self, mqtt_client, userdata, rc):
        print("Disconnected from mqtt server!")

    def on_subscribe(self, mqtt_client, userdata, mid, granted_qos):
        print("Successfully subscribed to topic!")

    def on_message(self, mqtt_client, userdata, msg):
        self.queue.append(f"{msg.topic};{msg.payload.decode('utf-8')}")
        #print(msg.topic + " - " + msg.payload.decode('utf-8'))

    def publish(self, topic, msg):
        print("Publishing... topic: " + topic +": "+msg)
        self.mqtt.publish(topic, msg, 0, False)

    def get_from_queue(self):
        if len(self.queue) != 0:
            return self.queue.popleft()
        else:
            return None
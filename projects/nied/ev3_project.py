#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time
import math


class MyDelegate(object):

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print("My project")
    print("--------------------------------------------")
    ev3.Sound.speak("My project").wait()

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    mqtt_client = com.MqttClient(MyDelegate)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


main()

#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time
import math


def main():
    print("--------------------------------------------")
    print("My project")
    print("--------------------------------------------")
    ev3.Sound.speak("Ready").wait()

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    start = None
    pixy = ["SIG1", "SIG2", "SIG3", "SIG4"]

# ----------------------------------------------------------------------------------------------------------------------
    while robot.running is True:

        if robot.active is True:
            for _ in range(sides):
                robot.forward(400,400)
                if robot.color_sensor.reflected_light_intensity > 10:
                    robot.stop()
                robot.turn_degrees(turn_amount, speed_deg_per_second)
            robot.pixy.mode = "SIG3"
            # if robot.pixy.value(1) < 165:
            #     robot.left(robot.SLOW_SPEED, robot.SLOW_SPEED)
            # elif robot.pixy.value(1) > 185:
            #     robot.right(robot.SLOW_SPEED, robot.SLOW_SPEED)
            # if 165 <= robot.pixy.value(1) <= 185:
            #     robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            #     robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            #     if 100 > robot.ir_sensor.proximity:
            #         if start is None:
            #             start = robot.ir_sensor.proximity
            #         robot.forward(300, 300)
            #         if robot.ir_sensor.proximity <= 1.5 or robot.ir_sensor.proximity == 100:
            #             robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            #             robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            #             robot.arm_up()
            #             if robot.ir_sensor.proximity <= 4:
            #                 robot.turn_degrees(200, robot.MAX_SPEED)
            #                 robot.drive_inches(start/2.7, 400)
            #                 ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
            #                 robot.active = False
            #             else:
            #                 robot.arm_down()
            # time.sleep(0.25)

        time.sleep(0.1)


main()

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
    pixy = ["SIG1", "SIG2", "SIG3", "SIG4"]

# ----------------------------------------------------------------------------------------------------------------------
    while robot.running is True:

        while robot.active is True:
            # robot.arm_calibration()
            for k in range(robot.sides):
                # distance = None
                robot.pixy.mode = pixy[k]
                search = True
                while search is True:
                    robot.forward(300, 300)
                    if robot.color_sensor.reflected_light_intensity > 15:
                        search = False
                robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                robot.drive_inches(-2, robot.SLOW_SPEED)
                robot.turn_degrees(195, 200)
                ready = True
                while ready is True:
                    if robot.pixy.value(1) < 165:
                        # robot.special_turn_degrees(5, 200)
                        # robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        # robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        robot.left(robot.SLOW_SPEED, robot.SLOW_SPEED)

                    elif robot.pixy.value(1) > 185:
                        # robot.special_turn_degrees(-5, 200)
                        # robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        # robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        robot.right(robot.SLOW_SPEED, robot.SLOW_SPEED)
                    #     ------------------------------------------------------------------
                    elif 165 <= robot.pixy.value(1) <= 185:
                        robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                        if 100 > robot.ir_sensor.proximity:
                            # if distance is None:
                            #     distance = robot.ir_sensor.proximity
                            robot.forward(300, 300)
                            if robot.ir_sensor.proximity <= 1.5 or robot.ir_sensor.proximity == 100:
                                robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                                robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
                                robot.arm_up()
                                if robot.ir_sensor.proximity <= 4 or robot.ir_sensor.proximity == 100:
                                    robot.turn_degrees(195, robot.MAX_SPEED)
                                    search_line = True
                                    while search_line is True:
                                        robot.forward(300, 300)
                                        if robot.color_sensor.reflected_light_intensity > 15:
                                            search_line = False
                                    robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                                    robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                                    # robot.drive_inches(distance * 0.27559, 300)
                                    robot.arm_down()
                                    robot.drive_inches(-3, robot.SLOW_SPEED)
                                    # robot.turn_degrees(-robot.degrees_turned, 200)
                                    # robot.degrees_turned = 0
                                    robot.turn_degrees(199, 200)
                                    robot.turn_degrees(-((360 / robot.sides)/2), 200)
                                    ready = False
                                else:
                                    robot.arm_down()
                    time.sleep(0.25)
            print('finished')
            ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
            ev3.Sound.speak("Construction Complete")
            robot.active = False

    time.sleep(0.1)


main()

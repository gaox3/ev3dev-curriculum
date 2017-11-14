import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    ev3.Sound.speak("Avoid collision system activated").wait()
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    assert left_motor.connected
    assert right_motor.connected

    # Robot
    robot = robo.Snatch3r()
    # Remote control
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    while True:
        if robot.ir_sensor.proximity < 10:
            robot.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            robot.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
            time.sleep(1)
            robot.turn_degrees(90, 200)
        else:
            left_motor.run_forever(speed_sp=400)
            right_motor.run_forever(speed_sp=400)


def drive_forward(left_motor, right_motor, time_s):
    left_motor.run_forever(speed_sp=400)
    right_motor.run_forever(speed_sp=400)
    time.sleep(time_s)
    left_motor.stop(stop_action="brake")
    right_motor.stop(stop_action="brake")


main()

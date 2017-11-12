import ev3dev.ev3 as ev3
import time


def main():
    ev3.Sound.speak("Avoid collision system activated").wait()
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    assert left_motor.connected
    assert right_motor.connected


def drive_forward(left_motor, right_motor, time_s):
    left_motor.run_forever(speed_sp=400)
    right_motor.run_forever(speed_sp=400)
    time.sleep(time_s)
    left_motor.stop(stop_action="brake")
    right_motor.stop(stop_action="brake")

while True:
    
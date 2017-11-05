"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""
import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.arm_motor.connected
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        assert self.left_motor.connected
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert self.right_motor.connected
        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor
        self.MAX_SPEED = 900
        self.running = True
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

    # ---MOTORS------------------------------------------------------------------------
    def drive_inches(self, position, speed):
        self.left_motor.run_to_rel_pos(speed_sp=speed, position_sp=position * 90,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(speed_sp=speed, position_sp=position * 90,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        if degrees_to_turn > 0:
            self.left_motor.run_to_rel_pos(speed_sp=(-turn_speed_sp), position_sp=-5.1*degrees_to_turn,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=5.1*degrees_to_turn,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        else:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=5.1*degrees_to_turn,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=(-turn_speed_sp), position_sp=-5.1*degrees_to_turn,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def stop(self):
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def forward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def back(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def left(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def right(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    # ---DIGITAL INPUTS----------------------------------------------------------------
    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-360 * arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def shutdown(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_COAST)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()
        self.running = False

    # ---MQTT----------------------------------------------------------------------------
    def loop_forever(self):
        self.arm_calibration()
        while self.running:
            time.sleep(0.1)

    # ---ANALOG SENSORS------------------------------------------------------------------
    def seek_beacon(self):
        rc1 = ev3.RemoteControl(channel=1)
        assert rc1.connected
        beacon_seeker = ev3.BeaconSeeker
        forward_speed = 300
        turn_speed = 100
        slow_turn_speed = 30
        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.right(slow_turn_speed, slow_turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 0:
                        self.forward(forward_speed, forward_speed)
                    elif current_distance == 0:
                        self.stop()
                        return True
                elif 2 <= math.fabs(current_heading) <= 10:
                    if current_heading < 0:
                        self.left(turn_speed, turn_speed)
                    elif current_heading > 0:
                        self.right(turn_speed, turn_speed)
                elif math.fabs(current_heading) > 10:
                    self.right(slow_turn_speed, slow_turn_speed)
                    print("Heading too far off")
            rc1.process()
            time.sleep(0.2)
        print("Abandon ship!")
        self.stop()
        return False



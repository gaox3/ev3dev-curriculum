
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegatePC(object):
    def __init__(self):
        self.running = True


def main():
    root = tkinter.Tk()
    root.title("MQTT Remote")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    my_delegate = MyDelegatePC()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    start_button = ttk.Button(main_frame, text="Go!")
    start_button.grid(row=1, column=1)
    start_button['command'] = lambda: start(mqtt_client)
    root.bind('<space>', lambda event: start(mqtt_client))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=1, column=3)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))
    root.mainloop()


def start(mqtt_client):
    print("Go!")
    mqtt_client.send_message("start")


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


main()

__author__ = 'rod!'

import sys
import serial
from pythonosc import osc_message_builder
from pythonosc import udp_client
import Filters
import time


def main(argv):
    winSize1 = 4
    winSize2 = 24
    winSize3 = 4
    winSize4 = 3
    ser = serial.Serial("/dev/cu.usbmodemFA131")  # Mac OS X example
    ser.flushInput()
    # 3 windows on each sensor stream.
    win1 = Filters.Window(winSize1)
    win2 = Filters.Window(winSize2)
    win3 = Filters.Window(winSize3)
    # this stream is a window of all three sensor streams together at once.
    win4 = Filters.Window(winSize4)

    fundamentalFrequency = 220

    while ser.readline():
        # clean arduino formatting.
        tuple = ser.readline().decode("ascii")
        tuple = tuple[:-2]  # remove the /r/n from the tuple
        tuple = tuple.split(",")
        # make sure we have the right types.
        sensor1 = int(tuple[0])
        sensor2 = int(tuple[1])
        sensor3 = int(tuple[2])

        # pipe tuples to window objects.
        win1.add(sensor1)
        win2.add(sensor2)
        win3.add(sensor3)

        win4.add(sensor1)
        win4.add(sensor2)
        win4.add(sensor3)
        control = 0.5
        #one window with gate and degree selection:
        if win1.count_window() == winSize1:
            # this "degree" takes the window input, maps it to appropriate values
            out = Filters.Mapper(win1.get()).map(0.0,1.0)
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_min()
            out = out*fundamentalFrequency
            if out:
                client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
                client.send_message('/synth1', [out,control])
            win1.clear()


        if win2.count_window() == winSize2:
            # this "degree" takes the window input, maps it to appropriate values
            out = Filters.Mapper(win2.get()).map(0.5, 1.5)
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_min()

            if out >200:
                client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
                client.send_message('/synth2', [out,control])
            win2.clear()
        if win3.count_window() == winSize3:
            # this "degree" takes the window input, maps it to appropriate values
            out = Filters.Mapper(win3.get()).map(1.0, 2.0)
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_min()
            out = out * 110

            if out < 170 :
                print("BOOSH")
                client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
                client.send_message('/synth3', [out,control])

            win3.clear()
        if win4.count_window() == winSize4:
            # this "degree" takes the window input, maps it to appropriate values
            out = Filters.ActionGate(win4.get()).gate(200)
            if out:
                client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
                client.send_message('/talk', [out, control])


            win4.clear()

if __name__ == "__main__":
    main(sys.argv)

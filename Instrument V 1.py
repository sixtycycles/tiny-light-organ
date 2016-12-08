
__author__ = 'rod!'

import sys
import serial
import collections
from pythonosc import osc_message_builder
from pythonosc import udp_client
import Filters
import math

def main(argv):

    winSize1, winSize2, winSize3 = 16,8,4
    ser = serial.Serial("/dev/cu.usbmodemFA131")  # Mac OS X example
    ser.flushInput()

    win1 = Filters.Window(winSize1)
    win2 = Filters.Window(winSize2)
    win3 = Filters.Window(winSize3)



    while ser.readline():
        #clean arduino formatting.
        tuple = ser.readline().decode("ascii")
        tuple = tuple[:-2]  # remove the /r/n from the tuple
        tuple = tuple.split(",")
        #make sure we have the right types.
        sensor1  = int(tuple[0])
        sensor2 = int(tuple[1])
        sensor3 = int(tuple[2])

        #pipe tuples to window objects.
        win1.add(sensor1)
        win2.add(sensor2)
        win3.add(sensor3)

        outStream = []



        #one window with gate and degree selection:
        if win1.count_window() == winSize1:

            #this "degree" takes the window input, maps it to appropriate values
            degree = (Filters.Mapper(win1.get()).map(0.0,1.0))
            #this takes the mapped window and returns the mean value.
            degree = Filters.Reducto(degree).reduce_mean()

            outStream.append(degree)
            win1.clear()

        if win2.count_window() == winSize2:
            # this "degree" takes the window input, maps it to appropriate values
            out = (Filters.Mapper(win2.get()).map(500.0, 10000.0))
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_max()
            outStream.append(out)
            win2.clear()

        if win3.count_window() == winSize3:
            # this "degree" takes the window input, maps it to appropriate values
            out = (Filters.Mapper(win3.get()).map(0.01, 1.0))
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_min()
            outStream.append(out)
            win3.clear()


        if outStream  :
            out = outStream
            print(out)
            client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
            client.send_message('/grains', out)
            outStream.clear()



if __name__ == "__main__":
    main(sys.argv)
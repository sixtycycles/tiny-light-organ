
__author__ = 'rod!'

import sys
import serial
import collections
from pythonosc import osc_message_builder
from pythonosc import udp_client
import Filters
import math

def main(argv):

    winSize1, winSize2, winSize3 = 2, 2, 2
    ser = serial.Serial("/dev/cu.usbmodemFA131")  # Mac OS X example
    ser.flushInput()

    win1 = Filters.Window(winSize1)
    win2 = Filters.Window(winSize2)
    win3 = Filters.Window(winSize3)

    noisereduction = Filters.Window(10)

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
        noisereduction.add([sensor1,sensor2,sensor3])
        outStream = {'freq': 1000 ,'filter': 1000, 'time':0.1,'position':0.0}

        #one window with gate and degree selection:
        if win1.count_window() == winSize1:

            #this "degree" takes the window input, maps it to appropriate values
            degree = (Filters.map_1_to_0(win1.get()).map())
            #this takes the mapped window and returns the mean value.
            degree = Filters.Reducto(degree).reduce_mean()

            outStream['time'] = degree
            win1.clear()

        if win2.count_window() == winSize2:
            filter = Filters.Reducto(win2.get()).reduce_mean()
            #divide by 500 to get values that the RQ parameter of the Equalizer can accept.
            outStream['filter'] = filter
            win2.clear()

        if win3.count_window() == winSize3:
            position = Filters.map_1_to_0(win3.get()).map()
            position = Filters.Reducto(position).reduce_mean()
            outStream['position'] = position
            win3.clear()
        #noise reduction takes a look at all values from all sensors and returns only the ones that are duplicated more than twice across all sensors.
        #this returns only the duplicated values, and so requires further processing as the size of the return is changeable.


        if outStream['time'] != 0.1 :
            dict = [outStream['time'], outStream['freq'],outStream['filter'],outStream['position']]
            print(dict)
            client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
            client.send_message('/synth2', dict)
            outStream.clear()
        #else:
            #print('stream')


if __name__ == "__main__":
    main(sys.argv)
__author__ = 'rod!'

import sys
import serial
from pythonosc import osc_message_builder
from pythonosc import udp_client
import Filters
import time


def main(argv):
    winSize1 = 12
    winSize2 = 12
    winSize3 = 12
    winSize4 = 33
    ser = serial.Serial("/dev/cu.usbmodemFA131")  # Mac OS X example
    ser.flushInput()
    # 3 windows on each sensor stream.
    win1 = Filters.Window(winSize1)
    win2 = Filters.Window(winSize2)
    win3 = Filters.Window(winSize3)
    # this stream is a window of all three sensor streams together at once.
    win4 = Filters.Window(winSize4)
    # this is the default output stream as a dictionary;


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
        # win4 takes a look at all values from all sensors and returns only the ones that are duplicated more than twice across all sensors.
        # this returns only the duplicated values, and so requires further processing as the size of the return is changeable. so in the event that the sensors return
        # [200,201,200] the stream will pass it through.
        win4.add(sensor1)
        win4.add(sensor2)
        win4.add(sensor3)
        outStream = []
        #one window with gate and degree selectiRon:
        if win1.count_window() == winSize1:

            # this "degree" takes the window input, maps it to appropriate values
            out = (Filters.Mapper(win1.get()).map(100,900))
            # this takes the mapped window and returns the mean value.
            out = Filters.Reducto(out).reduce_min()
            # set the key
            outStream.append(out)
            win1.clear()

        if win2.count_window() == winSize2:
            out = Filters.Reducto(win2.get()).reduce_mean()
            out = out*5
            outStream.append(out)
            win2.clear()

        #win3 returns the mean value from the window
        if win3.count_window() == winSize3:
            out = Filters.Mapper(win3.get()).map(0,1)
            out = Filters.Reducto(out).reduce_max()
            outStream.append(out*440)

            win3.clear()

        #win4  is a special case. it takes all values from all sensors and windows them.
        #it acts as a trigger event
        #
        if win4.count_window() == winSize4:
            out = Filters.ActionGate(win4.get()).gate(300)
            #if an event is created:
            #send special message for one shot sound.
            if out:
                client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
                client.send_message('/talk', [out])
                #this is a hack to keep this event from firing too many times after its initial occurance.

            win4.clear()

        while outStream:
            dict = outStream
            print(outStream)
            client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
            client.send_message('/synth', dict)
            #here clear is a built in method of dict. cool!
            outStream.clear()
            # print('stream')


if __name__ == "__main__":
    main(sys.argv)

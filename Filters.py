__author__ = 'Rod OConnor'

from numpy import interp
import math

#window holds values. should be transparrent how this works. everything is called in the main program to make it easy to trace actions.
class Window(object):
    def __init__(self, window_size):
        self.window_size = window_size
        self.clear()

    def add(self, tuple):
        self.window.append(tuple)
        if self.count_window() > self.window_size:
            self.window.pop(0)

    def get(self):
        return self.window

    def clear(self):
        self.window = []

    def count_window(self):
        return len(self.window)

#dont use this;
class OrderReduce(object):
    def __init__(self,list):
        self.list = list
        self.ordered = sorted(list)


    def getRange(self):
        max = self.ordered[len(self.list)-1]
        return max

#this class takes a window input and compares the elements for uniqueness.
# it then compares unique elements to determine the range in values.
class ActionGate(object):
    def __init__(self,window):
        self.window = window
        self.unique = []

        #SORTS THE WINDOW
    def do(self):
        for i in self.window:
            if i not in self.unique:
                self.unique.append(i)
        self.returnvals = sorted(self.unique)
        self.out = [self.returnvals[0],self.returnvals[len(self.returnvals)-1]]
        return self.out
    #RETURN DIFFERENCE IN WINDOW VALUES
    def getDiff(self):
        range = self.do()
        #subtract high val from low val return difference.
        self.out = range[1] - range[0]
        return self.out
    #IF GATE BIGgER THAN THIS
    def gate(self,threshold):
        self.threshold = threshold
        if self.getDiff() > self.threshold:
            #then return window
            return self.out


#maps window input to range set by arguments to make usable value ranges.
class Mapper(object):
    def __init__(self,window):
        self.window = window

    def map(self,minOut,maxOut):
        self.minOut = minOut
        self.maxOut = maxOut
        #the first array is the input range, this has to be scaled depending on how much light there is.
        #the second array is the output range, which can change depending on what you need it for.
        out = interp(self.window,[50.0,700.0],[minOut,maxOut])
        return out

#reduce class: methods for  extracting 1 tuple from
class Reducto(object):
    def __init__(self,window):
        self.window = window

    def reduce_mean(self):
        x = 0
        for i in self.window:
            x+=i
        return x/len(self.window)

    def reduce_min(self):
        return min(self.window)

    def reduce_max(self):
        return max(self.window)
    #this method returns the full window, so you will want to call it with another, like min or max. or just select an index.
    def floorIt(self):
        win = []
        for i in self.window:
            win.append(math.floor(self.window[i]))
        return win


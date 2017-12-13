##tiny-light-organ##
#rod oconnor for SIE558 final project#

This uses an arduino, python3 and supercollider.

The ```OSCreciever.scd``` file should be run in supercollider (https://supercollider.github.io/). The code from serial example should be burned into the Arduino (I use the Arduino IDE here:https://www.arduino.cc/en/Main/Software ).  

You can use the tutorial from Adafruit on photo-resistors to get an idea of how the circuits are setup.(basic basic example here: https://learn.adafruit.com/photocells/using-a-photocell) In this case I used three photo-resistors and they are on the digital pins that are spec'd in this ```.ino``` file.

The python code should be run in a python3 interpreter, and you will need to install numpy and python-osc <br>
 ``` pip install python-osc ```<br>
 ```pip install numpy```

 then you should be ready to go! i found that starting the python processor before supercollider caused issues, so play around with the order that you start things up in. Also, the code here has a lot of arbitrary values which i setup based on the light levels where i was running it, you may have to adjust some things.

 I will work on a proof of concept version, and also extending the SC side of things. I tried to keep most of the logic in the Python code, rather than on the arduino or in SC to make it easy to modify.

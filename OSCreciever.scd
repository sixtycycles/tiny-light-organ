// rod oconnor, for SIE558.

//boot the server:
s.boot;
//execute this block to get synths in memory:
(

SynthDef(\sines,{ |out =0 freq=440, filter = 5600,phase = 0.3,sustain =1 amp=0.3|
	var audio;
	audio = SinOsc.ar(freq/2,SinOsc.ar(phase,0,1),1);
	audio = Pan2.ar(RLPF.ar(audio,filter,1.23),0);
	audio = audio* EnvGen.ar(Env.sine,1, levelScale:amp,timeScale:sustain ,doneAction:2);
	OffsetOut.ar(out,audio);
}).store;

SynthDef(\square,{ |out =0 freq=440, mod = 220,sustain =1 amp=0.3|
	var audio;
	audio = LFPulse.ar(freq,0,0.5);
	audio = audio* EnvGen.ar(Env.sine,1, levelScale:amp,timeScale:sustain ,doneAction:2);
	audio = Pan2.ar(audio,0);
	OffsetOut.ar(out,audio);
}).store;

SynthDef(\talk,{ |out =0 freq=1200, talking = 200, filter=4000, mod = 6,sustain =0.01 amp=0.7|
	var audio;
	audio = SinOsc.ar(freq*2,SinOsc.ar(mod*talking,0,1),0.5);
	audio = audio* EnvGen.ar(Env.perc,1, levelScale:amp,timeScale:sustain ,doneAction:2);
	audio = Pan2.ar(audio,0);
	OffsetOut.ar(out,audio);
}).store;
)

//this block is listeners for OSC messages.
(
~s = OSCdef(\sines,{|msg,time,addr,recvPort|
	msg.postln;
	Synth("sines",[freq:msg[1],filter:msg[2],phase:msg[3]]);
},\synth,n);

 ~a = OSCdef(\synth1, {|msg,time,addr,recvPort|
 	msg.postln;
 	Synth("sines", [ freq:msg[1],amp:msg[2]]);
 },\synth1, n);
 ~b = OSCdef(\synth2, {|msg,time,addr,recvPort|
	msg.postln;
 	Synth("square", [ freq:msg[1],amp:msg[2]]);
 },\synth2 , n);
 ~c = OSCdef(\synth3, {|msg,time,addr,recvPort|
 	msg.postln;
	Synth("square", [ freq:msg[1],amp:msg[2],width:(0.1,0.2..0.9).choose;]);
 },\synth3 , n);
 ~d = OSCdef(\talk, {|msg,time,addr,recvPort|
 	msg.postln;
 	Synth("talk", [talking:msg[1] ]);
 },\talk , n);

 )

 //use these to stop things!
~a.free;
~b.free;
~c.free;
~d.free;
~s.free;
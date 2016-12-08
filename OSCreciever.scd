s.boot;
// SynthDef(\grains, { | out=0, bufnum = 0, filter = 100, rate = 1, startPos = 0, amp = 0.1, sustain = 1, pan = 0, loop = 1|
// 	var audio;
// 	rate = rate * BufRateScale.kr(bufnum);
// 	startPos = startPos * BufFrames.kr(bufnum);
//
// 	audio = BufRd.ar(2, bufnum, Phasor.ar(0, rate, startPos, BufFrames.ir(bufnum)), 1, 1);
// 	audio = EnvGen.ar( Env.perc(), 1, timeScale: sustain, doneAction: 2) * audio;
// 	audio = Pan2.ar(RLPF.ar(audio,filter,1.5), pan, amp);
// 	OffsetOut.ar(out, audio);
// }).store;


SynthDef(\sines,{ |out =0 freq=440, mod = 33,sustain =1 amp=0.7|
	var audio;
	audio = SinOsc.ar(freq,SinOsc.ar(mod));
	audio = audio* EnvGen.ar(Env.sine,1, levelScale:amp,timeScale:sustain ,doneAction:2);
	audio = Pan2.ar(audio,1.5);

	OffsetOut.ar(out,audio);
}).store;

SynthDef(\talk,{ |out =0 freq=1200, talking = 200, filter=4000, mod = 6,sustain =1 amp=0.7|
	var audio;
	audio = SinOsc.ar(freq,SinOsc.ar(mod*talking,0,1));
	audio = audio* EnvGen.ar(Env.perc,1, levelScale:amp,timeScale:sustain ,doneAction:2);
	audio = Pan2.ar(audio,0);

	OffsetOut.ar(out,audio);
}).store;


//b = Buffer.read(s, Platform.resourceDir +/+ "sounds/BLOOMER.WAV");

//OSCdef(\grains, {|msg, time, addr, recvPort|
//	msg.postln;
//	Synth("grains", [bufnum:b.bufnum, rate:msg[1], sustain:msg[4], startPos:msg[3], filter:msg[2]]);},\synth1 , n);


OSCdef(\synth, {|msg,time,addr,recvPort|
	msg.postln;
	Synth("sines", [ sustain:msg[1],freq:msg[2], mod:msg[3]*10 ]);
  },\synth1 , n);

OSCdef(\talk, {|msg,time,addr,recvPort|
	msg.postln;
	Synth("talk", [talking:msg[1] ]);
  },\talk , n);


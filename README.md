# grabTorcs
grab Torcs image .

## how to use
1. patch torcs with scr-patch (for torcs 1.3.7).
2. run torcs, select quick race.
3. run udp.py, --save_dir is save folder in your current working directory,default is data; --target_speed is speed of car.
4. use xbox360 to control car,left joystick for accelerate and brake, right joystick for steer.
## tips
you can change torcs/src/libs/raceengineclient/raceengine.cpp ReOneStep function(about line 625 in my case) to get more grab FPS, count is 50 for 10 FPS.


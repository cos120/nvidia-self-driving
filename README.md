# nvidia-self-driving
nvidia-self-driving
[paper](https://arxiv.org/abs/1604.07316)
## how to use
1. patch torcs with scr-patch (for torcs 1.3.7).
2. run torcs, select quick race.
3. tool/getTrainData.py to get train data from torcs
4. use xbox360 to control car,left joystick for accelerate and brake, right joystick for steer.
5. nvidia_keras for train model
6. drive_keras for run model
7. visual_back_prop.py for visualize model [paper](https://arxiv.org/abs/1611.05418)
## tips
you can change torcs/src/libs/raceengineclient/raceengine.cpp ReOneStep function(about line 625 in my case) to get more grab FPS, counting 50 for 10 FPS.


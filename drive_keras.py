"""
author: zj
file: drive_keras.py
time: 17-7-19
"""
import numpy as np
from keras.models import load_model

import tool.driveTool as driverTool
from tool import screenshot, snakeoil3_gym

model = load_model('model-029.h5')
C = snakeoil3_gym.Client( p=3001 )  # 3001
driver = driverTool.driveClient( 50, C, None )
imageTool = screenshot.screenShotFromC()
i = 0
for step in range( C.maxSteps, 0, -1 ):
    C.get_servers_input()
    image = imageTool.getImage()
    i+=1
    image = np.array([image[ 90:156, 60:260 ]])
    angle = model.predict(image)
    print(angle)
    driver.dataDrive( angle[0][0] )
    C.respond_to_server()
C.shutdown()

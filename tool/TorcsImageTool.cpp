//
// Created by zj on 17-6-21.
//

#include <iostream>
#include <unistd.h>
#include <sys/shm.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

#define image_width 640
#define image_height 480

struct shared_use_st
{
    int written;
    uint8_t data[image_width*image_height*3];
    int pause;
    int zmq_flag;
    int save_flag;
};


class TorcsImageTool{
private:
    void *shm = NULL;
    bool flg;
    struct shared_use_st *shared;

public:
    TorcsImageTool(){
        int shmid = shmget((key_t)1234, sizeof(struct shared_use_st),0666| IPC_CREAT);
        flg = true;
        if(shmid == -1){
            cout<<"error in shmget"<<endl;
        }

        shm = shmat(shmid, NULL, 0);
        if(shm ==  (void*)-1){
            cout<<"error in shmat"<<endl;
        }
        shared = (struct shared_use_st*)shm;
        shared->written = 0;
        shared->pause = 0;
        shared->zmq_flag = 0;
        shared->save_flag = 0;
        printf("\n********** Memory sharing started, attached at %X **********\n", shm);
    }
    void reverseGetImageFlag(){
        shared->pause = 1 - shared->pause;
    }

    uint8_t* getImage(){
        while(flg){
            if(shared->written == 1){
//                cout<<"1";
                shared->written = 0;
                return shared->data;
            }

        }
    }

    void stop(){
        flg = false;
    }
};

extern "C"{
    TorcsImageTool* getScreenshotTool(){return new TorcsImageTool();}
    void reserveScreenShotFlag(TorcsImageTool* imageTool){imageTool->reverseGetImageFlag();}
    void stopTorcsImageTool(TorcsImageTool* imageTool){imageTool->stop();}
    uint8_t* getScreenshot(TorcsImageTool* imageTool){return imageTool->getImage();}
}

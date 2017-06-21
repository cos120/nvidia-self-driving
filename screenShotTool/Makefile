all: target

cc=g++
TorcsScreenShot.o: TorcsImageTool.cpp
	$(cc) -c -fpic TorcsImageTool.cpp -o TorcsScreenShot.o 

target: TorcsScreenShot.o
	$(cc) -shared -Wl,-soname,TorcsScreenShot.so  TorcsScreenShot.o -o TorcsScreenShot.so


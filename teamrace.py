#!/usr/bin/python
# Here’s a complete example of a program that will spawn(产生,生产) 4 clients to control 4 different cars.
# This program will make 4 identical(相同的) cars on ports 3001-3004. This makes 4 cars with identical behavior.
import snakeoil
if __name__ == "__main__":
    Cs= [ snakeoil.Client(p=P) for P in [3001,3002,3003,3004] ]
    for step in range(Cs[0].maxSteps,0,-1):
        for C in Cs:
            C.get_servers_input()
            snakeoil.drive_example(C)
            C.respond_to_server()
    else:
        for C in Cs: C.shutdown()
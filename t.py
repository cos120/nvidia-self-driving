
import snakeoil3_gym


if __name__ == "__main__":
    C= snakeoil3_gym.Client()
    for step in range(C.maxSteps,0,-1):
        C.get_servers_input()
        snakeoil3_gym.drive_example(C)
        C.respond_to_server()
    C.shutdown()

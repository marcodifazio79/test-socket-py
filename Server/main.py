from server_soket import SocketSRV
"""
Main class to run
"""
class MAIN():
    
    def __init__(confparam) -> None:
        confparam.socket_obj = SocketSRV()
    def start(confparam):
        confparam.socket_obj.start()


if __name__ == "__main__":
    MAIN().start()

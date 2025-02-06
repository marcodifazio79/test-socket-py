import socket
import sys
import threading
import DatabaseFunctions   
import string
import random

from datetime import date, datetime, timedelta
now = datetime.now() 

def create_random_string():#size=4, chars=string.digits):
    all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase #+ string.punctuation
    return ''.join(random.choice(all_chars) for _ in range(8))



def Thread_SocketCommand():
    # Create a TCP/IP socket
    sock_forcommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_forcommand = ('192.168.10.20', 9909)
    print (sys.stderr, 'starting up on %s port %s' % server_forcommand)
    sock_forcommand.bind(server_forcommand)

    # Listen for incoming connections
    sock_forcommand.listen(1000)
    while True:
        # Wait for a connection
        print (sys.stderr, 'waiting for a connection')
        connection, modem_IP_address = sock_forcommand.accept()
    #   connection, modem_IP_address = sock_forcommand.accept()
        print(f"Connessione Server - Client Stabilita: {modem_IP_address}")
        
        try:
            print (sys.stderr, 'connection from', modem_IP_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(500)
                daterecived=str(data)
                daterecived=daterecived.replace("b'","")
                daterecived=daterecived.replace("'","")
                if __name__ == "__main__":
                    print (sys.stderr, 'received "%s"' % daterecived)
                    if data:
                        print (sys.stderr, 'sending data back to the client')
                        connection.send(b"sto cazzo")
                    else:
                        print (sys.stderr, 'no more data from', modem_IP_address)
                        break
        except:
            connection.close()        
        finally:
            # Clean up the connection
                connection.close()


def Thread_SocketListener():
    # Create a TCP/IP socket
    sock_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_Listener = ('192.168.10.20', 9005)
    print (sys.stderr, 'starting up on %s port %s' % server_Listener)
    sock_listener.bind(server_Listener)

    # Listen for incoming connections
    sock_listener.listen(1000)

    #sock_forcommand.listen(1000)

    x = threading.Thread(target=Thread_SocketCommand, args=())
    x.start()

    while True:
        # Wait for a connection
        print (sys.stderr, 'waiting for a connection')
        connection, modem_IP_address = sock_listener.accept()
    #   connection, modem_IP_address = sock_forcommand.accept()
        print(f"Connessione Server - Client Stabilita: {modem_IP_address}")
        
        try:
            print (sys.stderr, 'connection from', modem_IP_address)
            #DatabaseFunctions.InsertInto_Machines(modem_IP_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(500)
                daterecived=str(data)
                daterecived=daterecived.replace("b'","")
                daterecived=daterecived.replace("'","")

                if __name__ == "__main__":
                        
                    if (daterecived=="<^>"):
                        # todo CheckCommandToSend 
                        connection.send ("#PWD123456#,"+"WDR")
                            
                    if daterecived.startswith("<MID="):#tipo RECV
                        #all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase #+ string.punctuation
                        lastinfo = now.strftime("%Y/%m/%d,%H:%M:%S")
                        #resstring="#PWD123456#ROK,"+create_random_string(size=8, chars=all_chars)+"," +lastinfo
                        resstring="#PWD123456#ROK,"+create_random_string()+"," +lastinfo
                        connection.send(resstring.encode("utf-8"))   
                        print (sys.stderr, lastinfo+' - Sending data back to the client: '+resstring) 
                        DatabaseFunctions.updateModemTableEntry(str(modem_IP_address) , daterecived)
                        
                    DatabaseFunctions.InsertInto_MachineConnectionTrace(str(modem_IP_address) , daterecived)

                    print (sys.stderr, 'received "%s"' % daterecived)

        except:
            connection.close()        
        finally:
            # Clean up the connection
                connection.close()



def CheckDataInfo(_infoIP,_infoData):
    data_received=str(_infoData)
    if data_received.startswith("<TPK="):#tipo RECV
        DatabaseFunctions.insertMachineConnectionTrace(0,_infoIP,_infoData)
                           
    if data_received.startswith("<MID="):#tipo RECV
        if data_received.__contains__(">^<") | data_received.__contains__("><TPK="):
            data_rec_split=data_received.split("^")
            if data_rec_split[1].StartsWith("<TPK=$"):
                DatabaseFunctions.InsertInto_Machines(_infoIP,data_rec_split[0])
                DatabaseFunctions.InsertInto_MachineConnectionTrace(0,_infoIP,data_rec_split[1])
                
        else:
            DatabaseFunctions.InsertInto_Machines(_infoIP,data_received)

        

    if data_received.startswith("<TCA="):#<TCA=ROK,Eevlq972,24/11/29,06:53:43=OK> 
        DatabaseFunctions.insertMachineConnectionTrace(0,_infoIP,_infoData)

    #if str(_infoData).__contains__("#PWD="):#tipo SEND                


if __name__ == "__main__":
    Thread_SocketListener()

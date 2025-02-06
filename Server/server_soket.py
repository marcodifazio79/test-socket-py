import socket
import sys
import threading
import string
import random
import json
import requests
import os
import DatabaseFunctions
import xml.etree.ElementTree as ET



from requests.auth import AuthBase

from datetime import date, datetime, timedelta
now = datetime.now() 
    
class SocketSRV():

    def __init__(confparam) -> None:
        pathapp = os.path.dirname(os.path.abspath(sys.argv[0])) 
        json_path =pathapp+"\\config.json"
        jsonfile = open(json_path)
        data = json.load(jsonfile)
                
        SocketSRV.db_host = data.get("db",{}).get("db_host","conf_value")
        SocketSRV.db_name = data.get("db",{}).get("db_name","conf_value")
        SocketSRV.db_user = data.get("db",{}).get("db_user","conf_value")
        SocketSRV.db_password = data.get("db",{}).get("db_password","conf_value")

        SocketSRV.api_user = data.get("api_info",{}).get("user","conf_value")
        SocketSRV.api_pwd = data.get("api_info",{}).get("pwd","conf_value")
        SocketSRV.api_sendDataRaw = data.get("api_info",{}).get("api_sendDataRaw","conf_value")
        SocketSRV.api_sendCmdAnswer = data.get("api_info",{}).get("api_sendCmdAnswer","conf_value")

        SocketSRV.after_idle_sec = int(data.get("socket",{}).get("after_idle_sec","conf_value"))
        SocketSRV.interval_sec = int(data.get("socket",{}).get("interval_sec","conf_value"))
        SocketSRV.max_fails = int(data.get("socket",{}).get("max_fails","conf_value"))
        SocketSRV.host = data.get("socket",{}).get("host","conf_value")
        SocketSRV.port_modem =int(data.get("socket",{}).get("port_mdm","conf_value"))
        SocketSRV.port_command =int(data.get("socket",{}).get("port_cmd","conf_value"))

        SocketSRV.ThreadCount =int( data.get("socket",{}).get("ThreadCount","conf_value"))
        SocketSRV.bytes_recv =int( data.get("socket",{}).get("bytes_recv","conf_value"))
        SocketSRV.decoder = data.get("socket",{}).get("decoder","conf_value")
        SocketSRV.timer_commands =int( data.get("socket",{}).get("timer_commands","conf_value"))
        SocketSRV.code_socket_closed =int( data.get("socket",{}).get("code_socket_closed","conf_value"))
        SocketSRV.timeout_not_registered =int( data.get("socket",{}).get("timeout_not_registered","conf_value"))
        SocketSRV.timer_keep_alive =int( data.get("socket",{}).get("timer_keep_alive","conf_value"))
        

    def start(confparam):
        try:
            Thread_SocketListener()
        except Exception as e:
            print (e)
            return False

def API_Sendtrace(DataRaw):
        payload = {'newDataRaw':DataRaw}
        r=requests.get(SocketSRV.api_sendDataRaw,auth=(SocketSRV.api_user,SocketSRV.api_pwd),params=payload)

        if (r.status_code!="OK"):
            DatabaseFunctions.InsertInto_TEST_TRACE(DataRaw)

        print(r.status_code)
        return(r.status_code) 
        
def API_SendCommandAnswer(ipAdd,infodata):
        payload = {'ipAddress': ipAdd, 'infoanswer': infodata}

        r=requests.get(SocketSRV.api_sendCmdAnswer,auth=(SocketSRV.api_user,SocketSRV.api_pwd),params=payload)
        if (r.status_code!="OK"):
            DatabaseFunctions.InsertInto_ANSWER_TRACE(ipAdd,infodata)

        print(r.status_code)
        return(r.status_code) 

   
def create_random_string(lastinfo):#size=4, chars=string.digits):
    all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase #+ string.punctuation
    messToSend="#PWD123456#ROK,"+ ''.join(random.choice(all_chars) for _ in range(8))  + "," +lastinfo  
    return messToSend
    
def Create_Cmd_modem (xmlstring):# converte la stringa xml ricevuta dal frontend in un comando fruibile dal modem
    #<data><codElettronico>00025115</codElettronico><command>setLgg</command><value>30</value></data> 

    root = ET.fromstring(xmlstring)    
    for child in root:
        print(child.text , child.at)






# def CheckCommandPending(daterecived):
#     #cmd = "<MID=00002222-864086987654321><VER=VCG398D>";
#     splitdata =[ daterecived.split("-")]
#     mid=splitdata[0].replace("<MID=","")


def SendCommandtoModem(commandstring):

    s = socket.socket()
    #port = 9909
    s.bind((SocketSRV.host, SocketSRV.port_command))
    s.listen(1000)
    c, addr = s.accept()
    print("Socket Up and running with a connection from",addr)
    ipAdd=str(addr).replace("(","")
    ipAdd=ipAdd.replace(")","")
    ipAdd=ipAdd.replace("\'","")
    ipAdd=ipAdd.split(',')
    print(ipAdd[0])

    try:
        while True:
            rcvdData = c.recv(1024).decode()
            print (rcvdData)
            dataRecive=str(rcvdData)
            if (dataRecive.startswith("<TCA=")):
                 API_SendCommandAnswer(ipAdd[0],dataRecive)
            sendData = commandstring
            c.send(sendData.encode())
            if(sendData == "Bye" or sendData == "bye"):
                break
    except:
        c.close()        
    finally:
        c.close()

def Thread_SocketCommand():
    sock_forcommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Create a TCP/IP socket
    server_forcommand = (SocketSRV.host, SocketSRV.port_command) # #server_forcommand = ('0.0.0.0', 9909)
    print (sys.stderr, 'starting up on %s port %s' % server_forcommand)
    sock_forcommand.bind(server_forcommand)

    sock_forcommand.listen(1000)
    while True:
        print (sys.stderr, 'waiting for a connection')
        connection, modem_IP_address = sock_forcommand.accept()
        print(f"Connessione Server - Client Stabilita: {modem_IP_address}")
        
        try:
            print (sys.stderr, 'connection from', modem_IP_address)
            while True:
                data = connection.recv(SocketSRV.bytes_recv).decode()
                daterecived=str(data)
                if __name__ == "server_soket":
                    print (sys.stderr, 'received "%s"' % daterecived)
                    if data:
                        
                        print (sys.stderr, 'sending data back to the client')
                        sendData = DatabaseFunctions.Get_CMD_for_modem(data)
                        connection.send(sendData.encode())
                    else:
                        print (sys.stderr, 'no more data from', modem_IP_address)
                        break
        except:
            connection.close()        
        finally:
            # Clean up the connection
            connection.close()

def Thread_SocketListener():
    
    sock_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_Listener = (SocketSRV.host, SocketSRV.port_modem) #server_Listener = ('0.0.0.0', 9005)
    print (sys.stderr, 'starting up on %s port %s' % server_Listener)
    sock_listener.bind(server_Listener)
    sock_listener.listen(1000)

    x = threading.Thread(target=Thread_SocketCommand, args=())
    x.start()

    while True:
        print (sys.stderr, 'waiting for a connection')
        connection, modem_IP_address = sock_listener.accept()
        print(f"Connessione Server - Client Stabilita: {modem_IP_address}")
        
        try:
            print (sys.stderr, 'connection from', modem_IP_address)
            while True:
                data = connection.recv(SocketSRV.bytes_recv)
                daterecived=str(data)
                daterecived=daterecived.replace("b'","")
                daterecived=daterecived.replace("'","")

                if __name__ == "server_soket":
                        
                    if (daterecived=="<^>"):
                        # todo CheckCommandToSend 
                        connection.send ("#PWD123456#,"+"WDR")
                            
                    if daterecived.startswith("<MID="):#tipo RECV
                        lastinfo = now.strftime("%Y/%m/%d,%H:%M:%S")
                        resstring=create_random_string(lastinfo)
                        connection.send(resstring.encode(SocketSRV.decoder))   
                        print (sys.stderr, lastinfo+' - Sending data back to the client: '+resstring) 
                        API_Sendtrace(daterecived)
                        CheckCommandPending(modem_IP_address)
        
                    print (sys.stderr, 'received "%s"' % daterecived)

        except:
            connection.close()        
        finally:
            connection.close()



# def CheckDataInfo(_infoIP,_infoData):
#     data_received=str(_infoData)
#     if data_received.startswith("<TPK="):#tipo RECV
#         DatabaseFunctions.insertMachineConnectionTrace(0,_infoIP,_infoData)
                        
#     if data_received.startswith("<MID="):#tipo RECV
#         if data_received.__contains__(">^<") | data_received.__contains__("><TPK="):
#             data_rec_split=data_received.split("^")
#             if data_rec_split[1].StartsWith("<TPK=$"):
#                 DatabaseFunctions.InsertInto_Machines(_infoIP,data_rec_split[0])
#                 DatabaseFunctions.InsertInto_MachineConnectionTrace(0,_infoIP,data_rec_split[1])
                
#         else:
#             DatabaseFunctions.InsertInto_Machines(_infoIP,data_received)

        

#     if data_received.startswith("<TCA="):#<TCA=ROK,Eevlq972,24/11/29,06:53:43=OK> 
#         DatabaseFunctions.insertMachineConnectionTrace(0,_infoIP,_infoData)

        
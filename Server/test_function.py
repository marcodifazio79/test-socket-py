import sys
#import DatabaseFunctions
import mysql.connector

import string
import random
import os 
import sys 
import io
import socket
import json
import requests
import DatabaseFunctions
import server_soket
import threading

import xml.etree.ElementTree as ET

#from xml.etree.ElementTree import XML, fromstring

from datetime import date, datetime, timedelta

now = datetime.now() 

def create_random_string(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def testrandomfuntcion():
    all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase #+ string.punctuation
    lastinfo = now.strftime("%Y/%m/%d,%H:%M:%S")
    resstring="#PWD123456#ROK,"+create_random_string(size=8, chars=all_chars)+"," +lastinfo
    print(resstring) 

def testxmlreader(xmlstring):

    
    root = ET.fromstring(xmlstring)    
    for child in root:
        print(child.text , child.attrib)
    
def load_API_Sendtrace():
    
    API_Sendtrace("<TPK=$M1,00025115,11,100,50,87,10,0,20,0,50,3582,100,14179,200,5161,0,0,9999,8,2633550,26319,0,628,0,30,31494,0*1E,00025115,C.26,89314404000840961628,861230048298112,16,99,P,0,0,30,240,31494+11>")
    API_Sendtrace("<TCA=#MHD?-00025115>")
    API_Sendtrace("#PWD123456#MHD?")
    API_Sendtrace("#PWD123456#ROK,NnoZPY1C,25/01/28,06:13:19")
    API_Sendtrace("<MID=00025115-861230048298112><VER=C.26>^")


def API_Sendtrace(DataRaw):
        payload = {'newDataRaw':DataRaw}
        r=requests.get("https://tlk-svi.dedemapp.com/api/SendTrace",auth=("sviluppoapp@dedem.it","2Yk9[qqx)@@HrqP2"),params=payload)

        if (r.status_code!=200):
            DatabaseFunctions.InsertInto_TEST_TRACE(DataRaw)

        print(r.status_code)
        return(r.status_code) 
        

def API_SendCommandAnswer(ipAdd,infodata):
        payload = {'ipAddress': ipAdd, 'infoanswer': infodata}

        r=requests.get("https://tlk-svi.dedemapp.com/api/SendCommandAnswer",auth=("sviluppoapp@dedem.it","2Yk9[qqx)@@HrqP2"),params=payload)
        if (r.status_code!=200):
            DatabaseFunctions.InsertInto_ANSWER_TRACE(ipAdd,infodata)

        print(r.status_code)
        return(r.status_code) 
    



def CheckCommmandQueue(ipaddress):
    
    cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
    cnx._open_connection()
    cursor = cnx.cursor()
    

    info_IP_Port=str(ipaddress).replace("(","")
    info_IP_Port=info_IP_Port.replace(")","")
    info_IP_Port=info_IP_Port.replace("\'","")
    info_IP_Port=info_IP_Port.split(',')
    info_IP_Port[1]=info_IP_Port[1].replace(" ","")
    print(info_IP_Port[0],info_IP_Port[1])

   # CmdAnswerCMD=CmdStructure(id=id,ip_address=ipaddress,command="",value_param="",time_stamp=now.strftime("%Y/%m/%d,%H:%M:%S"), pending=True)

    sqlstr="SELECT command,value_param FROM commandrequest Where ip_address ='"+ info_IP_Port[0] +"'"
    cursor.execute(sqlstr)
    myresult = cursor.fetchall()
    count=cursor.rowcount

    if count==0:
        Mid_AlredyRegistred=False
        
    else:
        Mid_AlredyRegistred=True
        info=[]
        for x in myresult:
            info=str(x).split(',')

        sqlstr="SELECT ModemCommand FROM command_list Where WebCommand ='"+ info_IP_Port[0] +"'"
        cursor.execute(sqlstr)
        myresult = cursor.fetchall()
        count=cursor.rowcount

        SendCommandtoModem("#PWD123456#MHD?")

def SendCommandtoModem(commandstring):

    s = socket.socket()
    port = 9909
    s.bind(('192.168.10.9', port))
    s.listen(1000)
    c, addr = s.accept()
    print("Socket Up and running with a connection from",addr)
    info_IP_PORT=str(addr).replace("(","")
    info_IP_PORT=info_IP_PORT.replace(")","")
    info_IP_PORT=info_IP_PORT.replace("\'","")
    info_IP_PORT=info_IP_PORT.split(',')
    info_IP_PORT[1]=info_IP_PORT[1].replace(" ","")
    print(info_IP_PORT[0],info_IP_PORT[1])

    # x = threading.Thread(target=Testreinviodati(ipAdd[0],ipAdd[1]), args=())
    # x.start
    try:
        while True:
            rcvdData = c.recv(1024).decode()
            print (rcvdData)
            dataRecive=str(rcvdData)
            if (dataRecive.startswith("<TCA=")):
                 API_SendCommandAnswer(info_IP_PORT[0],dataRecive)
            sendData = commandstring
            c.send(sendData.encode())
            if(sendData == "Bye" or sendData == "bye"):
                break
    except:
        c.close()        
    finally:
            # Clean up the connection
        c.close()
    
 




    
def test():
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
    print(script_directory)

if __name__ == '__main__':
    #SendCommandtoModem("#PWD123456#MHD?")
    #load_API_Sendtrace()
    DatabaseFunctions.Get_CMD_for_modem("<data><codElettronico>00025115</codElettronico><command>setLgg</command><value>30</value></data>")

from __future__ import print_function
from datetime import date, datetime, timedelta

import xml.etree.ElementTree as ET

import mysql.connector
now = datetime.now() # current date and time


from collections import namedtuple

CmdStructure= namedtuple("CommandStructur","id mid command value_param time_stamp pending")

def SaveCommmand (xmlstring):
    root = ET.fromstring(xmlstring)    
    for child in root:
        print(child.text , child.attrib)


def Get_CMD_for_modem(xmlstring):      
    try:
        root = ET.fromstring(xmlstring)    
        cmd=""
        mid=""
        value=""
        ipaddress=""
        stringcommand="#PWD123456"
        i=1
        for child in root:
            print(child.text , child.tag)
            match child.tag:
                case "codElettronico":
                    mid=child.text
                case "command":
                    cmd=child.text
                case "ipaddress":
                    ipaddress=child.text    
                case "value":
                    value=child.text
                    

        cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
        cnx._open_connection()
        cursor = cnx.cursor()
        sqlstr="SELECT ModemCommand FROM command_list Where WebCommand ='"+ cmd +"'"
        cursor.execute(sqlstr)
        myresult = cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            Mid_AlredyRegistred=False
            
        else:
            Mid_AlredyRegistred=True
            tmpsplit=[]
            for x in myresult:
                tmpsplit=str(x).split(',')
                realCMD=tmpsplit[0]
                realCMD=realCMD.replace("(","")
                realCMD=realCMD.replace("'","")

            stringcommand=stringcommand+realCMD+value 

            return stringcommand
    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()
        return str(e)  

    finally:
        cursor.close()
        cnx.close()  


def CheckCommmand(ipaddress):
    
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

        sqlstr="SELECT ModemCommand FROM command_list Where WebCommand ='"+ info[0] +"'"
        cursor.execute(sqlstr)
        myresult = cursor.fetchall()
        count=cursor.rowcount
        cursor.close()
        cnx.close()  
        

def InsertInto_TEST_TRACE(DATA_RAW):
    try:
        cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
        cnx._open_connection()
        cursor = cnx.cursor()
    
       

        Prefix_Datarow=str(DATA_RAW)[:6]

        #verifica esistenza riga su db

        match Prefix_Datarow:
            case "<TPK=$":
                Info_Datarow=str(DATA_RAW)[:17]#<TPK=$M1,00025115
            case "#PWD12":
                Info_Datarow=str(DATA_RAW)[:14] ##PWD123456#ROK
                if (Info_Datarow!="#PWD123456#ROK"):
                    Info_Datarow=str(DATA_RAW)
            case "<MID=0":
                Info_Datarow=str(DATA_RAW)[:12]#<MID=00025115
            case "<TCA=#":
                Info_Datarow=str(DATA_RAW)

            case _:
                Info_Datarow=""

        sqlstr="SELECT id FROM test_trace Where data_raw LIKE '"+ Info_Datarow +"%' LIMIT 0, 1"

        print (sqlstr)
        cursor.execute(sqlstr)
        myresult = cursor.fetchall()
        count=cursor.rowcount
        
        if count==0:
            add_row = ("INSERT INTO test_trace "
                    "(time_stamp, data_raw)"
                    "VALUES (%s, %s)")

            data_row = (date_now, DATA_RAW)
            cursor.execute(add_row, data_row)
                                    
            cnx.commit()
        else:
            info=[]

            for x in myresult:
                info=str(x).split(',')

            idrow=info[0].replace("(","")
            
            date_now = now.strftime("%Y/%m/%d %H:%M:%S")
            print(date_now)
            sql = "UPDATE test_trace SET time_stamp = '"+date_now+"', data_raw = '"+ DATA_RAW +"' Where id ='"+ idrow +"'"
            cursor.execute(sql)
            cnx.commit()

    except Exception as e:
        print(e)
        cursor.close()
        cnx.close()   

    finally:
        cursor.close()
        cnx.close()   

    
    


def InsertInto_ANSWER_TRACE(ip,datainfo):
    try:

        cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
        cnx._open_connection()
        cursor = cnx.cursor()

        date_now = now.strftime("%Y/%m/%d %H:%M:%S")

        #verifica esistenza comand su db
        sqlstr="SELECT id FROM answer_trace Where ip_address ='"+ str(ip) +"' and data_answer = '"+str(datainfo)+"' LIMIT 0, 1"

        cursor.execute(sqlstr)
        myresult = cursor.fetchall()

        count=cursor.rowcount
        if count==0:
            add_row = ("INSERT INTO answer_trace "
                    "(ip_address,data_answer, time_stamp)"
                    "VALUES (%s, %s,%s)")

            data_row = (ip,datainfo,date_now)

            cursor.execute(add_row, data_row)
                                    
            cnx.commit()
            
            
        else:
     
            info=[]

            for x in myresult:
                info=str(x).split(',')

            idrow=info[0].replace("(","")
            date_now = now.strftime("%Y/%m/%d %H:%M:%S")
            sql = "UPDATE answer_trace SET time_stamp = '"+date_now+"' Where id ='"+ idrow +"'"
            cursor.execute(sql)
            cnx.commit()

        
    except Exception as e:
        print (e)
        cursor.close()
        cnx.close()   
    finally:
        cursor.close()
        cnx.close()   
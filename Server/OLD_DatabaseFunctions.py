from __future__ import print_function
from datetime import date, datetime, timedelta

import xml.etree.ElementTree as ET

import mysql.connector
now = datetime.now() # current date and time


from collections import namedtuple

ModemStruct= namedtuple("ModemInfo","mid imei version ip_add MarkedBroken, id")


def updateModemTableEntry(_infoIP,infoData):
    cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
    cnx._open_connection()
    cursor = cnx.cursor()


    xstr=str(_infoIP).split(",")
    xstr[0]=xstr[0].replace("(","")
    xstr[0]=xstr[0].replace("'","")
    ip_address=xstr[0].replace("(","")

    if (ip_address=="127.0.0.1"):
        return

    datasplit=str(infoData).split(">")

    datasplit[0]=datasplit[0].replace("<TCA=SYNC><MID=","")
    datasplit[0]=datasplit[0].replace("<MID=","")
    datasplit2=datasplit[0].split("-")
    mid=datasplit2[0]
    imei=datasplit2[1]

    version=datasplit[1].replace("<VER=","")

    if (mid=="77770001") or (mid.startswith("5555555"))or (mid=="TCC"):
        mid=mid+"_"+imei.ToString()
                    
    InfoModemRecived=ModemStruct(mid=mid,imei=imei,ip_add=ip_address,version=version,MarkedBroken=0,id=0)

    sqlstr="SELECT mid,imei,ip_address,version,MarkedBroken,id FROM machines Where ip_address ='"+ ip_address +"'"
    #sqlstr="SELECT mid,imei,ip_address,version,MarkedBroken FROM machines Where mid ='"+ mid +"'"
    
    print (sqlstr)
    cursor.execute(sqlstr)

    myresult = cursor.fetchone()
#    myresult = cursor.fetchone()
#    myresult = cursor.fetchmany(2)
    
    count=cursor.rowcount

    if count<0:
        Mid_AlredyRegistred=False
        
    else:
        Mid_AlredyRegistred=True
        info=[]

        for x in myresult:
            info.append(x)

        InfoModemInTable=ModemStruct(mid=info[0],imei=info[1],ip_add=info[2],version=info[3],MarkedBroken=info[4],id=info[5])

        if (str(InfoModemInTable.mid).startswith("Recupero")):    
            date_now = now.strftime("%Y/%m/%d %H:%M:%S")
            sql = "UPDATE machines SET mid='"+InfoModemRecived.mid+"',imei='"+InfoModemRecived.imei+"',version='"+InfoModemRecived.version +"',IsOnline='1',last_communication = '"+date_now+"' Where ip_address ='"+ ip_address +"'"
            cursor.execute(sql)
            cnx.commit()
            return
        # se mid e imei coincidono aggiorno i campi version last_comucation e IsOnline
        if ((InfoModemInTable.mid==InfoModemRecived.mid)and(InfoModemInTable.imei==InfoModemRecived.imei)):
            date_now = now.strftime("%Y/%m/%d %H:%M:%S")
            sql = "UPDATE machines SET IsOnline='1',last_communication = '"+date_now+"',version='"+InfoModemRecived.version+"' Where ip_address ='"+ ip_address +"'"
            cursor.execute(sql)
            cnx.commit()
            return
        # se i mid coincidono e gli imei no,  aggiorno il campo imei
        if ((InfoModemInTable.mid==InfoModemRecived.mid)and(InfoModemInTable.imei!=InfoModemRecived.imei)):#and(InfoModemInTable.imei==0)):
            #if  (str(InfoModemInTable.version).startswith("PSD")):
            date_now = now.strftime("%Y/%m/%d %H:%M:%S")
            sql = "UPDATE machines SET IsOnline='1',last_communication = '"+date_now+"',imei='"+InfoModemRecived.imei+"' Where ip_address ='"+ ip_address +"'"
            cursor.execute(sql)
            cnx.commit()
            return
        # se i mid coincidono e gli imei no,significa che ho cambiato il modem ,ma non la SIM(mantengo l'ip)
        if (InfoModemInTable.MarkedBroken==1):
                #°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° da verificare
                date_now = now.strftime("%Y/%m/%d %H:%M:%S")
                sql = "UPDATE machines SET IsOnline='1',last_communication = '"+date_now+"',imei='"+InfoModemRecived.imei+"' Where ip_address ='"+ ip_address +"'"
                cursor.execute(sql)
                cnx.commit()
                #°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
        if ((InfoModemInTable.mid==InfoModemRecived.mid)and(InfoModemInTable.imei!=InfoModemRecived.imei)and(InfoModemInTable.MarkedBroken==0) ):
                date_now = now.strftime("%Y/%m/%d %H:%M:%S")
                sql = "UPDATE machines SET IsOnline='1',last_communication = '"+date_now+"',imei='"+InfoModemRecived.imei+"' Where ip_address ='"+ ip_address +"'"
                cursor.execute(sql)
                cnx.commit()

         #nextlevel:       



    cursor.close()
    cnx.close()    


    

def InsertInto_Machines(ip_address):#qui il modem fa la prima connessione al socket e arriva esclusivamente l'ip
    
    cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')
    cnx._open_connection()
    cursor = cnx.cursor()
 
    xstr=str(ip_address).split(",")
    xstr[0]=xstr[0].replace("(","")
    xstr[0]=xstr[0].replace("'","")
    ip_address=xstr[0].replace("(","")
    sqlstr="SELECT mid,imei,ip_address,version FROM machines Where ip_address ='"+ ip_address +"'"
    print (sqlstr)
    cursor.execute(sqlstr)

    myresult = cursor.fetchone()
#    myresult = cursor.fetchone()
#    myresult = cursor.fetchmany(2)
    
    count=cursor.rowcount

    if count<0: # se l'ip in arrivo non è presente nel db lo inserisco con tutti i valori
        imei=now.strftime("%Y%m%d%H%M%S%f")
        mid="Recupero in corso"+imei
        version=""
        date_now = now.strftime("%Y/%m/%d %H:%M:%S")

        add_machines = ("INSERT INTO machines "
                    "(ip_address, imei, mid, version, IsOnline, last_communication, time_creation, MarkedBroken, LogEnabled, sim_serial)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        data_Machines = (ip_address, imei, mid,version,True,date_now,date_now, False,'0','0')
        cursor.execute(add_machines, data_Machines)
        id_macchina = cursor.lastrowid #se un ip è nuovo invio il valore dell'id del record, 
                                       #se non si registra un modem entro un determinato intervallo di tempo con questo ip elimino il record
        cnx.commit()

    else:
        
        date_now = now.strftime("%Y/%m/%d %H:%M:%S")
        sql = "UPDATE machines SET IsOnline ='1', last_communication = '"+date_now+"' Where ip_address ='"+ ip_address +"'"
        cursor.execute(sql)
        cnx.commit()
        id_macchina=0 #se un ip è gia presente non invio il valore dell'id
        # info=[]

        # for x in myresult:
        #     info.append(x)
        #     updateModemTableEntry(ip_address,_infoData)

    cursor.close()
    cnx.close()    

    return id_macchina
   
def InsertInto_MachineConnectionTrace(_idmacchina, _infoIP,_infoData):
    cnx = mysql.connector.connect(user='bot_user', password='Qwert@#!99', host='127.0.0.1', database='test_py')

    cnx._open_connection()

    cursor = cnx.cursor()
    
    xstr=str(_infoIP).split(",")
    xstr[0].replace("(","")
    
    ip_address=xstr[0].replace("'","")
    
    tr_data=str(_infoData)

    tr_data=tr_data.replace("b","") 
    time_stamp = now.strftime("%Y/%m/%d, %H:%M:%S")


    add_MachineConnectioTrace = ("INSERT INTO machinesconnectiontrace "
                "(time_stamp, ip_address, send_or_recv, transferred_data, id_Macchina)"
                "VALUES (%s, %s, %s, %s, %s)")

    data_MachineConnectioTrace = (time_stamp,ip_address, "Recived", tr_data,_idmacchina,)

    cursor.execute(add_MachineConnectioTrace, data_MachineConnectioTrace)
    
    id_macchina = cursor.lastrowid
    cnx.commit()
    cursor.close()

    cnx.close()    

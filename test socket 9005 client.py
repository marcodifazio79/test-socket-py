import socket
import string

s = socket.socket()

s.connect(('192.168.10.9',9005))

#try:
while True:
    strinfo = ("<MID=77770001-868328053299265><VER=C.26>^<TPK=$M1,77770001,11,100,100,0,10,0,20,0,50,0,100,0,200,0,0,0,9999,0,0,0,0,0,0,30,2,0*15,77770001,C.26,89882280666125028229,868328053299265,22,99,K,0,0,30,240,2+06>")
    s.send(strinfo.encode())
    
    datarecive=s.recv(1024).decode()
    print (datarecive)
    
    strinfo = "Trasmission OK"
    s.send(strinfo.encode());
    commandanswer=""

    if(strinfo == "Bye" or strinfo == "bye"):
        break
    print (s.recv(1024).decode())
# except:
#     s.close()

# finally:
#     s.close()


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host ="192.168.10.9"
# port =9909
# s.connect((host,port))

# def ts(str):
#    s.send('e') 
#    data = ''
#    data = s.recv(1024)
#    print (data)

# while 2:
#    r = input('enter')
#    ts(s)

# s.close ()
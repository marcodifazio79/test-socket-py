import socket
import string

s = socket.socket()
s.connect(('192.168.10.9',9909))

#try:
while True:
    strinfo = ("Connect!")
    s.send(strinfo.encode())
    commandanswer=""
    datarecive=s.recv(1024).decode()
    commandrequest=str(datarecive)
    print (commandrequest)

    if (commandrequest.startswith("#PWD123456")):
        infocmd=commandrequest.split('#')
        if (infocmd[2]=="MHD?"):
            commandanswer="<TCA=#MHD?-00011122>"
    
    strinfo = commandanswer
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
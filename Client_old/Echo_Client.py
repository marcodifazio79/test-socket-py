import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.10.20', 9005)
print (sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)


try:
    
    # Send data
    message = b'<MID=00002222-864086987654321><VER=VCG398D>'
    message = b'<TPK=$M1,00025115,11,100,50,87,10,0,20,0,50,3472,100,13730,200,5018,0,0,9999,8,2554550,25533,0,628,0,30,29685,0*17,00025115,C.26,89314404000840961628,861230048298112,18,99,P,0,0,30,240,29685+1D> '
    message = b'#PWD123456#ROK,RbCOGW2C,24/11/28,07:14:44'
    message = b'<MID=00025115-861230048298112><VER=C.26>^'
    message = b'#PWD123456#MHD?'
    print (sys.stderr, 'sending "%s"' % message)
    sock.send(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    #time.sleep(1)
    while amount_received < amount_expected:
        data = sock.recv(4096).decode
        datarecived=str(data)
        datarecived=datarecived.replace("b'","'")
        datarecived=datarecived.replace("'","")
        amount_received += len(datarecived)
        print (sys.stderr, 'received "%s"' % datarecived)
    

finally:
    print (sys.stderr, 'closing socket')
    sock.close()
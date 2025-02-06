import requests
from server_soket import SocketSRV

from requests.auth import AuthBase


# def __init__(self, Username: str, SubKey: str):
#         self.Username = SocketSRV.api_user
#         self.SubKey = SocketSRV.api_pwd

def API_Sendtrace(DataRaw):
        # '<TPK=$F2,00030052,NCG398O,5,25000,0,0,0,0,0,0,0,1048576,48,48,,0,1,0,0,0,2000,30,1276*38,00030052,NCG398O,89882280666050760929,864086062432327,17,SLIM-3.22,,0,0,30,240,1277+2B>'
        payload = {'newDataRaw':DataRaw}
        #payload = {'newDataRaw':'<TPK=$F2,00030052,NCG398O,5,25000,0,0,0,0,0,0,0,1048576,48,48,,0,1,0,0,0,2000,30,1276*38,00030052,NCG398O,89882280666050760929,864086062432327,17,SLIM-3.22,,0,0,30,240,1277+2B>'}

        r=requests.get("https://tlk-svi.dedemapp.com/api/SendTrace",auth=(SocketSRV.api_user,SocketSRV.api_pwd),params=payload)

        print(r.status_code)

def API_SendCommandAnswer():
        payload = {'mid': 'response', 'key2': 'response'}

        r=requests.get("https://tlk-svi.dedemapp.com/api/SendCommandAnswer",params=payload,auth=("sviluppoapp@dedem.it","2Yk9[qqx)@@HrqP2"))

        print(r.status_code)

# print(r.headers)
# print(r.content)  # bytes
# print(r.text)     # r.content as str

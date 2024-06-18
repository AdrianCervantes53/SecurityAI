import socket
import json
from Exceptions import *

from numpy import empty

class ClienteTCP(object):
    def __init__(self, ipRaspberry, puerto):
        self.host = ipRaspberry
        self.puerto = puerto
        
    def EnviarData(self, data:dict) -> bool:
        try:
            if data is empty:
                raise DictionaryEmpty("No data")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.puerto))
            json_data = json.dumps(data) + '\n'
            client_socket.sendall(json_data.encode('utf-8'))
            client_socket.close()
            return True
        except DictionaryEmpty as e:
            print("SendDict: ",e)
            return False
        except Exception as e:
            print("EnviarData: ",e)
            return False
        
    def ConvertToDict(self, tipo:str, dispositivoId:str, accion:bool) -> dict:
        try:
            data = {
                "tipo": tipo,
                "id": dispositivoId,
                "accion": accion
                }
            return data
        except Exception as e:
            print(e)
            return {}
from PyQt5.QtCore import pyqtSignal, QObject

import json
import socket
import threading

class ServerThread(QObject):
    handleEventSignal = pyqtSignal(dict)

    def __init__(self, host='26.174.164.42', port=1053):
        super().__init__()
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)
        self.allowData = True

    def startServer(self):
        print(f"Servidor escuchando en {self.host}:{self.port}")
        while True:
            clientSocket, clientAddress = self.serverSocket.accept()
            #print(f"Conexión desde {clientAddress}")
            buffer = ""
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    try:
                        jsonData = json.loads(line)
                        print("Recibido JSON:", jsonData)
                        while True:
                            if self.allowData:
                                self.handleEventSignal.emit(jsonData)
                                self.allowData = False
                                break

                    except json.JSONDecodeError:
                        print("No se pudo decodificar el JSON")

            clientSocket.close()

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QAction, QWidget, QToolBar, QLabel
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSlot, QDateTime
from PyQt5 import QtWidgets

import sys
import socket
import json
import threading
from datetime import datetime

from ServidorTCP.HiloServidorTCP import ServerThread
from Interface.Scripts.EventClasses import AlertWindow, DetectionWindow, MessageWindow
from Interface.Designs.SecurityWindow import Ui_WatchMenWindow

class WatchMenApp (QMainWindow, Ui_WatchMenWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setupUi(self)
        self.showNormal()

        self.screen = QApplication.primaryScreen()

        self.alertText = "Desconexión con dispositivo(s): {} "
        self.detectionText = "Se detectó {} en cámara: {}"
        self.messageText = "Conexión establecida con dispositivo(s): {}"
        self.historialText = ""
        self.CamarasConectadas = set()
        self.DvrsConectados = set()
        
        self.serverThread = ServerThread()
        self.serverThread.handleEventSignal.connect(self.handleEvent)

        self.serverThreadInstance = threading.Thread(target=self.serverThread.startServer)
        self.serverThreadInstance.daemon = True
        self.serverThreadInstance.start()

        self.positions = {
            "0": {"tipo": "", "id": set()},
            "1": {"tipo": "", "id": set()},
            "2": {"tipo": "", "id": set()},
            "3": {"tipo": "", "id": set()},
            "4": {"tipo": "", "id": set()},}
        
        self.events = {
            "0": None,
            "1": None,
            "2": None,
            "3": None,
            "4": None
        }

    def NewDeteccionDialog(self, cls):
        newDialog = cls(self.screen, self.RemoveEvent)
        newDialog.setParent(self.eventWidget)
        return newDialog

    @pyqtSlot(dict)
    def handleEvent(self, data):
        if data["tipo"] == "conexion":
            self.ConnectionEvent(data)

        elif data["tipo"] == "deteccion":
            self.DetectionEvent(data)

        elif data["tipo"] == "camaras":
            self.ConfigurarCamaras(data)

        elif data["tipo"] == "dvrs":
            self.ConfigurarDvrs(data)

    def ConfigurarCamaras(self, data):
        del data["tipo"]
        self.camaras = data
        self.serverThread.allowData = True

    def ConfigurarDvrs(self, data):
        del data["tipo"]
        self.dvrs = data
        self.serverThread.allowData = True

    def ConnectionEvent(self, data):
        dispositivoId = data["id"]
        time = QDateTime.currentDateTime().toString("HH:mm:ss")
        #str(datetime.now().time())
        if dispositivoId in self.dvrs:
            nombre = self.dvrs[dispositivoId]["nombre"]
            if data["accion"]:
                self.DvrsConectados.add(dispositivoId)
                historialText = f"{time} - {nombre} -> Conectado"
            else:
                self.DvrsConectados.remove(dispositivoId)
                historialText = f"{time} - {nombre} -> Desconectado"
        else:
            nombre = self.camaras[dispositivoId]["nombre"]
            if data["accion"]:
                self.CamarasConectadas.add(dispositivoId)
                historialText = f"{time} - {nombre} -> Conectado"
            else:
                self.CamarasConectadas.remove(dispositivoId)
                historialText = f"{time} - {nombre} -> Desconectado"
            
        self.historialTextEdit.append(historialText)
        self.AddEvent("msg" if data["accion"] else "alert", dispositivoId)

    def DetectionEvent(self, data):
        time = QDateTime.currentDateTime().toString("HH:mm:ss")
        tipoDeteccion = data["accion"]
        dispositivoId = data["id"]
        nombre = self.camaras[dispositivoId]["nombre"]
        historialText = f"{time} - {nombre} -> Detección{tipoDeteccion}"
        self.historialTextEdit.append(historialText)
        self.AddEvent(tipoDeteccion, dispositivoId)

    def AddEvent(self, tipo, id):
        show = False
        #remover id de evento repetido (conexion-desconexion)
        for value in self.positions.values():
            if (id in value["id"]) and (tipo == "msg" or tipo == "alert") and (value["tipo"] != "Persona"):
                print("updating conecction")
                self.RemoveId(id)
                break

        #agregar id si existe evento de mensaje o alerta 
        for values in self.positions.values():
            if (tipo == "msg" or tipo == "alert") and tipo == values["tipo"]:
                values["id"].add(id)
                show = True
                break

        if not show:
            #agregar evento
            for values in self.positions.values():
                if not values["id"]:
                    values["tipo"] = tipo
                    values["id"].add(id)
                    break
        self.DrawEvents()

    def RemoveId(self, id):
        for pos, value in self.positions.items():
            if id in value["id"]:
                value["id"].remove(id)
                if not value["id"]:
                    self.RemoveEvent(pos, False)
                    break

    @pyqtSlot(str)
    def RemoveEvent(self, pos, show = True):
        self.positions[pos]["tipo"] = ""
        self.positions[pos]["id"].clear()
        self.UpdateEvents(pos)
        if show:
            self.DrawEvents()

    def UpdateEvents(self, pos):
        end = False
        for value in self.positions.values():
            if not end:
                if not value["tipo"]:
                    end = True
            else:
                if value["tipo"]:
                    self.ArrangeEvents(int(pos))
                    break

    def ArrangeEvents(self, pos):
        for i in range(pos, len(self.positions) - 1):
            self.positions[str(i)]["tipo"] = self.positions[str(i + 1)]["tipo"]
            self.positions[str(i)]["id"] = self.positions[str(i + 1)]["id"].copy()
        
    def DrawEvents(self):
        for event in self.events.values():
            try:
                event.exit()
            except:
                ...
        self.events.clear()

        self.events.clear()
        for pos, value in self.positions.items():
            if value["tipo"]:
                if value["tipo"] == "msg":
                    event = self.NewDeteccionDialog(MessageWindow)
                    nombre = ""
                    for id in value["id"]:
                        if id in self.camaras:
                            nombre += self.camaras[id]["nombre"] + ", "
                            continue
                        if id in self.dvrs:
                            nombre += self.dvrs[id]["nombre"] + ", "
                            continue
                    text = self.messageText.format(nombre)

                elif value["tipo"] == "alert":
                    event = self.NewDeteccionDialog(AlertWindow)
                    nombre = ""
                    for id in value["id"]:
                        if id in self.camaras:
                            nombre += self.camaras[id]["nombre"] + ", "
                            continue
                        if id in self.dvrs:
                            nombre += self.dvrs[id]["nombre"] + ", "
                            continue
                    text = self.alertText.format(nombre)
                else:
                    event = self.NewDeteccionDialog(DetectionWindow)
                    camaraId = list(value["id"])[0]
                    text = self.detectionText.format(value["tipo"], self.camaras[camaraId]["nombre"])

                self.events[pos] = event
                event.updateText(text)
                event.showDialog(int(pos))
        #print("SHOW",self.positions)
        self.serverThread.allowData = True
        self.updateConnectedDevices()

    def updateConnectedDevices(self):
        self.totalCamarasLabel.setText(str(len(self.camaras)))
        self.connectedCamarasLabel.setText(str(len(self.CamarasConectadas)))
        self.disconnectedCamarasLabel.setText(str(len(self.camaras) - len(self.CamarasConectadas)))
        
        self.totalDvrsLabel.setText(str(len(self.dvrs)))
        self.connectedDvrsLabel.setText(str(len(self.DvrsConectados)))
        self.disconnectedDvrsLabel.setText(str(len(self.dvrs) - len(self.DvrsConectados)))

    def closeApp(self):
        self.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = WatchMenApp()
    window.show()
    sys.exit(app.exec())
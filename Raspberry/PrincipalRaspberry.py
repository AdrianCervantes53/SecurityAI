from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QListWidget, QAction, QWidget, QToolBar
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import QtWidgets

import sys
import socket
import json
import threading

from ServidorTCP.HiloServidorTCP import ServerThread
from Interface.Scripts.EventClasses import AlertWindow, DetectionWindow, MessageWindow
from Interface.Designs.SecurityWindow import Ui_WatchMenWindow

class WatchMenApp (QMainWindow, Ui_WatchMenWindow):
    def __init__(self):
        super(WatchMenApp, self).__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setupUi(self)
        self.showNormal()

        self.screen = QApplication.primaryScreen()
        #screen = QApplication.primaryScreen()
        #self.detectionDialog = AlertWindow(screen, self.RemoveEvent)
        #self.detectionDialog.setParent(self.eventWidget)
        self.alertText = "Desconexión con dispositivo(s): {} "
        #self.alertDialog = DetectionWindow(screen, self.RemoveEvent)
        #self.alertDialog.setParent(self.eventWidget)
        self.detectionText = "Se detectó {} en cámara: {}"
        #self.messageDialog = MessageWindow(screen, self.RemoveEvent)
        #self.messageDialog.setParent(self.eventWidget)
        self.messageText = "Conexión establecida con dispositivo(s): {}"

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
        self.AddEvent("msg" if data["accion"] else "alert", data["id"])

    def DetectionEvent(self, data):
        self.AddEvent(data["accion"], data["id"])

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
                    print("break2")
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

    def closeApp(self):
        self.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = WatchMenApp()
    window.show()
    sys.exit(app.exec())
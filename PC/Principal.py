from datetime import datetime
import cv2

import requests
from datetime import datetime
import multiprocessing as mp
import threading
from time import time, sleep

from DB.ConexionDB import ConexionDB
from DB.DatosConexionDB import Datos
from TransferenciaRaspberry.ConexionRaspberry import ClienteTCP
from HiloCamara import Observer
from Dispositivos.Camara import Camara
from Dispositivos.DVR import DVR
from Exceptions import *

class WatchMen:
    def __init__(self):
        self.DataBase = ConexionDB(Datos)
        
    def InicializarDispositivos(self, dvrs:dict, camaras:dict) -> (dict, dict): # type: ignore
        dvrObjects = {}
        for key, dvr in dvrs.items():
            dvrObjects[dvr["id"]] = DVR(dvr["ip"], 
                                        dvr["id"], 
                                        dvr["nombre"], 
                                        dvr["puerto"], 
                                        dvr["usuario"],
                                        dvr["contrasena"])
        videoPath = "rtsp://{}:{}@{}:{}/cam/realmonitor?channel={}&subtype=1"
        camaraObjects = {}
        for camara in camaras.values():
            cam = Camara(camara["id"], 
                         camara["iddvr"],
                         camara["nombre"], 
                         camara["canal"], 
                         camara["horarioInicio"],
                         camara["horarioFin"])
            dvrParent = dvrObjects[cam.dvrId]
            cam.camaraIp = videoPath.format(dvrParent.usuario, dvrParent.contrasena, dvrParent.dvrIp, dvrParent.puerto, cam.canal)
            camaraObjects[camara["id"]] = cam 
        return dvrObjects, camaraObjects
    
    def manageScheduleLoop(self):
        while True:
            tiempoActual = datetime.now().time()

            for camara in self.camaraObjects.values():
                if camara.horarioInicio <= tiempoActual <= camara.horarioFin:
                    if camara.vigilanciaActiva != True:
                        camara.vigilanciaActiva = True
                        print(f"id: {camara.camaraId}, activa: {camara.vigilanciaActiva}")
                        #self.DataBase.ActualizarVigilanciaActiva(True)
                else:
                    if camara.vigilanciaActiva != False:
                        camara.vigilanciaActiva = False
                        print(f"id: {camara.camaraId}, activa: {camara.vigilanciaActiva}")
                        #self.DataBase.ActualizarVigilanciaActiva(False)
            sleep(5)
            print("_", tiempoActual)
    
    def mainSetup(self):
        self.raspberryIp, self.raspberryPuerto = self.DataBase.ConsultarDatosRaspberry("Clave del Dispositivo")
        #self.Raspberry = ClienteTCP(self.raspberryIp, self.raspberryPuerto)
        
        dvrs = self.DataBase.ConsultarDvrs()

        camaras = self.DataBase.ConsultarCamaras()
        
        self.dvrObjects, self.camaraObjects = self.InicializarDispositivos(dvrs, camaras)
        
        keys_to_omit = ["canal", "horarioInicio","horarioFin", "ip", "puerto", "usuario", "contrasena"]

        cameraData = {
            outer_key: {inner_key: value for inner_key, value in inner_dict.items() if inner_key not in keys_to_omit}
            for outer_key, inner_dict in camaras.items()
            }
        
        dvrData = {
            outer_key: {inner_key: value for inner_key, value in inner_dict.items() if inner_key not in keys_to_omit}
            for outer_key, inner_dict in dvrs.items()
            }

        configDict = {"tipo": "configuracion"}
        dispositivos = {**configDict, **dvrData, **cameraData}

        """
        sended = self.Raspberry.EnviarData(dispositivos)
        if not sended:
            print("No se pudo enviar lista de dispositivos")
            return
        print("sended: ",dispositivos)
        data = self.Raspberry.ConvertToDict("conexion", "1", True)
        self.Raspberry.EnviarData(data)

        """
        self.observers = {}
        manageSchedule = threading.Thread(target=self.manageScheduleLoop)
        manageSchedule.daemon = True
        manageSchedule.start()
        manageSchedule.join()
        #self.mainLoop()
        
                    
    def mainLoop(self):
        dvrDesconectado = set()
        camaraDesconectada = set()
        while True:
            for dvr in self.dvrObjects.values():
                connected = self.CheckDVRConnection(dvr.ip)
                
                if not connected :
                    if dvr.dvrId not in dvrDesconectado:
                        dvr.active = False
                        data = self.Raspberry.ConvertToDict("conexion", dvr.dvrId, dvr.active)
                        self.Raspberry.EnviarData(data)
                        dvrDesconectado.add(dvr.dvrId)
                else:
                    if connected and dvr.dvrId in dvrDesconectado:
                        dvr.active = True
                        data = self.Raspberry.ConvertToDict("conexion", dvr.dvrId, dvr.active)
                        self.Raspberry.EnviarData()
                        dvrDesconectado.remove(dvr.dvrId)

            for camara in self.camaraObjects.values():
                camara.CheckCameraConnection()
                
                if not camara.active:
                    if camara.camaraId not in camaraDesconectada:
                        camara.active = False
                        data = self.Raspberry.ConvertToDict("conexion", camara.camaraId, dvr.active)
                        self.Raspberry.EnviarData(data)
                        camaraDesconectada.add(camara.camaraId)
                    continue
                else:
                    if camara.camaraId in camaraDesconectada:
                        camara.active = True
                        data = self.Raspberry.ConvertToDict("conexion", camara.camaraId, dvr.active)
                        self.Raspberry.EnviarData(data)
                        camaraDesconectada.remove(camara.camaraId)
                        
                tiempoActual = datetime.now().time()
                if camara.vigilanciaActiva:
                    if not camara.running:
                        self.startProcess(camara)
                else:
                    if camara.running:
                        self.stopProcess(camara)
                    
    def startProcess(self, camara):
        try:
            with mp.Manager() as manager:
                sharedValue = manager.namespace()
                sharedValue.running = camara.running
                cam = Observer(sharedValue, self.DataBase, self.raspberryIp, self.raspberryPuerto, camara.camaraIp, camara.camaraId)
                cam.start()
                self.observers[camara.camaraId] = cam
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.DataBase.NewTask(camara.camaraId, camara.nombre, timestamp)
        except ErrorStartingProcess as e:
            print("ErrorStartingProcess:", e)
        
    def stopProcess(self, camara):
        try:
            cam = self.observers[camara.camaraId]
            cam.stop()
            cam.join()
            del self.observers[camara.camaraId]
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.DataBase.EndTask(camara.camaraId, timestamp)
        except NoProcessToStop as e:
            print("NoProcessToStop", e)


if __name__=="__main__":
    app = WatchMen()
    app.mainSetup()
    cv2.waitKey(0)
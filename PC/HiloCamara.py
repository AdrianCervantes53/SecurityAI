import cv2
import multiprocessing as mp
from ultralytics import YOLO
import datetime
import time
import signal
import sys

from TransferenciaRaspberry.ConexionRaspberry import ClienteTCP

class Observer(mp.Process):
    def __init__(self, DataBase, ip, puerto, cameraIp, cameraId):
        super().__init__()
        self.DataBase = DataBase
        #self.Raspberry = ClienteTCP(ip, puerto)
        self.cameraIp = cameraIp
        self.cameraId = cameraId
        self.stopEvent = mp.Event()
        
    def run(self):
        
        model = YOLO('Modelos/yolov8n.pt')
        cap = cv2.VideoCapture(self.cameraIp)
        print("framed")
        ret , firstFrame = cap.read()
        ret , firstFrame = cap.read()
        if not ret :
            print("ay")
        
        firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
        firstFrameGray = cv2.GaussianBlur(firstFrameGray, (21, 21), 0)
        cooldown = False
        cooldownTime = 0
        while not self.stopEvent.is_set() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            if cooldown:
                cooldown = False if time.time() - cooldownTime > 10 else True
            else:
                """ gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # Calcular la diferencia absoluta entre el primer fotograma y el actual
                frame_delta = cv2.absdiff(firstFrameGray, gray)
                thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

                # Dilatar la imagen umbral para llenar los agujeros y encontrar contornos
                thresh = cv2.dilate(thresh, None, iterations=2)
                contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Verificar si hay contornos significativos
                motion_detected = False
                for contour in contours:
                    if cv2.contourArea(contour) > 800:  # Ajusta el tama�o m�nimo del �rea del contorno
                        motion_detected = True
                        break

                if motion_detected:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #print(f"movimiento - {self.cameraId}")
                    #data = self.Raspberry.ConvertToDict("deteccion", self.camaraId, "Movimiento")
                    #self.Raspberry.EnviarData(data)
                    #self.DataBase.InsertarSituacion("deteccion", self.camaraId, timestamp) """

                # Realiza la inferencia
                results = model(frame, conf=0.4, verbose=False, classes=[0])
                if 0 in results[0].boxes.cls:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"persona - {self.cameraId}")
                    #data = self.Raspberry.ConvertToDict("deteccion", self.camaraId, "Persona")
                    #self.Raspberry.EnviarData(data)
                    #self.DataBase.InsertarSituacion("deteccion", self.camaraId, timestamp)

                    cooldown = True
                    cooldownTime = time.time()

                    res_plotted = results[0].plot()
                    cv2.imshow(f"test {self.cameraId}", res_plotted)
                    cv2.waitKey(1)
                #first_frame_gray = gray
    
        cap.release()
        self.stop()
        
    def stop(self):
        self.stopEvent.set()


if __name__ == "__main__":
    channels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    cameraNames = [
    "PTZ PATIO GPA",
    "AREA COMUN ATG B",
    "MAQUINA 3D",
    "IMPRESION 3D", 
    "AV OLIMPICA",
    "AREA COMUN ATG A",
    "OFICINA CIM",
    "PATIO GPA",
    "ALMACEN CIM",
    "ALMACEN 2 CIM"
    ]
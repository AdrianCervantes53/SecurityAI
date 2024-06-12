import cv2
import multiprocessing as mp
from ultralytics import YOLO
import datetime
import signal
import sys

from TransferenciaRaspberry.ConexionRaspberry import ClienteTCP

class Observer(mp.Process):
    def __init__(self, sharedValue, DataBase, ip, puerto, cameraIp, cameraId):
        super().__init__()
        self.sharedValue = sharedValue
        self.DataBase = DataBase
        self.Raspberry = ClienteTCP(ip, puerto)
        self.cameraIp = cameraIp
        self.cameraId = cameraId
        self.stopEvent = mp.Event()
        
    def run(self):
        
        self.sharedValue.running = True
        model = YOLO('Modelos/yolov8n.pt')
        cap = cv2.VideoCapture(self.cameraIp)
        
        ret , firstFrame = cap.read()
        if not ret :
            return
        
        firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
        firstFrameGray = cv2.GaussianBlur(firstFrameGray, (21, 21), 0)

        while not self.stopEvent.is_set() and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Calcular la diferencia absoluta entre el primer fotograma y el actual
            frame_delta = cv2.absdiff(first_frame_gray, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

            # Dilatar la imagen umbral para llenar los agujeros y encontrar contornos
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Verificar si hay contornos significativos
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Ajusta el tamaño mínimo del área del contorno
                    motion_detected = True
                    break

            if motion_detected:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = self.Raspberry.ConvertToDict("movimiento", self.camaraId, True)
                self.Raspberry.EnviarData(data)
                #self.DataBase.InsertarSituacion("movimiento", self.camaraId, timestamp)

            # Realiza la inferencia
            results = model(frame, conf=0.7, verbose=False, classes=[0])
            if 0 in results[0].boxes.cls:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = self.Raspberry.ConvertToDict("persona", self.camaraId, True)
                self.Raspberry.EnviarData(data)
                #self.DataBase.InsertarSituacion("persona", self.camaraId, timestamp)


            first_frame_gray = gray
    
        cap.release()
        self.sharedValue.running = False
        
    def stop(self):
        self.stopEvent.set()


if __name__ == "__main__":
    #channels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    channels = ["4", "5", "8"]
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
    cameraNames = [
    "IMPRESION 3D",
    "AV OLIMPICA",
    "PATIO GPA"
    ]

    output_queue = mp.Queue()
    stop_event = mp.Event()

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, stop_event))


    processes = []
    for channel, cameraName in zip(channels, cameraNames):
        p = mp.Process(target=process_frame, args=(channel, cameraName, output_queue, stop_event))
        p.start()
        processes.append(p)

    writer_process = mp.Process(target=write_results, args=(output_queue, stop_event, 'detections.txt'))
    writer_process.start()
    processes.append(writer_process)

    for p in processes:
        p.join()






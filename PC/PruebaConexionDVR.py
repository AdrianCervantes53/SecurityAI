import cv2
import multiprocessing as mp
from ultralytics import YOLO
import datetime
import signal
import sys

# Función para realizar la inferencia y guardar los resultados
def process_frame(channel, camera_name, output_queue, stop_event):
    model = YOLO('yolov8m.pt')  # Carga el modelo YOLOv8
    cap = cv2.VideoCapture(f"rtsp://admin:1111@192.168.1.38:554/cam/realmonitor?channel={channel}&subtype=1")

    ret, first_frame = cap.read()
    if not ret:
        print(f"Error al capturar el primer fotograma de {camera_name}")
        return

    first_frame_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_frame_gray = cv2.GaussianBlur(first_frame_gray, (21, 21), 0)

    while not stop_event.is_set() and cap.isOpened():
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
            #output_queue.put((camera_name, timestamp))
            print(f"Movimiento en {camera_name}, a las {timestamp}")

        # Realiza la inferencia
        results = model(frame, conf=0.7, verbose=False, classes=[0])
        if 0 in results[0].boxes.cls:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Deteccion en {camera_name}, a las {timestamp}")
            #output_queue.put((camera_name, timestamp))
            """ res = results[0].plot(labels=True)
            cv2.imshow("deteccion", res)
            cv2.waitKey(1) """

        first_frame_gray = gray
    
    cap.release()

# Función para escribir los resultados en un archivo txt
def write_results(output_queue, stop_event, file_path):
    with open(file_path, 'w') as f:
        while not stop_event.is_set() or not output_queue.empty():
            if not output_queue.empty():
                camera_name, timestamp = output_queue.get()
                f.write(f'Detected person in {camera_name} at {timestamp}\n')
                f.flush()

def signal_handler(sig, frame, stop_event):
    print('Interrupt received, stopping...')
    stop_event.set()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #channels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    channels = ["4", "5", "8"]
    cameraNames = [
    "PTZ PATIO GPA",
    "AREA COMUN ATG B",
    "MAQUINA 3D",
    "IMPRESIÓN 3D", 
    "AV OLIMPICA",
    "AREA COMUN ATG A",
    "OFICINA CIM",
    "PATIO GPA",
    "ALMACEN CIM",
    "ALMACEN 2 CIM"
    ]
    cameraNames = [
    "IMPRESIÓN 3D",
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







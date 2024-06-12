import cv2

class Camara:
    def __init__(self, camaraId, dvrId, nombre, canal, horarioInicio, horarioFin):
        self._camaraIp = None
        self._camaraId = camaraId
        self._dvrId = dvrId
        self._nombre = nombre
        self._canal = canal
        self._horarioInicio = horarioInicio
        self._horarioFin = horarioFin
        self._vigilanciaActiva = False
        self._running = False
        self._active = False
        
    def __repr__(self): return f'Camara({self._nombre}, {self._camaraId}, {self._dvrId})'

    def CheckCameraConnection(self) -> None:
        try:
            cap = cv2.VideoCapture(self.camaraIp)
            if cap.isOpened():
                self.active= True
        except Exception as e:
            print(f"Error: {e}")
            self.active= False
            
    @property
    def camaraIp(self): return self._camaraIp
    @camaraIp.setter
    def camaraIp(self, valor): self._camaraIp = valor

    @property
    def camaraId(self): return self._camaraId

    @property
    def dvrId(self): return self._dvrId

    @property
    def nombre(self): return self._nombre

    @property
    def canal(self): return self._canal

    @property
    def horarioInicio(self): return self._horarioInicio
    @horarioInicio.setter
    def horarioInicio(self, valor): self._horarioInicio = valor

    @property
    def horarioFin(self): return self._horarioFin
    @horarioFin.setter
    def horarioFin(self, valor): self._horarioFin = valor

    @property
    def vigilanciaActiva(self): return self._vigilanciaActiva
    @vigilanciaActiva.setter
    def vigilanciaActiva(self, valor): self._vigilanciaActiva = valor

    @property
    def vigilanciaActiva(self): return self._vigilanciaActiva
    @vigilanciaActiva.setter
    def vigilanciaActiva(self, valor): self._vigilanciaActiva = valor
    
    @property
    def running(self): return self._running
    @running.setter
    def running(self, valor): self._running = valor

    @property
    def active(self): return self._active
    @active.setter
    def active(self, valor): self._active = valor





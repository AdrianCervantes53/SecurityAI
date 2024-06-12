import requests

class DVR:
    def __init__(self, dvrIp, dvrId, nombre, puerto, usuario, contrasena):
        self._dvrIp = dvrIp
        self._dvrId = dvrId
        self._nombre = nombre
        self._puerto = puerto
        self._usuario = usuario
        self._contrasena = contrasena
        self._active = False
        
    def __repr__(self): return f'DVR({self._nombre}, {self._dvrId})'
        
    def CheckDVRConnection(self) -> None:
        try:
            response = requests.get(f"http://{self._dvrIp}")
            if response.status_code == 200:
                self.active= True
        except Exception as e:
            print(f"Error: {e}")
            self.active= False
            
    @property
    def dvrIp(self): return self._dvrIp

    @property
    def dvrId(self): return self._dvrId

    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, nuevo_nombre): self._nombre = nuevo_nombre

    @property
    def puerto(self): return self._puerto

    @property
    def usuario(self): return self._usuario

    @property
    def contrasena(self): return self._contrasena

    @property
    def active(self): return self._active
    @active.setter
    def active(self, nuevo_active): self._active = nuevo_active





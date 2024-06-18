import pyodbc
import datetime


class ConexionDB:
    def __init__(self,Datos):
        self.Datos=Datos
        #self.connect()
    
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.Datos["nameServer"]};'
                f'DATABASE={self.Datos["nameDB"]};'
                f'UID={self.Datos["User"]};'
                f'PWD={self.Datos["Pwd"]}'
            )
            print("Conexion exitosa a la base de datos.")
        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    
    def execute(self, proc_name, params):
        try:
            cursor = self.connection.cursor()
            placeholders = ','.join(['?' for _ in params])
            query = f"EXEC {proc_name} {placeholders}"
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as e:
            print(f"Error al ejecutar el procedimiento almacenado: {e}")
            return None
    
    def executeNoReturn(self, proc_name, params):
        try:
            cursor = self.connection.cursor()
            placeholders = ','.join(['?' for _ in params])
            query = f"EXEC {proc_name} {placeholders}"
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            print("Procedimiento almacenado ejecutado con exito.")
        except pyodbc.Error as e:
            print(f"Error al ejecutar el procedimiento almacenado: {e}")
    
    def executeNoParams(self, proc_name):
        try:
            cursor = self.connection.cursor()
            query = f"EXEC {proc_name}"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as e:
            print(f"Error al ejecutar el procedimiento almacenado: {e}")
            return None
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexion cerrada.")
    
    def ConsultarDatosRaspberry(self, *args):
        #return self.execute("PA_Name", args)
        #return '26.114.167.197', 1053
        return '26.174.164.42', 1053
    
    def ConsultarDvrs(self, *args):
        #return self.execute("PA", *args)
        dvrs = {
            "1": {
                "id": "1",
                "nombre": "DVR PARQUE ATG",
                "ip": "192.168.1.38",
                "puerto": "554",
                "usuario": "admin",
                "contrasena": "1111"
                },  
            }
        return dvrs
    
    def ConsultarCamaras(self, *args):
        #return self.execute("PA", *args)
        hi = 10
        hf = 11
        camaras = {
            "3": {
                "iddvr": "1",
                "id": "3",
                "nombre": "PTZ Patio GPA",
                "canal": "1",
                "horarioInicio": datetime.time(hi, 50, 0),
                "horarioFin": datetime.time(hf, 10, 0),
                },
            "4": {
                "iddvr": "1",
                "id": "4",
                "nombre": "Area Comun ATG B",
                "canal": "2",
                "horarioInicio": datetime.time(hi, 58, 0),
                "horarioFin": datetime.time(hf, 4, 0),
                },
            "5": {
                "iddvr": "1",
                "id": "5",
                "nombre": "Maquina 3D",
                "canal": "3",
                "horarioInicio": datetime.time(hi, 59, 0),
                "horarioFin": datetime.time(hf, 5, 10),
                },
            "6": {
                "iddvr": "1",
                "id": "6",
                "nombre": "Av Olimpica A",
                "canal": "5",
                "horarioInicio": datetime.time(hi, 59, 0),
                "horarioFin": datetime.time(hf, 5, 0),
                },
            "7": {
                "iddvr": "1",
                "id": "7",
                "nombre": "Av Olimpica B",
                "canal": "11",
                "horarioInicio": datetime.time(hi, 59, 0),
                "horarioFin": datetime.time(hf, 15, 0),
                }
        }

        return camaras
    
    
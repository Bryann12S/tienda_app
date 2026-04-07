import json
import os

class Database:
    def __init__(self, path="data/data.json"):
        self.path = path
        self._crear_archivo_si_no_existe()
        
    def _crear_archivo_si_no_existe(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"productos": []},f,indent=4)
    
    def leer_datos(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {"productos": [], "ventas": [], "gastos": [], "deudores": []}
        
    def guardar_datos(self, datos):
        with open(self.path, "w") as f:
            json.dump(datos, f, indent=4)
    
    def obtener_productos(self):
        datos = self.leer_datos()
        return datos.get("productos", [])
    
    def guardar_productos(self, productos):
        datos= self.leer_datos()
        datos["productos"] = productos
        self.guardar_datos(datos)

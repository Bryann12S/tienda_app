from models.gasto import Gasto
import json
import os
from datetime import datetime

class GastoController:

    def __init__(self, archivo="data/data.json"):
        self.archivo = archivo
    
    def crear_gasto(self, descripcion, monto):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos = json.load(f)
        else:
            datos = {"productos": [], "ventas": [], "gastos": [], "deudores": []}

        gastos = datos.get("gastos", [])
        
        nuevo_id = len(gastos) + 1

        gasto = Gasto(
            nuevo_id,
            descripcion,
            monto,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        gastos.append(gasto.to_dict())

        datos["gastos"] = gastos

        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)

        print("✅ Gasto creado exitosamente")
    
    def listar_gastos(self):
        with open(self.archivo, "r") as f:
            datos = json.load(f)

        gastos = datos.get("gastos", [])

        if not gastos:
            print("No hay gastos registrados")
            return
        
        for g in gastos:
            print(f"{g['id']} - {g['descripcion']} - ${g['monto']} - {g['fecha']}")
            print("--------------------")
    
    def calcular_balance(self):

        with open(self.archivo, "r") as f:
            datos = json.load(f)
        
        ventas = datos.get("ventas", [])
        gastos = datos.get("gastos", [])

        total_ganancias = 0
        total_gastos = 0

        #ganancias
        for v in ventas:
            for item in v["items"]:
                ganancia = (item["precio_venta"] - item["precio_compra"]) * item["cantidad"]
                total_ganancias += ganancia
        #ventas
        for g in gastos:
            total_gastos += g["monto"]

        balance = total_ganancias - total_gastos

        print(f"💰 Ganancias: {total_ganancias}")
        print(f"💸 Gastos: {total_gastos}")
        print(f"📊 Balance: {balance}")
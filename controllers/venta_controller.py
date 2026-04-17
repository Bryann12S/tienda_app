from models.venta import Venta, ItemVenta
from controllers.producto_controller import ProductoController 
import json
import os
from datetime import datetime

class VentaController:
    def __init__(self, archivo="data/data.json"):

        self.archivo = archivo 
        self.producto_controller = ProductoController()

    def cargar_datos(self):
        datos = {"productos":[], "ventas":[], "gastos":[], "deudores": []}
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos.update(json.load(f))
        return datos
    
    def guardar_datos(self, datos):
        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)


    def _generar_id(self):
        datos = self.cargar_datos()

        ventas = datos.get("ventas", [])

        if not ventas: 
            return 1

        ultimo_id = max(v["id"] for v in ventas)

        return ultimo_id + 1

    def crear_venta(self, items_data):
        datos = self.cargar_datos()

        items = []

        for item in items_data:
            producto = self.producto_controller.buscar_producto_por_id(item["id"])

            if not producto:
                print("❌ Producto no encontrado")
                return
            
            if not producto.activo:
                print("❌ Producto inactivo")
                return
            
            if producto.stock < item["cantidad"]:
                print(f"❌ Stock insuficiente para {producto.nombre}")
                return
            
            #crear Itemventa
            item_venta = ItemVenta(
                producto.id,
                producto.nombre,
                producto.precio_venta,
                producto.precio_compra,
                item["cantidad"]
            )

            items.append(item_venta)
        
        #crear venta
        venta = Venta(
            self._generar_id(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            items   
        )

        #Actualizar stock
        for item in items:
            producto = self.producto_controller.buscar_producto_por_id(item.producto_id)
            producto.stock -= item.cantidad
            self.producto_controller.actualizar_producto(producto)

        #guardar datos
        datos["ventas"].append(venta.to_dict())
        self.guardar_datos(datos)

        print("✅ Venta creada exitosamente")

    def obtener_ventas(self):
        datos = self.cargar_datos()
        return datos.get("ventas", [])
    
    def calcular_ganancia_total(self):
        datos = self.cargar_datos()

        ventas = datos.get("ventas", [])

        total = 0

        for v in ventas:

            for item in v["items"]:
                ganancia = (item["precio_venta"] - item["precio_compra"]) * item["cantidad"]
                total += ganancia

        print(f"Ganancia total: {total}")

    def ganancia_por_dia(self, fecha_busqueda):
        datos = self.cargar_datos()

        ventas = datos.get("ventas", [])

        total = 0

        for v in ventas: 
            fecha_venta = v["fecha"].split(" ")[0] #quitamos la hora

            if fecha_venta == fecha_busqueda:
                for item in v["items"]:
                    ganancia = (item["precio_venta"] - item["precio_compra"]) * item["cantidad"]
                    total += ganancia
            
            print(f"💰 Ganancia del dia {fecha_busqueda}: {total}")

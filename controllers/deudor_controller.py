from models.deudor import Deudor
from models.venta import ItemVenta
from controllers.producto_controller import ProductoController
import json
import os
from datetime import datetime

class DeudorController:
    def __init__(self, archivo="data/data.json"):
        self.archivo = archivo
        self.producto_controller = ProductoController()

    def crear_fiado(self, nombre_cliente, items_data, fecha_limite=None):

        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos = json.load(f)
        else:
            datos = {"productos": [], "ventas": [], "gastos": [], "deudores": []}

        items = []
        total = 0

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
            total += item_venta.calcular_subtotal()
        
        deudor = Deudor(
            id = len(datos.get("deudores", [])) + 1,
            nombre = nombre_cliente,
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            items = items,
            total = total,
            estado = "pendiente",
            abonado = 0.0,
            fecha_limite = fecha_limite
        )

        #Actualizar stock
        for item in items:
            producto = self.producto_controller.buscar_producto_por_id(item.producto_id)
            producto.stock -= item.cantidad
            self.producto_controller.actualizar_producto(producto)

        datos["deudores"].append(deudor.to_dict())

        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)

        print("✅ Fiado creado exitosamente")
    
    def abonar_a_deuda(self, id_deudor, monto_abono):
        if not os.path.exists(self.archivo):
            return False, "No hay datos"

        with open(self.archivo, "r") as f:
            datos = json.load(f)
        deudores = datos.get("deudores", [])

        encontrado = False
        for d in deudores:
            if d.get("id") == id_deudor:
                encontrado = True
                estado = d.get("estado", "pendiente")
                if estado == "pagado":
                    return False, "La deuda ya está totalmente pagada."
                
                abonado_actual = d.get("abonado", 0.0)
                total = d.get("total", 0.0)
                
                nuevo_abonado = abonado_actual + monto_abono
                if nuevo_abonado >= total:
                    d["abonado"] = total
                    d["estado"] = "pagado"
                else:
                    d["abonado"] = nuevo_abonado
                break
        
        if not encontrado:
            return False, "Deudor no encontrado"

        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)
        
        return True, "Abono registrado exitosamente"

    def marcar_como_pagado(self, id_deudor):
        if not os.path.exists(self.archivo):
            return False, "No hay datos"

        with open(self.archivo, "r") as f:
            datos = json.load(f)
        deudores = datos.get("deudores", [])

        encontrado = False
        for d in deudores:
            if d["id"] == id_deudor:
                encontrado = True
                if d.get("estado", "pendiente") == "pagado":
                    return False, "La deuda ya figura como pagada"
                d["estado"] = "pagado"
                d["abonado"] = d.get("total", 0.0)
                break
        
        if not encontrado:
            return False, "Deudor no encontrado"

        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)
        
        return True, "Deuda marcada como pagada"
    
    def obtener_deudores(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos = json.load(f)
            return datos.get("deudores", [])
        return []

    def listar_deuddas_pendientes(self):
        deudores = self.obtener_deudores()
        return [d for d in deudores if d.get("estado", "pendiente") == "pendiente"]
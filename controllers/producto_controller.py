from models.producto import Producto
from models.database import Database

class ProductoController:
    def __init__(self):
        self.db = Database()

    def crear_producto(self, nombre, precio_compra, precio_venta, stock):
        
        id = self._generar_id()

        producto = Producto(
            id, 
            nombre, 
            precio_compra, 
            precio_venta, 
            stock)

        productos = self.db.obtener_productos()

        productos.append(producto.to_dict())

        self.db.guardar_productos(productos)

    def listar_productos(self):
        productos_data = self.db.obtener_productos()

        productos = []

        for data in productos_data:
            if data.get("activo", True):
                producto = Producto.from_dict(data)
                productos.append(producto)

        return productos
    
    def _generar_id(self):
        productos_data = self.db.obtener_productos()
        if not productos_data:
            return 1
        
        ultimo_id = max(p["id"] for p in productos_data)

        return ultimo_id + 1

    def buscar_producto_por_id(self, id):
        
        productos = self.db.obtener_productos()

        for p in productos:
            if p["id"] == id:
                return Producto.from_dict(p)
        return None
    
    def actualizar_producto(self, producto_actualizado):        
        productos = self.db.obtener_productos()
        
        for i, p in enumerate(productos):

            if p["id"] == producto_actualizado.id:    
                
                productos[i] = producto_actualizado.to_dict()

                break

        self.db.guardar_productos(productos)

    def desactivar_producto(self, id_producto):
        productos = self.db.obtener_productos()

        for p in productos:
            
            if p["id"] == id_producto:
                p["activo"] = False
                break

        self.db.guardar_productos(productos)

    def vender_producto(self, id_producto, cantidad):
        producto = self.buscar_producto_por_id(id_producto)

        if not producto:
            print("Producto no encontrado")
            return
        
        if not producto.activo:
            print("Producto desactivado")
            return

        if not producto.stock:
            print("Stock insuficiente")
            return
        
        producto.stock -= cantidad

        self.actualizar_producto(producto)

        print("Venta realizada")
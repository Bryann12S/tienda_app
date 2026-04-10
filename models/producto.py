class Producto:
    def __init__(self, id, nombre, precio_compra, precio_venta, stock, activo=True):
        self.id = id
        self.nombre = nombre
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.activo = activo

    def actualizar_stock(self, cantidad):
        self.stock += cantidad

    def reducir_stock(self, cantidad):
        if cantidad > self.stock:
            raise ValueError("Stock insuficiente")
        self.stock -= cantidad

    def to_dict(self):
        return {
            "id":self.id,
            "nombre":self.nombre,
            "precio_compra":self.precio_compra,
            "precio_venta":self.precio_venta,
            "stock":self.stock,
            "activo":self.activo
        }
    @staticmethod
    def from_dict(data):
        return Producto(
            data["id"],
            data["nombre"],
            data["precio_compra"],
            data["precio_venta"],
            data["stock"],
            data.get("activo", True)
        )
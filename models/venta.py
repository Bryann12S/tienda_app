class ItemVenta:
    def __init__(self, producto_id, nombre, precio_venta, precio_compra, cantidad):

        self.producto_id = producto_id
        self.nombre = nombre
        self.precio_venta = precio_venta
        self.precio_compra = precio_compra
        self.cantidad = cantidad
    
    def calcular_subtotal (self):
        return self.precio_venta * self.cantidad

    def calcular_ganancia(self):
        return (self.precio_venta - self.precio_compra) * self.cantidad
    
    def to_dict(self):
        return {
            "producto_id":self.producto_id,
            "nombre":self.nombre,
            "precio":self.precio_venta,
            "precio_compra":self.precio_compra,
            "cantidad":self.cantidad,
            "subtotal":self.calcular_subtotal()
        }
        


class Venta:

    def __init__(self, id, fecha, items):

        self.id = id
        self.fecha = fecha
        self.items = items

    def calcular_total(self):
        total = 0

        for item in self.items:
            total += item.calcular_subtotal()

        return total

    def calcular_ganancia(self):
        ganancia = 0

        for item in self.items:
            ganancia += item.calcular_ganancia()

        return ganancia
    
    def to_dict(self):

        return {
            "id":self.id,
            "fecha":self.fecha,
            "items":[item.to_dict() for item in self.items],
            "total":self.calcular_total()
        }
    
class ItemVenta:
    def __init__(self, producto_id, nombre, precio, cantidad):

        self.producto_id = producto_id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
    
    def calcular_subtotal (self):
        return self.precio * self.cantidad
    
    def to_dict(self):
        return {
            "producto_id":self.producto_id,
            "nombre":self.nombre,
            "precio":self.precio,
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
            total += item.cacular_suntotal()

        return total
    
    def to_dict(self):

        return {
            "id":self.id,
            "fecha":self.fecha,
            "items":[item.to_dict() for item in self.items],
            "total":self.cacular_total()
        }
    
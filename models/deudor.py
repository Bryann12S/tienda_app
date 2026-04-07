class Deudor:
    def __init__(self, id, nombre, fecha, items, total, estado="pendiente"):

        self.id = id
        self.nombre = nombre
        self.fecha = fecha
        self.items = items
        self.total = total
        self.estado = estado

    def to_dict(self):

        return {
            "id":self.id,
            "nombre":self.nombre,
            "fecha":self.fecha,
            "items":[item.to_dict() for item in self.items],
            "total":self.total,
            "estado":self.estado
        }

    
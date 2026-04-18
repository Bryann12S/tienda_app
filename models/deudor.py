class Deudor:
    def __init__(self, id, nombre, fecha, items, total, estado="pendiente", abonado=0.0, fecha_limite=None):

        self.id = id
        self.nombre = nombre
        self.fecha = fecha
        self.items = items
        self.total = total
        self.estado = estado
        self.abonado = abonado
        self.fecha_limite = fecha_limite

    def to_dict(self):

        return {
            "id":self.id,
            "nombre":self.nombre,
            "fecha":self.fecha,
            "items":[item.to_dict() for item in self.items],
            "total":self.total,
            "estado":self.estado,
            "abonado": self.abonado,
            "fecha_limite": self.fecha_limite
        }

    
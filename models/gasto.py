class Gasto:
    def __init__(self, id, descripcion, monto, fecha):
        self.id = id
        self.descripcion = descripcion
        self.monto = monto
        self.fecha = fecha

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "monto": self.monto,
            "fecha": self.fecha
        }

    

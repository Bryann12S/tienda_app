import tkinter as tk
from controllers.producto_controller import ProductoController

controller = ProductoController()

def abrir_producto_view():
    ventana = tk.Toplevel()
    ventana.title("Productos")

    tk.Label(ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Precio Compra").pack()
    entry_precio_compra = tk.Entry(ventana)
    entry_precio_compra.pack()

    tk.Label(ventana, text="Precio Venta").pack()
    entry_precio_venta = tk.Entry(ventana)
    entry_precio_venta.pack()

    tk.Label(ventana, text="Stock").pack()
    entry_stock = tk.Entry(ventana)
    entry_stock.pack()
    
    def agregar():
        controller.crear_producto(
            entry_nombre.get(),
            entry_precio_compra.get(),
            entry_precio_venta.get(),
            entry_stock.get()
        )
    
    tk.Button(ventana, text="Guardar", command=agregar).pack()

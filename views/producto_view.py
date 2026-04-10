import tkinter as tk
import tkinter.ttk as ttk
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
            float(entry_precio_compra.get()),
            float(entry_precio_venta.get()),
            int(entry_stock.get())
        )
        mostrar_productos()
    
    tk.Button(ventana, text="Guardar", command=agregar).pack()

    frame_lista = tk.Frame(ventana)
    frame_lista.pack()

    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
    
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio", text="Precio Venta")
    tabla.heading("Stock", text="Stock")

    tabla.pack()

    def mostrar_productos():

        #limpiar frame_lista
        for fila in tabla.get_children():
            tabla.delete(fila)

        productos = controller.listar_productos()

        for p in productos:
            tabla.insert("", "end", values=(
                p.id,
                p.nombre,
                p.precio_venta,
                p.stock
            ))

    tk.Button(ventana, text="Mostrar productos", command=mostrar_productos).pack()
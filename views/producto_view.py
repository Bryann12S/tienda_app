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
            float(entry_precio_compra.get()),
            float(entry_precio_venta.get()),
            int(entry_stock.get())
        )
    
    tk.Button(ventana, text="Guardar", command=agregar).pack()

    frame_lista = tk.Frame(ventana)
    frame_lista.pack()

    def mostrar_productos():
        
        productos = controller.listar_productos()
        
        for p in productos:
            print(p.nombre, p.stock) #prueba    

        #limpiar frame_lista
        for widget in frame_lista.winfo_children():
            widget.destroy()

        for p in productos:
            texto = f"{p.id} - {p.nombre} - Stock: {p.stock}"
            tk.Label(frame_lista, text=texto).pack()

    tk.Button(ventana, text="Mostrar productos", command=mostrar_productos).pack()
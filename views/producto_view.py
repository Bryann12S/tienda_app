import tkinter as tk
import tkinter.ttk as ttk
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController

controller_producto = ProductoController()
controller_venta = VentaController()

def abrir_producto_view():
    ventana = tk.Toplevel()
    ventana.title("Productos")

    id_editando = None

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

        nonlocal id_editando
        
        try:
            nombre = entry_nombre.get()
            precio_compra = float(entry_precio_compra.get())
            precio_venta = float(entry_precio_venta.get())
            stock = int(entry_stock.get())

        except:
            print("Datos inválidos")
            return

        if id_editando:
           
           producto = controller_producto.buscar_producto_por_id(id_editando)

           producto.nombre = entry_nombre.get()
           producto.precio_compra = float(entry_precio_compra.get())
           producto.precio_venta = float(entry_precio_venta.get())
           producto.stock = int(entry_stock.get())

           controller_producto.actualizar_producto(producto)
           
           id_editando = None

        else:
            controller_producto.crear_producto(
                entry_nombre.get(),
                float(entry_precio_compra.get()),
                float(entry_precio_venta.get()),
                int(entry_stock.get())
        )
        mostrar_productos()

        #limpiar campos
        entry_nombre.delete(0, tk.END)
        entry_precio_compra.delete(0, tk.END)
        entry_precio_venta.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
    
    tk.Button(ventana, text="Guardar", command=agregar).pack()


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

        productos = controller_producto.listar_productos()

        for p in productos:
            tabla.insert("", "end", values=(
                p.id,
                p.nombre,
                p.precio_venta,
                p.stock
            ))

    tk.Button(ventana, text="Mostrar productos", command=mostrar_productos).pack()

    def obtener_id_seleccionado():
        seleccion = tabla.selection()

        if not seleccion:
            print("No has seleccionado nada")
            return None

        item = tabla.item(seleccion[0])
        datos = item["values"]

        return datos[0] 

    def editar_producto():

        print("Editando....")

        id_producto = obtener_id_seleccionado()

        if not id_producto:
            return

        producto = controller_producto.buscar_producto_por_id(id_producto)

        nonlocal id_editando
        id_editando = id_producto

        #cargar datos entrys

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, producto.nombre)

        entry_precio_compra.delete(0, tk.END)
        entry_precio_compra.insert(0, producto.precio_compra)

        entry_precio_venta.delete(0, tk.END)
        entry_precio_venta.insert(0, producto.precio_venta)

        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, producto.stock)

    tk.Button(ventana, text="Editar", command=editar_producto).pack()

    def eliminar_producto():
        id_producto = obtener_id_seleccionado()

        if not id_producto:
            return

        controller_producto.desactivar_producto(id_producto)
        mostrar_productos()

    tk.Button(ventana, text="Eliminar", command=eliminar_producto).pack()


    tk.Label(ventana, text="Cantidad a vender").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    def vender_producto():
        id_producto = obtener_id_seleccionado()

        if not id_producto:
            return

        try:
            cantidad = int(entry_cantidad.get())
        except:
            print("Cantidad inválida")
            return

        producto = controller_producto.buscar_producto_por_id(id_producto)
        
        if producto.stock < cantidad:
            print("No hay stock suficiente")
            return

        #crear item de venta
        item = {
            "id": id_producto,
            "nombre": producto.nombre,
            "cantidad": cantidad,
            "precio_compra": producto.precio_compra,
            "precio_venta": producto.precio_venta
        }

        #registrar venta
        controller_venta.crear_venta([item])

        #bajar stock
        controller_producto.vender_producto(id_producto, cantidad)

        mostrar_productos()

    tk.Button(ventana, text="Vender", command=vender_producto).pack()

    mostrar_productos()

    ventana.mainloop()
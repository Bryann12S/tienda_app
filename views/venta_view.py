import tkinter as tk
from tkinter import ttk, messagebox
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController

producto_controller = ProductoController()
venta_controller = VentaController()

def abrir_venta_view():

    ventana = tk.Toplevel()
    ventana.title("Ventas")
    ventana.geometry("700x500")

    carrito = []

    # ========================
    # TABLA PRODUCTOS
    # ========================
    tabla_productos = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Precio", "Stock"),
        show="headings"
    )

    tabla_productos.heading("ID", text="ID")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Precio", text="Precio")
    tabla_productos.heading("Stock", text="Stock")

    tabla_productos.pack()

    # ========================
    # CARGAR PRODUCTOS
    # ========================
    def cargar_productos():

        for fila in tabla_productos.get_children():
            tabla_productos.delete(fila)

        productos = producto_controller.listar_productos()

        for p in productos:
            tabla_productos.insert("", "end", values=(
                p.id,
                p.nombre,
                p.precio_venta,
                p.stock
            ))

    # ========================
    # OBTENER PRODUCTO
    # ========================
    def obtener_producto_seleccionado():

        seleccion = tabla_productos.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return None

        item = tabla_productos.item(seleccion[0])
        datos = item["values"]

        return datos[0]  # ID

    # ========================
    # INPUT CANTIDAD
    # ========================
    tk.Label(ventana, text="Cantidad").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    # ========================
    # AGREGAR AL CARRITO
    # ========================
    def agregar_al_carrito():

        id_producto = obtener_producto_seleccionado()

        if not id_producto:
            return

        try:
            cantidad = int(entry_cantidad.get())
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        producto = producto_controller.buscar_producto_por_id(id_producto)

        if producto.stock < cantidad:
            messagebox.showerror("Error", "Stock insuficiente")
            return

        item = {
            "id": producto.id,
            "nombre": producto.nombre,
            "cantidad": cantidad,
            "precio_compra": producto.precio_compra,
            "precio_venta": producto.precio_venta
        }

        carrito.append(item)

        actualizar_carrito()

    tk.Button(ventana, text="Agregar al carrito", command=agregar_al_carrito).pack()

    # ========================
    # TABLA CARRITO
    # ========================
    tabla_carrito = ttk.Treeview(
        ventana,
        columns=("Nombre", "Cantidad", "Precio", "Subtotal"),
        show="headings"
    )

    tabla_carrito.heading("Nombre", text="Nombre")
    tabla_carrito.heading("Cantidad", text="Cantidad")
    tabla_carrito.heading("Precio", text="Precio")
    tabla_carrito.heading("Subtotal", text="Subtotal")

    tabla_carrito.pack()

    # ========================
    # TOTAL
    # ========================
    label_total = tk.Label(ventana, text="Total: $0")
    label_total.pack()

    # ========================
    # ACTUALIZAR CARRITO
    # ========================
    def actualizar_carrito():

        for fila in tabla_carrito.get_children():
            tabla_carrito.delete(fila)

        total = 0

        for item in carrito:

            subtotal = item["cantidad"] * item["precio_venta"]
            total += subtotal

            tabla_carrito.insert("", "end", values=(
                item["nombre"],
                item["cantidad"],
                item["precio_venta"],
                subtotal
            ))

        label_total.config(text=f"Total: ${total}")

    # ========================
    # CONFIRMAR VENTA
    # ========================
    def confirmar_venta():

        if not carrito:
            messagebox.showwarning("Aviso", "Carrito vacío")
            return

        # guardar venta
        venta_controller.crear_venta(carrito)

        # actualizar stock
        for item in carrito:
            producto_controller.vender_producto(item["id"], item["cantidad"])

        messagebox.showinfo("Éxito", "Venta realizada")

        carrito.clear()
        actualizar_carrito()
        cargar_productos()

    tk.Button(ventana, text="Confirmar venta", command=confirmar_venta).pack()

    # iniciar
    cargar_productos()
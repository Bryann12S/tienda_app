import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
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

        for item in carrito:
            if item["id"] == producto.id:
                if producto.stock < item["cantidad"] + cantidad:
                    messagebox.showerror("Error", "Stock insuficiente")
                    return
                item["cantidad"] += cantidad
                actualizar_carrito()
                return

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
    # ACCIONES DEL CARRITO
    # ========================
    def eliminar_del_carrito():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito")
            return
            
        indice = tabla_carrito.index(seleccion[0])
        carrito.pop(indice)
        actualizar_carrito()

    def aumentar_cantidad():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito")
            return
            
        indice = tabla_carrito.index(seleccion[0])
        item_carrito = carrito[indice]
        
        producto = producto_controller.buscar_producto_por_id(item_carrito["id"])
        if producto.stock <= item_carrito["cantidad"]:
            messagebox.showerror("Error", "Stock insuficiente")
            return
            
        item_carrito["cantidad"] += 1
        actualizar_carrito()

    def disminuir_cantidad():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del carrito")
            return
            
        indice = tabla_carrito.index(seleccion[0])
        item_carrito = carrito[indice]
        
        if item_carrito["cantidad"] > 1:
            item_carrito["cantidad"] -= 1
            actualizar_carrito()
        else:
            if messagebox.askyesno("Eliminar", "¿Deseas eliminar el producto del carrito?"):
                carrito.pop(indice)
                actualizar_carrito()

    frame_acciones_carrito = tk.Frame(ventana)
    frame_acciones_carrito.pack(pady=5)

    tk.Button(frame_acciones_carrito, text="➖ Disminuir", command=disminuir_cantidad).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_acciones_carrito, text="➕ Aumentar", command=aumentar_cantidad).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_acciones_carrito, text="Eliminar seleccionado", command=eliminar_del_carrito).pack(side=tk.LEFT, padx=5)

    # ========================
    # TOTAL, PAGO Y CAMBIO
    # ========================
    label_total = tk.Label(ventana, text="Total: $0")
    label_total.pack()

    frame_pago = tk.Frame(ventana)
    frame_pago.pack()
    
    tk.Label(frame_pago, text="Pago Cliente:").pack(side=tk.LEFT)
    entry_pago = tk.Entry(frame_pago)
    entry_pago.pack(side=tk.LEFT)
    
    label_cambio = tk.Label(ventana, text="Cambio: $0")
    label_cambio.pack()
    
    def calcular_cambio():
        total = sum((item["cantidad"] * item["precio_venta"]) for item in carrito)
        try:
            pago = float(entry_pago.get())
            if pago < total:
                messagebox.showerror("Error", "El pago es menor al total")
                return None
            cambio = pago - total
            label_cambio.config(text=f"Cambio: ${cambio:.2f}")
            return pago, cambio
        except ValueError:
            messagebox.showerror("Error", "Monto de pago inválido")
            return None

    tk.Button(ventana, text="Calcular Cambio", command=calcular_cambio).pack()

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

        resultado_pago = calcular_cambio()
        if not resultado_pago:
            return

        pago, cambio = resultado_pago
        total = sum((item["cantidad"] * item["precio_venta"]) for item in carrito)

        # guardar venta
        venta_controller.crear_venta(carrito)

        # generar ticket
        if not os.path.exists("tickets"):
            os.makedirs("tickets")
            
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_ticket = f"tickets/ticket_{fecha}.txt"
        
        with open(nombre_ticket, "w") as file:
            file.write("=== TICKET DE COMPRA ===\n")
            file.write(f"Fecha: {fecha}\n")
            file.write("-" * 25 + "\n")
            for item in carrito:
                subtotal = item['cantidad'] * item['precio_venta']
                file.write(f"{item['nombre']} x{item['cantidad']} - ${subtotal:.2f}\n")
            file.write("-" * 25 + "\n")
            file.write(f"Total: ${total:.2f}\n")
            file.write(f"Pago: ${pago:.2f}\n")
            file.write(f"Cambio: ${cambio:.2f}\n")
            file.write("========================\n")

        # actualizar stock
        for item in carrito:
            producto_controller.vender_producto(item["id"], item["cantidad"])

        messagebox.showinfo("Éxito", f"Venta realizada\nTicket generado: {nombre_ticket}")

        carrito.clear()
        actualizar_carrito()
        cargar_productos()
        entry_pago.delete(0, tk.END)
        label_cambio.config(text="Cambio: $0")

    tk.Button(ventana, text="Confirmar venta", command=confirmar_venta).pack()

    # iniciar
    cargar_productos()
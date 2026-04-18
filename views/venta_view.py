import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import os
from datetime import datetime
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from controllers.deudor_controller import DeudorController

producto_controller = ProductoController()
venta_controller = VentaController()
deudor_controller = DeudorController()

def abrir_venta_view(parent):
    ventana = parent
    carrito = []

    # Layout: Izquierda (Catálogo), Derecha (Carrito y Check-out)
    frame_izq = tb.LabelFrame(ventana, text="Catálogo de Productos")
    frame_izq.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    frame_der = tb.LabelFrame(ventana, text="Carrito de Compras y Facturación")
    frame_der.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    # ========================
    # IZQUIERDA: CATÁLOGO
    # ========================
    tabla_productos = tb.Treeview(frame_izq, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", bootstyle="primary")
    tabla_productos.heading("ID", text="ID")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Precio", text="Precio")
    tabla_productos.heading("Stock", text="Stock")
    tabla_productos.column("ID", width=50, anchor=CENTER)
    tabla_productos.column("Stock", width=80, anchor=CENTER)
    
    tabla_productos.pack(fill=BOTH, expand=True, pady=(0, 10))

    frame_agregar = tb.Frame(frame_izq)
    frame_agregar.pack(fill=X)

    tb.Label(frame_agregar, text="Cant:", font=("Arial", 12)).pack(side=LEFT, padx=5)
    entry_cantidad = tb.Entry(frame_agregar, width=10)
    entry_cantidad.pack(side=LEFT, padx=5)
    entry_cantidad.insert(0, "1")

    def obtener_producto_seleccionado():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del catálogo.")
            return None
        return tabla_productos.item(seleccion[0])["values"][0]

    def agregar_al_carrito():
        id_producto = obtener_producto_seleccionado()
        if not id_producto:
            return

        try:
            cantidad = int(entry_cantidad.get())
            if cantidad <= 0: raise ValueError
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

    tb.Button(frame_agregar, text="➕ Añadir al Carrito", command=agregar_al_carrito, bootstyle="success").pack(side=RIGHT, padx=5)

    # ========================
    # DERECHA: CARRITO
    # ========================
    tabla_carrito = tb.Treeview(frame_der, columns=("Nombre", "Cantidad", "Precio", "Subtotal"), show="headings", bootstyle="info")
    tabla_carrito.heading("Nombre", text="Nombre")
    tabla_carrito.heading("Cantidad", text="Cant.")
    tabla_carrito.heading("Precio", text="Precio Unit.")
    tabla_carrito.heading("Subtotal", text="Subtotal")
    tabla_carrito.column("Cantidad", width=60, anchor=CENTER)
    
    tabla_carrito.pack(fill=BOTH, expand=True, pady=(0, 10))

    frame_acciones_carrito = tb.Frame(frame_der)
    frame_acciones_carrito.pack(fill=X, pady=5)

    def modificar_cant(delta):
        seleccion = tabla_carrito.selection()
        if not seleccion: return
        indice = tabla_carrito.index(seleccion[0])
        item_carrito = carrito[indice]
        
        if delta > 0:
            producto = producto_controller.buscar_producto_por_id(item_carrito["id"])
            if producto.stock <= item_carrito["cantidad"]:
                messagebox.showerror("Error", "Stock insuficiente")
                return
            item_carrito["cantidad"] += 1
        else:
            if item_carrito["cantidad"] > 1:
                item_carrito["cantidad"] -= 1
            else:
                if messagebox.askyesno("Eliminar", "¿Eliminar del carrito?"):
                    carrito.pop(indice)
        actualizar_carrito()

    def eliminar_del_carrito():
        seleccion = tabla_carrito.selection()
        if not seleccion: return
        indice = tabla_carrito.index(seleccion[0])
        carrito.pop(indice)
        actualizar_carrito()

    tb.Button(frame_acciones_carrito, text="➖", command=lambda: modificar_cant(-1), bootstyle="secondary-outline").pack(side=LEFT, padx=2)
    tb.Button(frame_acciones_carrito, text="➕", command=lambda: modificar_cant(1), bootstyle="secondary-outline").pack(side=LEFT, padx=2)
    tb.Button(frame_acciones_carrito, text="🗑️ Quitar", command=eliminar_del_carrito, bootstyle="danger-outline").pack(side=LEFT, padx=10)

    # Panel Inferior Facturación
    panel_factura = tb.Frame(frame_der, bootstyle="light")
    panel_factura.pack(fill=X, pady=10)

    label_total = tb.Label(panel_factura, text="Total: $0.00", font=("Arial", 20, "bold"), bootstyle="inverse-primary")
    label_total.pack(fill=X, pady=5)

    frame_pago = tb.Frame(panel_factura)
    frame_pago.pack(fill=X, pady=5)
    tb.Label(frame_pago, text="Efectivo Recibido: $").pack(side=LEFT)
    entry_pago = tb.Entry(frame_pago, width=15)
    entry_pago.pack(side=LEFT, padx=5)

    def calcular_cambio():
        total = sum((i["cantidad"] * i["precio_venta"]) for i in carrito)
        try:
            pago = float(entry_pago.get())
            if pago < total:
                messagebox.showerror("Error", "El pago es menor al total")
                return None
            cambio = pago - total
            label_cambio.config(text=f"Cambio a Devolver: ${cambio:.2f}")
            return pago, cambio
        except ValueError:
            messagebox.showerror("Error", "Monto de pago inválido")
            return None

    btn_cambio = tb.Button(frame_pago, text="Calcular Cambio", command=calcular_cambio, bootstyle="info-outline")
    btn_cambio.pack(side=LEFT, padx=5)
    
    label_cambio = tb.Label(panel_factura, text="Cambio a Devolver: $0.00", font=("Arial", 12, "bold"), bootstyle="success")
    label_cambio.pack(pady=5)

    # ========================
    # FUNCIONES PRINCIPALES
    # ========================
    def cargar_productos():
        for fila in tabla_productos.get_children():
            tabla_productos.delete(fila)
        for p in producto_controller.listar_productos():
            tabla_productos.insert("", "end", values=(p.id, p.nombre, f"${p.precio_venta:.2f}", p.stock))

    def actualizar_carrito():
        for fila in tabla_carrito.get_children():
            tabla_carrito.delete(fila)
        total = 0
        for item in carrito:
            subt = item["cantidad"] * item["precio_venta"]
            total += subt
            tabla_carrito.insert("", "end", values=(item["nombre"], item["cantidad"], f"${item['precio_venta']:.2f}", f"${subt:.2f}"))
        label_total.config(text=f"Total: ${total:.2f}")

    def confirmar_venta():
        if not carrito:
            messagebox.showwarning("Aviso", "Carrito vacío")
            return
        total = sum((i["cantidad"] * i["precio_venta"]) for i in carrito)

        resultado_pago = calcular_cambio()
        if not resultado_pago: return
        pago, cambio = resultado_pago

        venta_controller.crear_venta(carrito)

        if not os.path.exists("tickets"): os.makedirs("tickets")
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_ticket = f"tickets/ticket_{fecha}.txt"
        with open(nombre_ticket, "w") as file:
            file.write("=== TICKET DE COMPRA ===\n")
            file.write(f"Fecha: {fecha}\n")
            file.write("-" * 25 + "\n")
            for item in carrito:
                subt = item['cantidad'] * item['precio_venta']
                file.write(f"{item['nombre']} x{item['cantidad']} - ${subt:.2f}\n")
            file.write("-" * 25 + "\n")
            file.write(f"Total: ${total:.2f}\n")
            file.write(f"Pago: ${pago:.2f}\n")
            file.write(f"Cambio: ${cambio:.2f}\n")
            file.write("========================\n")

        for item in carrito:
            producto_controller.vender_producto(item["id"], item["cantidad"])

        messagebox.showinfo("Éxito", f"Venta realizada\nTicket generado: {nombre_ticket}")
        carrito.clear()
        actualizar_carrito()
        cargar_productos()
        entry_pago.delete(0, END)
        label_cambio.config(text="Cambio a Devolver: $0.00")

    tb.Button(frame_der, text="✅ CONFIRMAR VENTA", bootstyle="success", command=confirmar_venta).pack(fill=X, pady=10)

    cargar_productos()
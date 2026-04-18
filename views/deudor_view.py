import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
from controllers.deudor_controller import DeudorController

deudor_controller = DeudorController()

def abrir_deudor_view(parent):
    ventana = parent

    # ========================
    # TABLA DEUDORES
    # ========================
    frame_tabla = tb.LabelFrame(ventana, text="Lista de Deudores")
    frame_tabla.pack(fill=BOTH, expand=True, padx=15, pady=10)

    tabla = tb.Treeview(
        frame_tabla,
        columns=("ID", "Nombre", "Fecha", "Total", "Estado"),
        show="headings",
        bootstyle="warning"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Cliente")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total")
    tabla.heading("Estado", text="Estado")

    tabla.column("ID", width=70, anchor=CENTER)
    tabla.column("Nombre", anchor=W)
    tabla.column("Fecha", anchor=CENTER)
    tabla.column("Total", width=120, anchor=E)
    tabla.column("Estado", width=120, anchor=CENTER)

    tabla.pack(fill=BOTH, expand=True)

    # ========================
    # DETALLE DE PRODUCTOS
    # ========================
    frame_detalle = tb.LabelFrame(ventana, text="Detalle de Productos Fiados")
    frame_detalle.pack(fill=BOTH, expand=True, padx=15, pady=5)

    tabla_detalle = tb.Treeview(
        frame_detalle,
        columns=("Nombre", "Cantidad", "Precio", "Subtotal"),
        show="headings",
        bootstyle="info"
    )

    tabla_detalle.heading("Nombre", text="Nombre")
    tabla_detalle.heading("Cantidad", text="Cantidad")
    tabla_detalle.heading("Precio", text="Precio Unit.")
    tabla_detalle.heading("Subtotal", text="Subtotal")
    
    tabla_detalle.column("Cantidad", anchor=CENTER)
    tabla_detalle.column("Precio", anchor=E)
    tabla_detalle.column("Subtotal", anchor=E)

    tabla_detalle.pack(fill=BOTH, expand=True)

    def cargar_datos():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        deudores = deudor_controller.obtener_deudores()
        for d in deudores:
            estado = d.get("estado", "pendiente")
            tabla.insert("", "end", values=(
                d["id"],
                d["nombre"],
                d["fecha"],
                f"${d['total']:.2f}",
                estado.upper()
            ))

    def mostrar_detalle(event):
        seleccion = tabla.selection()
        if not seleccion:
            return

        item = tabla.item(seleccion[0])
        id_deudor = item["values"][0]

        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        deudores = deudor_controller.obtener_deudores()
        for d in deudores:
            if d["id"] == id_deudor:
                for producto in d.get("items", []):
                    subtotal = producto["cantidad"] * producto["precio_venta"]
                    tabla_detalle.insert("", "end", values=(
                        producto["nombre"],
                        producto["cantidad"],
                        f"${producto['precio_venta']:.2f}",
                        f"${subtotal:.2f}"
                    ))
                break

    tabla.bind("<<TreeviewSelect>>", mostrar_detalle)

    # ========================
    # ACCIONES
    # ========================
    frame_acciones = tb.Frame(ventana)
    frame_acciones.pack(pady=10)

    def marcar_pagado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una cuenta de la lista primero")
            return
            
        item = tabla.item(seleccion[0])
        id_deudor = item["values"][0]
        estado = item["values"][4]
        
        if estado == "PAGADO":
            messagebox.showinfo("Aviso", "Esta cuenta ya ha sido pagada previamente.")
            return

        respuesta = messagebox.askyesno("Confirmar Pago", "¿Estás seguro de marcar esta deuda como pagada?")
        if respuesta:
            exito, mensaje = deudor_controller.marcar_como_pagado(id_deudor)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)

    tb.Button(frame_acciones, text="💲 Marcar como Pagado", bootstyle="success", command=marcar_pagado).pack(side=LEFT, padx=5)
    tb.Button(frame_acciones, text="🔄 Actualizar Lista", command=cargar_datos, bootstyle="secondary-outline").pack(side=LEFT, padx=5)

    cargar_datos()

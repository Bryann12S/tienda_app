import tkinter as tk
from tkinter import ttk, messagebox
from controllers.deudor_controller import DeudorController

deudor_controller = DeudorController()

def abrir_deudor_view():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Deudores (Fiados)")
    ventana.geometry("800x600")

    # ========================
    # TABLA DEUDORES
    # ========================
    frame_tabla = tk.LabelFrame(ventana, text="Lista de Deudores")
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("ID", "Nombre", "Fecha", "Total", "Estado"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Cliente")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total")
    tabla.heading("Estado", text="Estado")

    tabla.column("ID", width=50, anchor="center")
    tabla.column("Nombre", anchor="w")
    tabla.column("Fecha", anchor="center")
    tabla.column("Total", width=100, anchor="center")
    tabla.column("Estado", width=100, anchor="center")

    tabla.pack(fill="both", expand=True, padx=5, pady=5)

    # ========================
    # DETALLE DE PRODUCTOS
    # ========================
    frame_detalle = tk.LabelFrame(ventana, text="Detalle de Productos Fiados")
    frame_detalle.pack(fill="both", expand=True, padx=10, pady=5)

    tabla_detalle = ttk.Treeview(
        frame_detalle,
        columns=("Nombre", "Cantidad", "Precio", "Subtotal"),
        show="headings"
    )

    tabla_detalle.heading("Nombre", text="Nombre")
    tabla_detalle.heading("Cantidad", text="Cantidad")
    tabla_detalle.heading("Precio", text="Precio Unit.")
    tabla_detalle.heading("Subtotal", text="Subtotal")

    tabla_detalle.pack(fill="both", expand=True, padx=5, pady=5)

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
    frame_acciones = tk.Frame(ventana)
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

    tk.Button(frame_acciones, text="Marcar como Pagado", font=("Arial", 10, "bold"), fg="green", command=marcar_pagado).pack(side="left", padx=5)
    tk.Button(frame_acciones, text="Actualizar Lista", command=cargar_datos).pack(side="left", padx=5)

    cargar_datos()

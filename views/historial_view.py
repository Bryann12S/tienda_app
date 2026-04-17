import tkinter as tk
from tkinter import ttk
from controllers.venta_controller import VentaController

venta_controller = VentaController()

def abrir_historial_view():

    ventana = tk.Toplevel()
    ventana.title("Historial de Ventas")
    ventana.geometry("800x500")

    # ========================
    # TABLA VENTAS
    # ========================
    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Fecha", "Total"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total")

    tabla.pack(fill="both", expand=True)

    # ========================
    # DETALLE
    # ========================
    tabla_detalle = ttk.Treeview(
        ventana,
        columns=("Nombre", "Cantidad", "Precio", "Subtotal"),
        show="headings"
    )

    tabla_detalle.heading("Nombre", text="Nombre")
    tabla_detalle.heading("Cantidad", text="Cantidad")
    tabla_detalle.heading("Precio", text="Precio")
    tabla_detalle.heading("Subtotal", text="Subtotal")

    tabla_detalle.pack(fill="both", expand=True)

    # ========================
    # CARGAR VENTAS
    # ========================
    def cargar_ventas():

        for fila in tabla.get_children():
            tabla.delete(fila)

        ventas = venta_controller.obtener_ventas()

        for v in ventas:

            total = 0
            for item in v["items"]:
                total += item["cantidad"] * item["precio_venta"]

            tabla.insert("", "end", values=(
                v["id"],
                v["fecha"],
                round(total, 2)
            ))

    # ========================
    # MOSTRAR DETALLE
    # ========================
    def mostrar_detalle(event):

        seleccion = tabla.selection()

        if not seleccion:
            return

        item = tabla.item(seleccion[0])
        id_venta = item["values"][0]

        ventas = venta_controller.obtener_ventas()

        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        for v in ventas:
            if v["id"] == id_venta:

                for item in v["items"]:

                    subtotal = item["cantidad"] * item["precio_venta"]

                    tabla_detalle.insert("", "end", values=(
                        item["nombre"],
                        item["cantidad"],
                        item["precio_venta"],
                        subtotal
                    ))

    tabla.bind("<<TreeviewSelect>>", mostrar_detalle)

    cargar_ventas()

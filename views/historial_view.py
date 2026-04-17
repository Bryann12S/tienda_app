import tkinter as tk
from tkinter import ttk
from controllers.venta_controller import VentaController

venta_controller = VentaController()

def abrir_historial_view():
    ventana = tk.Toplevel()
    ventana.title("Historial de Ventas")
    ventana.geometry("600x400")

    tk.Label(ventana, text="Historial de Ventas", font=("Arial", 14, "bold")).pack(pady=10)

    # Tabla
    tabla_ventas = ttk.Treeview(
        ventana,
        columns=("ID", "Fecha", "Total P.", "Total $"),
        show="headings"
    )

    tabla_ventas.heading("ID", text="ID Venta")
    tabla_ventas.heading("Fecha", text="Fecha")
    tabla_ventas.heading("Total P.", text="Cant. Productos")
    tabla_ventas.heading("Total $", text="Total Venta")

    # Configurar columnas
    tabla_ventas.column("ID", width=80, anchor="center")
    tabla_ventas.column("Fecha", width=180, anchor="center")
    tabla_ventas.column("Total P.", width=100, anchor="center")
    tabla_ventas.column("Total $", width=120, anchor="center")

    tabla_ventas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Cargar datos
    ventas = venta_controller.obtener_ventas()
    
    for v in ventas:
        cantidad_productos = sum(item["cantidad"] for item in v.get("items", []))
        total_venta = sum(item["cantidad"] * item["precio_venta"] for item in v.get("items", []))
        
        tabla_ventas.insert("", "end", values=(
            v.get("id", ""),
            v.get("fecha", ""),
            cantidad_productos,
            f"${total_venta:.2f}"
        ))

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

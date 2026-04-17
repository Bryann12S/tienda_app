import tkinter as tk
from tkinter import ttk, messagebox
from controllers.venta_controller import VentaController

venta_controller = VentaController()

def abrir_historial_view():

    ventana = tk.Toplevel()
    ventana.title("Historial de Ventas y Reportes")
    ventana.geometry("850x600")

    # ========================
    # PANEL DE REPORTES Y FILTROS
    # ========================
    frame_top = tk.Frame(ventana, bg="#f0f0f0", pady=10, padx=10)
    frame_top.pack(fill="x", side="top")

    # Filtros
    frame_filtros = tk.Frame(frame_top, bg="#f0f0f0")
    frame_filtros.pack(side="left", fill="y")
    
    tk.Label(frame_filtros, text="📅 Filtrar por fecha (YYYY-MM-DD):", bg="#f0f0f0").pack(anchor="w")
    
    frame_input = tk.Frame(frame_filtros, bg="#f0f0f0")
    frame_input.pack(fill="x")
    
    entry_fecha = tk.Entry(frame_input, width=15)
    entry_fecha.pack(side="left", padx=(0, 5))

    # Métricas
    frame_metricas = tk.Frame(frame_top, bg="#f0f0f0")
    frame_metricas.pack(side="right", fill="both", expand=True)

    lbl_ganancia = tk.Label(frame_metricas, text="💰 Ganancias: $0.00", font=("Arial", 11, "bold"), bg="#f0f0f0")
    lbl_ganancia.pack(side="left", padx=15, expand=True)

    lbl_producto = tk.Label(frame_metricas, text="🏆 Más vendido: Ninguno (0)", font=("Arial", 11, "bold"), bg="#f0f0f0")
    lbl_producto.pack(side="left", padx=15, expand=True)

    # Funciones de filtrado y reporte
    def aplicar_filtro():
        fecha = entry_fecha.get().strip()
        if fecha:
            # Validar formato simple
            if len(fecha) != 10 or fecha.count("-") != 2:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD")
                return
        else:
            fecha = None
            
        cargar_ventas_y_reportes(fecha)

    def limpiar_filtro():
        entry_fecha.delete(0, tk.END)
        cargar_ventas_y_reportes(None)

    tk.Button(frame_input, text="Filtrar", command=aplicar_filtro).pack(side="left")
    tk.Button(frame_input, text="Limpiar", command=limpiar_filtro).pack(side="left", padx=5)


    # ========================
    # TABLA VENTAS
    # ========================
    frame_ventas = tk.LabelFrame(ventana, text="Historial de Ventas")
    frame_ventas.pack(fill="both", expand=True, padx=10, pady=5)

    tabla = ttk.Treeview(
        frame_ventas,
        columns=("ID", "Fecha", "Total"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total")

    tabla.pack(fill="both", expand=True, padx=5, pady=5)

    # ========================
    # DETALLE
    # ========================
    frame_detalle = tk.LabelFrame(ventana, text="Detalle de Venta Seleccionada")
    frame_detalle.pack(fill="both", expand=True, padx=10, pady=5)

    tabla_detalle = ttk.Treeview(
        frame_detalle,
        columns=("Nombre", "Cantidad", "Precio", "Subtotal"),
        show="headings"
    )

    tabla_detalle.heading("Nombre", text="Nombre")
    tabla_detalle.heading("Cantidad", text="Cantidad")
    tabla_detalle.heading("Precio", text="Precio")
    tabla_detalle.heading("Subtotal", text="Subtotal")

    tabla_detalle.pack(fill="both", expand=True, padx=5, pady=5)

    # ========================
    # CARGAR VENTAS Y REPORTES
    # ========================
    def cargar_ventas_y_reportes(fecha_filtro=None):

        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        # Cargar ventas filtradas
        ventas = venta_controller.obtener_ventas_por_fecha(fecha_filtro)

        for v in ventas:
            total = 0
            for item in v["items"]:
                total += item["cantidad"] * item["precio_venta"]

            tabla.insert("", "end", values=(
                v["id"],
                v["fecha"],
                round(total, 2)
            ))

        # Actualizar Reportes (Métricas)
        ganancia = 0
        if fecha_filtro:
            ganancia = venta_controller.ganancia_por_dia(fecha_filtro)
        else:
            ganancia = sum((item["precio_venta"] - item["precio_compra"]) * item["cantidad"] for v in ventas for item in v["items"])
            
        producto, cant = venta_controller.obtener_producto_mas_vendido(fecha_filtro)

        lbl_ganancia.config(text=f"💰 Ganancias: ${ganancia:.2f}")
        lbl_producto.config(text=f"🏆 Más vendido: {producto} ({cant})")


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

    # Iniciar cargando todo
    cargar_ventas_y_reportes(None)

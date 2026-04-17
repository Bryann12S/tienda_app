import tkinter as tk
from tkinter import ttk, messagebox
from controllers.venta_controller import VentaController
from controllers.deudor_controller import DeudorController

venta_controller = VentaController()
deudor_controller = DeudorController()

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

    lbl_ventas_totales = tk.Label(frame_metricas, text="📈 Ventas Totales: $0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
    lbl_ventas_totales.grid(row=0, column=0, padx=10, pady=2, sticky="w")

    lbl_ganancias_reales = tk.Label(frame_metricas, text="✅ Ganancias Reales: $0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
    lbl_ganancias_reales.grid(row=0, column=1, padx=10, pady=2, sticky="w")

    lbl_deben = tk.Label(frame_metricas, text="🛑 Cuánto te deben: $0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
    lbl_deben.grid(row=1, column=0, padx=10, pady=2, sticky="w")

    lbl_perdidas = tk.Label(frame_metricas, text="📉 Pérdidas (Costo): $0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
    lbl_perdidas.grid(row=1, column=1, padx=10, pady=2, sticky="w")

    lbl_producto = tk.Label(frame_metricas, text="🏆 Más vendido: Ninguno (0)", font=("Arial", 10, "bold"), bg="#f0f0f0")
    lbl_producto.grid(row=0, column=2, rowspan=2, padx=10, pady=2, sticky="w")

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
        columns=("ID", "Fecha", "Total", "Estado"),
        show="headings"
    )

    tabla.heading("ID", text="ID/Tipo")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total")
    tabla.heading("Estado", text="Estado")

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

    def marcar_pagado():
        seleccion = tabla.selection()
        if not seleccion:
            return
            
        item = tabla.item(seleccion[0])
        id_str = str(item["values"][0])
        
        if id_str.startswith("F-"):
            id_deudor = int(id_str.replace("F-", ""))
            estado = item["values"][3]
            if estado.lower() == "pagado":
                messagebox.showinfo("Aviso", "Esta cuenta ya está pagada.")
                return
                
            if messagebox.askyesno("Confirmar", "¿Marcar esta deuda como pagada?"):
                exito, msg = deudor_controller.marcar_como_pagado(id_deudor)
                if exito:
                    messagebox.showinfo("Éxito", msg)
                    fecha_filtro = entry_fecha.get().strip() if entry_fecha.get().strip() else None
                    if fecha_filtro and (len(fecha_filtro) != 10 or fecha_filtro.count("-") != 2):
                        fecha_filtro = None
                    cargar_ventas_y_reportes(fecha_filtro)
                else:
                    messagebox.showerror("Error", msg)

    btn_pagar = tk.Button(frame_detalle, text="Marcar como Pagado", font=("Arial", 10, "bold"), fg="blue", command=marcar_pagado)
    btn_pagar.pack(pady=5)

    # ========================
    # CARGAR VENTAS Y REPORTES
    # ========================
    def cargar_ventas_y_reportes(fecha_filtro=None):

        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        # 1. Obtener los datos
        ventas = venta_controller.obtener_ventas()
        deudores = deudor_controller.obtener_deudores()

        if fecha_filtro:
            ventas = [v for v in ventas if v["fecha"].split(" ")[0] == fecha_filtro]
            deudores = [d for d in deudores if d.get("fecha","").split(" ")[0] == fecha_filtro]

        ventas_totales_monto = 0
        cuanto_deben = 0
        ganancias_reales = 0
        perdidas_costo = 0

        # Insertar ventas normales
        for v in ventas:
            total = 0
            ganancia_venta = 0
            for item in v.get("items", []):
                total += item["cantidad"] * item["precio_venta"]
                ganancia_venta += (item["precio_venta"] - item["precio_compra"]) * item["cantidad"]
                
            tabla.insert("", "end", values=(
                f"V-{v['id']}",
                v["fecha"],
                round(total, 2),
                "Pagado"
            ))
            ventas_totales_monto += total
            ganancias_reales += ganancia_venta

        # Insertar fiados (deudores)
        for d in deudores:
            total = 0
            costo_total = 0
            ganancia_fiado = 0
            for item in d.get("items", []):
                subt = item["cantidad"] * item["precio_venta"]
                costo = item["cantidad"] * item["precio_compra"]
                total += subt
                costo_total += costo
                ganancia_fiado += (item["precio_venta"] - item["precio_compra"]) * item["cantidad"]
                
            estado = d.get("estado", "pendiente").capitalize()
            
            tabla.insert("", "end", values=(
                f"F-{d['id']}",
                d.get("fecha", ""),
                round(total, 2),
                estado
            ))
            
            ventas_totales_monto += total
            if estado.lower() == "pendiente":
                cuanto_deben += total
                perdidas_costo += costo_total
            else:
                ganancias_reales += ganancia_fiado

        # Producto más vendido
        producto, cant = venta_controller.obtener_producto_mas_vendido(fecha_filtro)

        # Actualizar labels
        lbl_ventas_totales.config(text=f"📈 Ventas Totales: ${ventas_totales_monto:.2f}")
        lbl_ganancias_reales.config(text=f"✅ Ganancias Reales: ${ganancias_reales:.2f}")
        lbl_deben.config(text=f"🛑 Cuánto te deben: ${cuanto_deben:.2f}")
        lbl_perdidas.config(text=f"📉 Pérdidas (Costo): ${perdidas_costo:.2f}")
        lbl_producto.config(text=f"🏆 Más vendido: {producto} ({cant})")


    # ========================
    # MOSTRAR DETALLE
    # ========================
    def mostrar_detalle(event):

        seleccion = tabla.selection()

        if not seleccion:
            return

        item = tabla.item(seleccion[0])
        id_str = str(item["values"][0])
        
        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        if id_str.startswith("V-"):
            id_buscado = int(id_str.replace("V-", ""))
            items_encontrados = []
            for v in venta_controller.obtener_ventas():
                if v["id"] == id_buscado:
                    items_encontrados = v.get("items", [])
                    break
        elif id_str.startswith("F-"):
            id_buscado = int(id_str.replace("F-", ""))
            items_encontrados = []
            for d in deudor_controller.obtener_deudores():
                if d["id"] == id_buscado:
                    items_encontrados = d.get("items", [])
                    break
        else:
            return

        for it in items_encontrados:
            subtotal = it["cantidad"] * it["precio_venta"]
            tabla_detalle.insert("", "end", values=(
                it["nombre"],
                it["cantidad"],
                it["precio_venta"],
                subtotal
            ))

    tabla.bind("<<TreeviewSelect>>", mostrar_detalle)

    # Iniciar cargando todo
    cargar_ventas_y_reportes(None)

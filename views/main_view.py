import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from views.producto_view import abrir_producto_view
from views.venta_view import abrir_venta_view
from views.historial_view import abrir_historial_view
from views.deudor_view import abrir_deudor_view
from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController
from controllers.deudor_controller import DeudorController
 
venta_controller = VentaController()
producto_controller = ProductoController()
deudor_controller = DeudorController()
 
 
def iniciar_main_view():
    ventana = tb.Window(themename="cosmo")
    ventana.title("Tienda App - POS System")
    ventana.state('zoomed')
 
    # ── Layout principal ──────────────────────────────────────────────
    main_frame = tb.Frame(ventana)
    main_frame.pack(fill=BOTH, expand=True)
 
    # ── BARRA LATERAL ─────────────────────────────────────────────────
    sidebar = tb.Frame(main_frame, bootstyle="dark", width=200)
    sidebar.pack(side=LEFT, fill=Y)
    sidebar.pack_propagate(False)
 
    # Logo / título en el sidebar
    tb.Label(
        sidebar,
        text="🏪",
        font=("Arial", 28),
        bootstyle="inverse-dark"
    ).pack(pady=(25, 0))
 
    tb.Label(
        sidebar,
        text="Tienda App",
        font=("Arial", 13, "bold"),
        bootstyle="inverse-dark"
    ).pack(pady=(2, 20))
 
    tb.Separator(sidebar, bootstyle="secondary").pack(fill=X, padx=15, pady=5)
 
    # ── Contenedor del contenido ──────────────────────────────────────
    content_area = tb.Frame(main_frame)
    content_area.pack(side=LEFT, fill=BOTH, expand=True)
 
    # Guardamos referencia al botón activo
    active_btn = {"ref": None}
 
    NAV_ITEMS = [
        ("🏠  Inicio",       "inicio"),
        ("📦  Productos",    "productos"),
        ("🛒  Punto de Venta","ventas"),
        ("📊  Historial",    "historial"),
        ("📒  Cuentas Fiadas","fiados"),
    ]
 
    def mostrar_vista(nombre_vista):
        # Limpiar contenido
        for w in content_area.winfo_children():
            w.destroy()
 
        frame = tb.Frame(content_area)
        frame.pack(fill=BOTH, expand=True)
 
        if nombre_vista == "inicio":
            abrir_inicio_view(frame)
        elif nombre_vista == "productos":
            abrir_producto_view(frame)
        elif nombre_vista == "ventas":
            abrir_venta_view(frame)
        elif nombre_vista == "historial":
            abrir_historial_view(frame)
        elif nombre_vista == "fiados":
            abrir_deudor_view(frame)
 
    def crear_boton_nav(texto, vista):
        btn = tk.Button(
            sidebar,
            text=texto,
            font=("Arial", 11),
            anchor="w",
            padx=18,
            relief="flat",
            cursor="hand2",
            bd=0,
            bg="#2b3e50",        # color sidebar "dark" de cosmo
            fg="#c8d6e5",
            activebackground="#1a252f",
            activeforeground="#ffffff",
        )
        btn.pack(fill=X, pady=2, padx=8)
 
        def on_click():
            # Restaurar color del botón anterior
            if active_btn["ref"] and active_btn["ref"] != btn:
                active_btn["ref"].config(bg="#2b3e50", fg="#c8d6e5")
            # Marcar activo
            btn.config(bg="#1a7fbd", fg="#ffffff")
            active_btn["ref"] = btn
            mostrar_vista(vista)
 
        btn.config(command=on_click)
        return btn
 
    for texto, vista in NAV_ITEMS:
        crear_boton_nav(texto, vista)
 
    # Separador y versión al fondo del sidebar
    tb.Frame(sidebar).pack(expand=True)   # spacer
    tb.Separator(sidebar, bootstyle="secondary").pack(fill=X, padx=15, pady=5)
    tb.Label(
        sidebar,
        text="v1.0.0",
        font=("Arial", 9),
        bootstyle="inverse-dark",
        foreground="#556677"
    ).pack(pady=(0, 15))
 
    # Mostrar inicio por defecto (simula click en el primer botón)
    mostrar_vista("inicio")
    # Marcar el primer botón como activo visualmente
    primer_btn = sidebar.winfo_children()[3]  # 0=emoji, 1=label, 2=sep, 3=primer btn
    if isinstance(primer_btn, tk.Button):
        primer_btn.config(bg="#1a7fbd", fg="#ffffff")
        active_btn["ref"] = primer_btn
 
    ventana.mainloop()
 
 
# ══════════════════════════════════════════════════════════════════════
# VISTA DE INICIO / DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def abrir_inicio_view(parent):
    # ── Encabezado ────────────────────────────────────────────────────
    header = tb.Frame(parent, padding=(25, 18, 25, 5))
    header.pack(fill=X)
 
    tb.Label(
        header,
        text="Panel de Control",
        font=("Arial", 22, "bold"),
        bootstyle="primary"
    ).pack(side=LEFT)
 
    from datetime import datetime
    tb.Label(
        header,
        text=datetime.now().strftime("📅  %d/%m/%Y  %H:%M"),
        font=("Arial", 11),
        bootstyle="secondary"
    ).pack(side=RIGHT, pady=5)
 
    tb.Separator(parent, bootstyle="light").pack(fill=X, padx=25, pady=5)
 
    # ── Tarjetas de métricas ──────────────────────────────────────────
    frame_cards = tb.Frame(parent, padding=(25, 10))
    frame_cards.pack(fill=X)
 
    # Obtener datos
    try:
        ventas = venta_controller.obtener_ventas()
        productos = producto_controller.listar_productos()
        deudores = deudor_controller.obtener_deudores()
    except Exception:
        ventas, productos, deudores = [], [], []
 
    # Calcular métricas
    total_ventas_hoy = 0
    ganancia_hoy = 0
    from datetime import date
    hoy = date.today().isoformat()
    for v in ventas:
        if v.get("fecha", "").startswith(hoy):
            for it in v.get("items", []):
                total_ventas_hoy += it["cantidad"] * it["precio_venta"]
                ganancia_hoy += (it["precio_venta"] - it["precio_compra"]) * it["cantidad"]
 
    deuda_pendiente = 0
    deudores_pendientes = 0
    for d in deudores:
        if d.get("estado", "pendiente") != "pagado":
            deudores_pendientes += 1
            t = d.get("total", 0)
            a = d.get("abonado", 0)
            deuda_pendiente += t - a
 
    stock_bajo = [p for p in productos if p.stock <= 5]
 
    CARDS = [
        ("💵", f"${total_ventas_hoy:.2f}", "Ventas de Hoy",     "success"),
        ("📈", f"${ganancia_hoy:.2f}",     "Ganancia de Hoy",   "primary"),
        ("🛑", f"${deuda_pendiente:.2f}",  "Deuda Pendiente",   "danger"),
        ("👥", str(deudores_pendientes),   "Deudores Activos",  "warning"),
        ("📦", str(len(productos)),        "Productos Activos", "info"),
        ("⚠️", str(len(stock_bajo)),       "Stock Bajo (≤5)",   "secondary"),
    ]
 
    for col, (icono, valor, label, estilo) in enumerate(CARDS):
        card = tb.Frame(frame_cards, bootstyle=f"{estilo}", padding=15)
        card.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")
        frame_cards.columnconfigure(col, weight=1)
 
        tb.Label(card, text=icono, font=("Arial", 22), bootstyle=f"inverse-{estilo}").pack()
        tb.Label(card, text=valor, font=("Arial", 17, "bold"), bootstyle=f"inverse-{estilo}").pack()
        tb.Label(card, text=label, font=("Arial", 9),  bootstyle=f"inverse-{estilo}").pack()
 
    tb.Separator(parent, bootstyle="light").pack(fill=X, padx=25, pady=10)
 
    # ── Paneles inferiores ─────────────────────────────────────────────
    frame_bottom = tb.Frame(parent, padding=(25, 0, 25, 15))
    frame_bottom.pack(fill=BOTH, expand=True)
    frame_bottom.columnconfigure(0, weight=1)
    frame_bottom.columnconfigure(1, weight=1)
 
    # Panel: Últimas ventas
    lf_ventas = tb.LabelFrame(frame_bottom, text="🧾 Últimas Ventas")
    lf_ventas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
 
    cols_v = ("ID", "Fecha", "Total")
    tv_ventas = tb.Treeview(lf_ventas, columns=cols_v, show="headings", height=8, bootstyle="primary")
    for c in cols_v:
        tv_ventas.heading(c, text=c)
    tv_ventas.column("ID",    width=50,  anchor=CENTER)
    tv_ventas.column("Fecha", width=130, anchor=CENTER)
    tv_ventas.column("Total", width=80,  anchor=E)
    tv_ventas.pack(fill=BOTH, expand=True)
 
    for v in reversed(ventas[-10:]):
        t = sum(it["cantidad"] * it["precio_venta"] for it in v.get("items", []))
        tv_ventas.insert("", "end", values=(f"V-{v['id']}", v.get("fecha",""), f"${t:.2f}"))
 
    # Panel: Productos con stock bajo
    lf_stock = tb.LabelFrame(frame_bottom, text="⚠️ Productos con Stock Bajo")
    lf_stock.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
 
    cols_s = ("Nombre", "Stock")
    tv_stock = tb.Treeview(lf_stock, columns=cols_s, show="headings", height=8, bootstyle="warning")
    for c in cols_s:
        tv_stock.heading(c, text=c)
    tv_stock.column("Nombre", width=160)
    tv_stock.column("Stock",  width=60, anchor=CENTER)
    tv_stock.pack(fill=BOTH, expand=True)
 
    if stock_bajo:
        for p in stock_bajo:
            tv_stock.insert("", "end", values=(p.nombre, p.stock))
    else:
        tv_stock.insert("", "end", values=("✅ Todo el stock está bien", ""))
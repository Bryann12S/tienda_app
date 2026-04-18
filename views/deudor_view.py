import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from controllers.deudor_controller import DeudorController
from controllers.producto_controller import ProductoController

deudor_controller = DeudorController()
producto_controller = ProductoController()

def abrir_deudor_view(parent):
    ventana = parent
    carrito_fiado = []

    # ========================
    # TOP METRICS
    # ========================
    frame_metricas = tb.Frame(ventana, padding=10)
    frame_metricas.pack(fill=X, side=TOP)
    
    lbl_deudores = tb.Label(frame_metricas, text="👥 Deudores Pendientes: 0", font=("Arial", 12, "bold"), bootstyle="warning")
    lbl_deudores.pack(side=LEFT, padx=15)
    
    lbl_deuda_total = tb.Label(frame_metricas, text="💰 Dinero Total Pendiente: $0.00", font=("Arial", 12, "bold"), bootstyle="danger")
    lbl_deuda_total.pack(side=LEFT, padx=15)

    # ========================
    # PANELS
    # ========================
    frame_izq = tb.LabelFrame(ventana, text="Registrar Nuevo Fiado")
    frame_izq.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    frame_der = tb.LabelFrame(ventana, text="Gestión de Cuentas Fiadas")
    frame_der.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    # --- IZQUIERDA: CREAR FIADO --- #
    frame_datos = tb.Frame(frame_izq)
    frame_datos.pack(fill=X, pady=5)
    
    tb.Label(frame_datos, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
    entry_cliente = tb.Entry(frame_datos, width=20)
    entry_cliente.grid(row=0, column=1, padx=5, pady=5)
    
    tb.Label(frame_datos, text="Límite:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
    date_limite = tb.DateEntry(frame_datos, dateformat="%Y-%m-%d", width=12)
    date_limite.grid(row=0, column=3, padx=5, pady=5)

    tb.Label(frame_izq, text="Productos (Selecciona para fiar):", font=("Arial", 10, "bold")).pack(anchor=W, pady=5)
    
    tabla_disp = tb.Treeview(frame_izq, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=5)
    tabla_disp.heading("ID", text="ID")
    tabla_disp.heading("Nombre", text="Nombre")
    tabla_disp.heading("Precio", text="Precio")
    tabla_disp.heading("Stock", text="Stock")
    tabla_disp.column("ID", width=40)
    tabla_disp.column("Stock", width=50)
    tabla_disp.pack(fill=X)

    frame_add = tb.Frame(frame_izq)
    frame_add.pack(fill=X, pady=5)
    tb.Label(frame_add, text="Cant:").pack(side=LEFT)
    entry_cant = tb.Entry(frame_add, width=10)
    entry_cant.pack(side=LEFT, padx=5)
    entry_cant.insert(0, "1")

    def add_fiado():
        seleccion = tabla_disp.selection()
        if not seleccion: return
        id_prod = tabla_disp.item(seleccion[0])["values"][0]
        try:
            cant = int(entry_cant.get())
            if cant <= 0: raise Exception
        except: return messagebox.showerror("Error","Cantidad inválida")
        
        producto = producto_controller.buscar_producto_por_id(id_prod)
        if producto.stock < cant:
            return messagebox.showerror("Error","Stock insuficiente")
            
        for i in carrito_fiado:
            if i["id"] == producto.id:
                if producto.stock < i["cantidad"] + cant:
                    return messagebox.showerror("Error","Stock insuficiente")
                i["cantidad"] += cant
                actualizar_carr_f()
                return

        carrito_fiado.append({"id": producto.id, "nombre": producto.nombre, "cantidad": cant, "precio_compra": producto.precio_compra, "precio_venta": producto.precio_venta})
        actualizar_carr_f()

    tb.Button(frame_add, text="➕ Agregar al Fiado", bootstyle="primary", command=add_fiado).pack(side=LEFT, padx=5)

    tabla_carr = tb.Treeview(frame_izq, columns=("Nombre", "Cant", "Subt"), show="headings", height=4)
    tabla_carr.heading("Nombre", text="Nombre")
    tabla_carr.heading("Cant", text="Cant.")
    tabla_carr.heading("Subt", text="Subtotal")
    tabla_carr.pack(fill=X, pady=5)
    
    lbl_total_f = tb.Label(frame_izq, text="Total: $0.00", font=("Arial", 12, "bold"))
    lbl_total_f.pack(anchor=E)

    def actualizar_carr_f():
        for fila in tabla_carr.get_children(): tabla_carr.delete(fila)
        tot = sum((i["cantidad"]*i["precio_venta"]) for i in carrito_fiado)
        for i in carrito_fiado:
            tabla_carr.insert("","end",values=(i["nombre"], i["cantidad"], f"${i['cantidad']*i['precio_venta']:.2f}"))
        lbl_total_f.config(text=f"Total: ${tot:.2f}")

    def crear_f():
        cli = entry_cliente.get().strip()
        if not cli or not carrito_fiado:
            return messagebox.showwarning("Aviso", "Falta cliente o productos")
        
        lim = date_limite.entry.get()
        deudor_controller.crear_fiado(cli, carrito_fiado, lim)
        messagebox.showinfo("Exito", "Fiado Registrado")
        carrito_fiado.clear()
        entry_cliente.delete(0, END)
        actualizar_carr_f()
        cargar_productos()
        cargar_deudores()

    tb.Button(frame_izq, text="✅ Registrar Cuenta Fiada", command=crear_f, bootstyle="success").pack(fill=X, pady=5)

    # --- DERECHA: DEUDORES --- #
    tabla = tb.Treeview(frame_der, columns=("ID", "Nombre", "Límite", "Total", "Abonado", "Restante", "Estado"), show="headings", bootstyle="warning")
    for col in ("ID", "Nombre", "Límite", "Total", "Abonado", "Restante", "Estado"):
        tabla.heading(col, text=col)
    tabla.column("ID", width=40)
    tabla.column("Límite", width=80, anchor=CENTER)
    tabla.column("Total", width=80, anchor=E)
    tabla.column("Abonado", width=80, anchor=E)
    tabla.column("Restante", width=80, anchor=E)
    tabla.column("Estado", width=80, anchor=CENTER)
    tabla.pack(fill=BOTH, expand=True, pady=5)

    def cargar_productos():
        for f in tabla_disp.get_children(): tabla_disp.delete(f)
        for p in producto_controller.listar_productos():
            tabla_disp.insert("", "end", values=(p.id, p.nombre, p.precio_venta, p.stock))

    def cargar_deudores():
        for f in tabla.get_children(): tabla.delete(f)
        pendientes = 0
        dinero_pendiente = 0.0
        
        for d in reversed(deudor_controller.obtener_deudores()):
            t = d.get("total", 0.0)
            a = d.get("abonado", 0.0)
            r = t - a
            st = d.get("estado", "pendiente")
            if st != "pagado":
                pendientes += 1
                dinero_pendiente += r
                
            tabla.insert("", "end", values=(
                d["id"], d["nombre"], d.get("fecha_limite", "N/A"),
                f"${t:.2f}", f"${a:.2f}", f"${r:.2f}", st.upper()
            ))
            
        lbl_deudores.config(text=f"👥 Deudores Pendientes: {pendientes}")
        lbl_deuda_total.config(text=f"💰 Dinero Total Pendiente: ${dinero_pendiente:.2f}")

    frame_acc = tb.Frame(frame_der)
    frame_acc.pack(fill=X)

    def abonar():
        seleccion = tabla.selection()
        if not seleccion: return messagebox.showwarning("Aviso", "Selecciona cuenta")
        id_str = tabla.item(seleccion[0])["values"][0]
        estado = tabla.item(seleccion[0])["values"][6]
        if estado == "PAGADO": return messagebox.showinfo("Info", "Ya está pagada.")
        
        r = simpledialog.askfloat("Abonar", "Monto a ingresar:", minvalue=0.01)
        if r:
            exito, msg = deudor_controller.abonar_a_deuda(int(id_str), float(r))
            if exito:
                cargar_deudores()
                messagebox.showinfo("Exito", msg)
            else:
                messagebox.showerror("Error", msg)

    tb.Button(frame_acc, text="💲 Ingresar Abono", bootstyle="success", command=abonar).pack(side=LEFT, padx=5)

    cargar_productos()
    cargar_deudores()

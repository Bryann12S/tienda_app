import ttkbootstrap as tb
from ttkbootstrap.constants import *
from controllers.producto_controller import ProductoController

controller_producto = ProductoController()

def abrir_producto_view(parent):
    ventana = parent
    id_editando = None

    # Layout: Izquierda (Formulario), Derecha (Tabla)
    frame_izq = tb.LabelFrame(ventana, text="Formulario de Producto")
    frame_izq.pack(side=LEFT, fill=Y, padx=10, pady=10)

    frame_der = tb.Frame(ventana, padding=10)
    frame_der.pack(side=LEFT, fill=BOTH, expand=True)

    # --- FORMULARIO (Izquierda) ---
    tb.Label(frame_izq, text="Nombre del Producto", font=("Arial", 11)).pack(anchor=W, pady=(10, 2))
    entry_nombre = tb.Entry(frame_izq, width=30)
    entry_nombre.pack(fill=X, pady=(0, 10))

    tb.Label(frame_izq, text="Precio de Compra ($)", font=("Arial", 11)).pack(anchor=W, pady=2)
    entry_precio_compra = tb.Entry(frame_izq)
    entry_precio_compra.pack(fill=X, pady=(0, 10))

    tb.Label(frame_izq, text="Precio de Venta ($)", font=("Arial", 11)).pack(anchor=W, pady=2)
    entry_precio_venta = tb.Entry(frame_izq)
    entry_precio_venta.pack(fill=X, pady=(0, 10))

    tb.Label(frame_izq, text="Stock Inicial", font=("Arial", 11)).pack(anchor=W, pady=2)
    entry_stock = tb.Entry(frame_izq)
    entry_stock.pack(fill=X, pady=(0, 20))

    def agregar():
        nonlocal id_editando
        try:
            nombre = entry_nombre.get().strip()
            precio_compra = float(entry_precio_compra.get())
            precio_venta = float(entry_precio_venta.get())
            stock = int(entry_stock.get())
            if not nombre:
                raise ValueError
        except:
            tb.dialogs.dialogs.Messagebox.show_error("Datos inválidos o faltantes", "Error")
            return

        if id_editando:
           producto = controller_producto.buscar_producto_por_id(id_editando)
           producto.nombre = nombre
           producto.precio_compra = precio_compra
           producto.precio_venta = precio_venta
           producto.stock = stock
           controller_producto.actualizar_producto(producto)
           id_editando = None
           btn_guardar.config(text="Guardar Nuevo Producto")
        else:
            controller_producto.crear_producto(nombre, precio_compra, precio_venta, stock)
            
        mostrar_productos()
        limpiar_campos()

    def limpiar_campos():
        entry_nombre.delete(0, END)
        entry_precio_compra.delete(0, END)
        entry_precio_venta.delete(0, END)
        entry_stock.delete(0, END)
        nonlocal id_editando
        if id_editando:
            id_editando = None
            btn_guardar.config(text="Guardar Nuevo Producto")

    btn_guardar = tb.Button(frame_izq, text="Guardar Nuevo Producto", command=agregar, bootstyle="success")
    btn_guardar.pack(fill=X, pady=5)
    
    tb.Button(frame_izq, text="Limpiar Formulario", command=limpiar_campos, bootstyle="secondary-outline").pack(fill=X, pady=5)

    # --- TABLA Y ACCIONES (Derecha) ---
    titulo_tabla = tb.Label(frame_der, text="Inventario de Productos", font=("Arial", 16, "bold"))
    titulo_tabla.pack(anchor=W, pady=(0, 10))

    tabla = tb.Treeview(frame_der, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", bootstyle="primary")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio", text="Precio Venta")
    tabla.heading("Stock", text="Stock")
    tabla.column("ID", width=50, anchor=CENTER)
    tabla.column("Stock", width=80, anchor=CENTER)
    tabla.column("Precio", width=100, anchor=E)

    tabla.pack(fill=BOTH, expand=True)

    frame_acciones = tb.Frame(frame_der)
    frame_acciones.pack(fill=X, pady=10)

    def obtener_id_seleccionado():
        seleccion = tabla.selection()
        if not seleccion:
            tb.dialogs.dialogs.Messagebox.show_warning("Selecciona un producto de la tabla.", "Aviso")
            return None
        return tabla.item(seleccion[0])["values"][0]

    def editar_producto():
        id_producto = obtener_id_seleccionado()
        if not id_producto:
            return

        producto = controller_producto.buscar_producto_por_id(id_producto)
        nonlocal id_editando
        id_editando = id_producto

        limpiar_campos()
        id_editando = id_producto # restore because limpiar_campos clears it
        entry_nombre.insert(0, producto.nombre)
        entry_precio_compra.insert(0, producto.precio_compra)
        entry_precio_venta.insert(0, producto.precio_venta)
        entry_stock.insert(0, producto.stock)
        btn_guardar.config(text="Actualizar Producto")

    def eliminar_producto():
        id_producto = obtener_id_seleccionado()
        if not id_producto:
            return
        
        # Opcional confirmación
        controller_producto.desactivar_producto(id_producto)
        mostrar_productos()

    tb.Button(frame_acciones, text="✏️ Cargar para Editar", command=editar_producto, bootstyle="info").pack(side=LEFT, padx=5)
    tb.Button(frame_acciones, text="🗑️ Dar de Baja", command=eliminar_producto, bootstyle="danger").pack(side=LEFT, padx=5)

    def mostrar_productos():
        for fila in tabla.get_children():
            tabla.delete(fila)
        productos = controller_producto.listar_productos()
        for p in productos:
            tabla.insert("", "end", values=(p.id, p.nombre, f"${p.precio_venta:.2f}", p.stock))

    mostrar_productos()
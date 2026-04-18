import tkinter as tk
import ttkbootstrap as tb
from views.producto_view import abrir_producto_view
from views.venta_view import abrir_venta_view
from views.historial_view import abrir_historial_view
from views.deudor_view import abrir_deudor_view

def iniciar_main_view():
    ventana = tb.Window(themename="cosmo")
    ventana.title("Tienda App - POS System")
    ventana.state('zoomed') # Maximizar ventana
    
    container = tb.Frame(ventana)
    container.pack(fill="both", expand=True)

    def mostrar_menu():
        for widget in container.winfo_children():
            widget.destroy()
            
        menu_frame = tb.Frame(container)
        menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        tb.Label(menu_frame, text="MENÚ PRINCIPAL", font=("Arial", 32, "bold"), bootstyle="primary").pack(pady=40)

        tb.Button(menu_frame, text="📦 Gestión de Productos", command=lambda: mostrar_vista(abrir_producto_view), bootstyle="primary-outline", width=30).pack(pady=10, ipady=8)
        tb.Button(menu_frame, text="🛒 Punto de Venta", command=lambda: mostrar_vista(abrir_venta_view), bootstyle="success", width=30).pack(pady=10, ipady=8)
        tb.Button(menu_frame, text="📊 Historial y Reportes", command=lambda: mostrar_vista(abrir_historial_view), bootstyle="info", width=30).pack(pady=10, ipady=8)
        tb.Button(menu_frame, text="📒 Cuentas Fiadas", command=lambda: mostrar_vista(abrir_deudor_view), bootstyle="warning", width=30).pack(pady=10, ipady=8)

    def mostrar_vista(vista_func):
        for widget in container.winfo_children():
            widget.destroy()
        
        vista_frame = tb.Frame(container)
        vista_frame.pack(fill="both", expand=True)
        
        header = tb.Frame(vista_frame, bootstyle="secondary")
        header.pack(fill="x", pady=5)
        
        tb.Button(header, text="🔙 Regresar al Menú", command=mostrar_menu, bootstyle="danger").pack(side="left", padx=10, pady=5)
        
        cuerpo_vista = tb.Frame(vista_frame)
        cuerpo_vista.pack(fill="both", expand=True, padx=20, pady=10)
        
        vista_func(cuerpo_vista)

    mostrar_menu()
    ventana.mainloop()

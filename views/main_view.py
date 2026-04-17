import  tkinter as tk 
from views.producto_view import abrir_producto_view
from views.venta_view import abrir_venta_view
from views.historial_view import abrir_historial_view
from views.deudor_view import abrir_deudor_view

def iniciar_main_view():
    ventana = tk.Tk()
    ventana.title("Tienda App")
    ventana.geometry("400x400")
    
    tk.Label(ventana, text="MENÚ PRINCIPAL").pack()

    tk.Button(
        ventana, 
        text="Producto",
        command=abrir_producto_view
    ).pack(pady=5)

    tk.Button(
        ventana, 
        text="Venta",
        command=abrir_venta_view
    ).pack(pady=5)

    tk.Button(
        ventana, 
        text="Historial de Ventas",
        command=abrir_historial_view
    ).pack(pady=5)

    tk.Button(
        ventana, 
        text="Cuentas Fiadas (Deudores)",
        command=abrir_deudor_view
    ).pack(pady=5)

    ventana.mainloop()

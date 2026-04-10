import  tkinter as tk 
from views.producto_view import abrir_producto_view
from views.venta_view import abrir_venta_view

def iniciar_main_view():
    ventana = tk.Tk()
    ventana.title("Tienda App")
    ventana.geometry("400x400")
    
    tk.Label(ventana, text="MENÚ PRINCIPAL").pack()

    tk.Button(
        ventana, 
        text="Producto",
        command=abrir_producto_view
    ).pack()

    tk.Button(
        ventana, 
        text="Venta",
        command=abrir_venta_view
    ).pack()

    ventana.mainloop()


    

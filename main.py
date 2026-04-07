from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from controllers.deudor_controller import DeudorController
from controllers.gasto_controller import GastoController


def main():
    controller = ProductoController()
    venta_controller = VentaController()
    deudor_controller = DeudorController()
    gasto_controller = GastoController()

    print("=== CREAR PRODUCTO ===")

    controller.crear_producto(
           "Arroz",
           0.00,
           1.00,
           25
    )

    print("Producto creado\n")
    
    print("=== LISTAR PRODUCTOS ===")

    productos = controller.listar_productos()

    for producto in productos:
        print(f"ID: {producto.id}")
        print(f"Nombre: {producto.nombre}")
        print(f"Precio compra: {producto.precio_compra}")
        print(f"Precio venta: {producto.precio_venta}")
        print(f"Stock: {producto.stock}")
        print("--------------------")

    producto = controller.buscar_producto_por_id(1)

    if producto:
        print("Producto encontrado:")
        print(producto.nombre)
    else:
        print("Producto no encontrado")

    controller.vender_producto(1,3)
    
    venta_controller.crear_venta([
        {"id": 1, "cantidad": 2},
    ])

    venta_controller.calcular_ganancia_total()
    venta_controller.ganancia_por_dia("2026-04-07")

    deudor_controller.crear_fiado(
        "Bryan", 
        [
            {"id": 1, "cantidad": 2},
            {"id": 2, "cantidad": 3}
        ]
    )

    deudor_controller.marcar_como_pagado(1)

    gasto_controller.crear_gasto("Arroz", 1.00)
    gasto_controller.listar_gastos()
                                                 

if __name__ == "__main__":
    main()
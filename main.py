from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController

def main():
    controller = ProductoController()
    venta_controller = VentaController()

    print("=== CREAR PRODUCTO ===")

     #  controller.crear_producto(
     #       "Arroz",
     #       0.00,
     #       1.09,
     #       50
     #   )

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
                                                 

if __name__ == "__main__":
    main()
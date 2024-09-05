import os
import platform
from productos.GestionProductos import GestionProductos
from productos.ProductoAlimenticio import ProductoAlimenticio
from productos.ProductoElectronico import ProductoElectronico

def limpiar_consola():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    pass

def mostrar_menu():
    print(
        """
========== Menú de Gestion de Productos =========
1. Agregar Producto Alimenticio
2. Agregar Producto Electronico
3. Buscar Producto por codigo
4. Actualizar Producto
5. Eliminar Producto
6. Listar todos los Productos
7. Salir
=================================================
        """)
    
def agregar_producto(gestion, opcion_producto):
    codigo_producto = input("Ingrese el codigo del producto: ")
    nombre = input("Ingrese el nombre del producto: ")
    precio = input("Ingrese el precio del producto: ")
    stock = input("Ingrese la cantidad en stock: ")
    marca = input("Ingrese la marca del producto: ")
    categoria = input("Ingrese una categoria para el producto: ")
    
    if opcion_producto == '1':
        fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY/MM/DD): ")
        es_libre_gluten = input("Es libre de gluten (y/n): ")
        while es_libre_gluten != 'y' and es_libre_gluten != 'n':
            print("Opciones invalida. Digite 'y' (si) o 'n' (no)")
            es_libre_gluten = input("Es libre de gluten: y/n")
        es_libre_gluten = 1 if es_libre_gluten == 'y' else 0
        try:
            producto = ProductoAlimenticio(codigo_producto, nombre, precio, stock, marca, categoria, fecha_vencimiento, es_libre_gluten)
        except ValueError as error:
            print(f"Error al crear producto alimenticio.")
            print(f"{error}")
            input("Presione Enter para continuar...")
            return
        else:
            gestion.agregar_producto(producto)
        
    else:
        color = input("Ingrese color para el producto: ")
        meses_garantia = input("Ingrese los meses de garantias del producto: ")
        try:
            producto = ProductoElectronico(codigo_producto, nombre, precio, stock, marca, categoria, color, meses_garantia)
        except Exception as error:
            print(f"Error al crear producto electronico.")
            print(f"{error}")
            input("Presione Enter para continuar...")
            return
        else:
            gestion.agregar_producto(producto)
        
        
    input("Presione Enter para continuar...")

def buscar_producto_por_codigo(gestion):
    codigo = input("Ingrese el codigo del producto: ")
    producto = gestion.leer_producto(codigo)
    return producto

def eliminar_producto(gestion):
    codigo = input("Ingrese el codigo del producto: ")
    gestion.eliminar_producto(codigo)
    input("Presione Enter para continuar...")

def listar_productos(gestion): 
    productos = gestion.leer_productos()
    for producto in productos:
        print(producto)
        print("===================================")
    input("Presione Enter para continuar...")

def actualizar_producto(gestion):
    #Se reutiliza la funcion de buscar por codigo
    producto = buscar_producto_por_codigo(gestion)
    
    if (producto is None):
        input("Presione Enter para continuar...")
        return
    print("========== Menú de Actualizacion ==========")
    
    #Dictionario para seleccionar el campo segun la opcion ingresada por el usuario
    #Indice 0: Nombre de la propiedad dentro del json
    #Indice 1: Nombre del campo con otro formato para mostrar en consola.
    opciones_campos = {
        '1': ["nombre", "Nombre"],
        '2': ["precio", "Precio"],
        '3': ["stock", "Stock"],
        '4': ["marca", "Marca"],
        '5': ["categoria", "Categoria"]
    }
    
    while True:
        mostrar_menu_actualizar_campos(producto)
        opcion = input("Seleccione el campo que desea actualizar: ")
        
        #Opcion de salir del menú de actualizacion
        if opcion == '8':
            break
        
        #Se obtiene el arreglo correspondiente segun la opcion del usuario.
        #Sirve para los atributos generales.
        campo = opciones_campos.get(opcion)
        
        #Control para atributos especificos segun el tipo de producto.
        if opcion == '6':
            if 'fecha_vencimiento' in producto:
                campo = ["fecha_vencimiento","Fecha de Vencimiento"]
            else:
                campo = ["color", "Color"]
        if opcion == '7':
            if 'fecha_vencimiento' in producto:
                campo = ["es_libre_gluten", "Es libre de gluten"]
            else:
                campo = ["meses_garantia", "Meses de Garantia"]

        if campo is None:
            print("Ingrese una opcion válida")
            continue
        
        print("-----------------------------------------------")
        print(f"Campo a actualizar: {campo[1]}")
        valor = input(f"Nuevo {campo[1]}: ")
        gestion.actualizar_producto(producto.codigo_producto, campo, valor)
        input("Presione Enter para continuar...")

def mostrar_menu_actualizar_campos(producto):
    #Opciones generales de producto.
    menu = """
========= Seleccione el campo a actualizar =========
1.Nombre.
2.Precio.
3.Stock.
4.Marca.
5.Categoria.
"""
    #Agregar al menu las opciones segun el tipo de producto.
    if isinstance(producto, ProductoAlimenticio):
        menu += """6.Fecha de Vencimiento.
7.Libre de gluten.
8.Salir."""
    else:
        menu += """6.Color.
7.Meses de garantía.
8.Salir."""
        
    print(menu)

if __name__ == "__main__":
    #archivo_productos = 'productos_db.json'
    gestion = GestionProductos()
    
    while True:
        limpiar_consola()
        mostrar_menu()
        print("Seleccione una de las opciones:", end = ' ')
        opcion = input()
        
        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        elif opcion == '3':
            producto_datos = buscar_producto_por_codigo(gestion) 
            if producto_datos is not None:   
                mensaje_consola = ""
                mensaje_consola += f"""{producto_datos}
=========================================="""
                print(mensaje_consola)
            input("Presione Enter para continuar...")
        elif opcion == '4':
            actualizar_producto(gestion)
        elif opcion == '5':
            eliminar_producto(gestion)
        elif opcion == '6':
            listar_productos(gestion)
        elif opcion == '7':
            break;
        else: 
            print('Opcion inválida.')
        
import json
import os
from productos.Producto import Producto
from productos.ProductoAlimenticio import ProductoAlimenticio
from productos.ProductoElectronico import ProductoElectronico
import mysql.connector
from mysql.connector import Error
from decouple import config

class GestionProductos:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user= config('DB_USER')
        self.password=config('DB_PASSWORD')
        self.port = config('DB_PORT')
    
    def connect(self):
        try:
            coneccion = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if coneccion.is_connected():
                return coneccion
        except Error as e:
            print(f'Error al intentar conectar con la base de datos: {e}')
            return None
    # Leer todos los productos de la base de datos.
    def leer_productos(self):
        try:
            coneccion = self.connect()
            
            if coneccion:
                with coneccion.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * from productos')
                    productos_data = cursor.fetchall()
                    
                    productos = []
                    
                    for producto_data in productos_data:
                        codigo_producto = producto_data['codigo_producto']
                        
                        cursor.execute('SELECT fecha_vencimiento, es_libre_gluten FROM productos_alimenticios WHERE codigo_producto = %s', (codigo_producto,))

                        productoAlimenticio = cursor.fetchone()
                        
                        if productoAlimenticio:
                            producto_data['fecha_vencimiento'] = productoAlimenticio['fecha_vencimiento']
                            producto_data['es_libre_gluten'] = productoAlimenticio['es_libre_gluten']
                            producto = ProductoAlimenticio(**producto_data)
                        else:
                            cursor.execute('SELECT color, meses_garantia FROM productos_electronicos WHERE codigo_producto = %s', [codigo_producto,])
                            productoElectronico = cursor.fetchone()
                            producto_data['color'] = productoElectronico['color']
                            producto_data['meses_garantia'] = productoElectronico['meses_garantia']
                            producto = ProductoElectronico(**producto_data)

                        productos.append(producto)
        except Exception as e:
            print(f'Error al mostrar los productos: {e}')
        else: 
            return productos
        finally:
            if coneccion.is_connected():
                coneccion.close()       
        
    
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        except IOError as error:
            print(f"Error al intentar guardar los datos en el archivo: {error}")
        except Exception as error:
            print(f"Error Inesperado: {error}")
    
    # Lee producto por codigo
    def leer_producto(self, codigo_producto):
        try:
            coneccion = self.connect()
            
            if coneccion:
                with coneccion.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * from productos WHERE codigo_producto = %s', [codigo_producto,])
                    producto_data = cursor.fetchone()
                    if producto_data:
                        cursor.execute('SELECT fecha_vencimiento, es_libre_gluten FROM productos_alimenticios WHERE codigo_producto = %s', [codigo_producto,])
                        productoAlimenticio = cursor.fetchone()
                        
                        if productoAlimenticio:
                            producto_data['fecha_vencimiento'] = productoAlimenticio['fecha_vencimiento']
                            producto_data['es_libre_gluten'] = productoAlimenticio['es_libre_gluten']
                            producto = ProductoAlimenticio(**producto_data)
                        else :
                            cursor.execute('SELECT color, meses_garantia FROM productos_electronicos WHERE codigo_producto = %s', [codigo_producto,])
                            productoElectronico = cursor.fetchone()
                            producto_data['color'] = productoElectronico['color']
                            producto_data['meses_garantia'] = productoElectronico['meses_garantia']
                            producto = ProductoElectronico(**producto_data)
                    else:
                        return
                    
                    return producto
        except Exception as e:
            print(f'Error al obtener el producto: {e}')
        finally:
            if coneccion.is_connected():
                coneccion.close()       
    
    # Guardar producto en la base de datos
    def agregar_producto(self, producto):
        try:
            coneccion = self.connect()
            
            if coneccion:
                with coneccion.cursor() as cursor:
                    cursor.execute('INSERT INTO productos (codigo_producto, nombre, precio, stock, marca, categoria) VALUES (%s, %s, %s, %s, %s, %s)', [producto.codigo_producto, producto.nombre, producto.precio, producto.stock, producto.marca, producto.categoria])
                    
                    if isinstance(producto, ProductoAlimenticio):
                        print(producto.es_libre_gluten)
                        input("Esperando....")
                        cursor.execute('INSERT INTO productos_alimenticios (codigo_producto, fecha_vencimiento, es_libre_gluten) VALUES (%s, %s, %s)', [producto.codigo_producto, producto.fecha_vencimiento, producto.es_libre_gluten])
                    else:
                        cursor.execute('INSERT INTO productos_electronicos (codigo_producto, color, meses_garantia) VALUES (%s, %s, %s)', [producto.codigo_producto, producto.color, producto.meses_garantia])
                    
                    coneccion.commit()
                    print('Producto Agregado Correctamente!')
        except Exception as e:
            coneccion.rollback()
            print(f'Error Inesperado al guardar el producto: {e}')
        else:
            return producto
        finally:
            if coneccion.is_connected():
                cursor.close()
                coneccion.close()
        
    
    def eliminar_producto(self, codigo_producto):
        try:
            conneccion = self.connect()
            if conneccion:
            
                with conneccion.cursor() as cursor:
                    cursor.execute('SELECT codigo_producto FROM productos WHERE codigo_producto = %s', [codigo_producto,])
                    
                    if not cursor.fetchone():
                        print(f'No se ha encontrado un producto con el codigo {codigo_producto}')
                        return
                    
                    cursor.execute('DELETE FROM productos_electronicos WHERE codigo_producto = %s', [codigo_producto,])
                    cursor.execute('DELETE FROM productos_alimenticios WHERE codigo_producto = %s', [codigo_producto,])
                    cursor.execute('DELETE FROM productos WHERE codigo_producto = %s', [codigo_producto,])
                    
                    if cursor.rowcount > 0:
                        conneccion.commit()
                        print(f'Producto Elminado correctamente!')
                    else:
                        print(f'No se ha encontrado un producto con el codigo {codigo_producto}')
            
        except Exception as e:
            print(f'Error Inesperado al eliminar producto. {e}')
        finally:
            if conneccion.is_connected():
                conneccion.close()
    
    def actualizar_producto(self, codigo_producto, campo, valor):
        try:
            producto = self.leer_producto(codigo_producto)
            if producto:
                coneccion = self.connect()
                if coneccion:
                    setattr(producto, campo[0], valor)
                    with coneccion.cursor(dictionary=True) as cursor:
                        cursor.execute('UPDATE productos SET nombre = %s, precio = %s, stock = %s, marca = %s, categoria = %s WHERE codigo_producto = %s', [producto.nombre, producto.precio, producto.stock, producto.marca, producto.categoria, producto.codigo_producto])
                        if isinstance(producto, ProductoAlimenticio):
                            cursor.execute('UPDATE productos_alimenticios SET fecha_vencimiento = %s, es_libre_gluten = %s WHERE codigo_producto = %s', [producto.fecha_vencimiento, producto.es_libre_gluten, producto.codigo_producto])
                        else:
                           cursor.execute('UPDATE productos_electronicos SET color = %s, meses_garantia = %s WHERE codigo_producto = %s', [producto.color, producto.meses_garantia, producto.codigo_producto])
                        
                        coneccion.commit()
                pass
            else:
                print(f'No se ha encontrado producto con el codigo {codigo_producto}')
                    
        except Exception as e:
            print(f'Error inesperado al actualizar producto. {e}')
        else:
            return producto
        finally:
            if coneccion.is_connected():
                coneccion.close()
    
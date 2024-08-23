class Producto:
    def __init__(self, codigo_producto, nombre, precio, stock, marca, categoria):
        self.codigo_producto = codigo_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.marca = marca
        self.categoria = categoria
    
    @property
    def codigo_producto(self):
        return self._codigo_producto
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio(self):
        return self._precio
    
    @property
    def stock(self):
        return self._stock
    
    @property
    def marca(self):
        return self._marca
    
    @property
    def categoria(self):
        return self._categoria

    @codigo_producto.setter
    def codigo_producto(self, codigo_producto):
        self._codigo_producto = codigo_producto
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre
    
    @precio.setter
    def precio(self, nuevo_precio): 
        try:
            self._precio = float(nuevo_precio)
        except ValueError as error:
            raise ValueError("El valor del precio ingresado debe ser un numero!")
    
    @stock.setter
    def stock(self, nuevo_stock):
        try:
            self._stock = int(nuevo_stock)
        except ValueError as error:
            raise ValueError("El valor de stock ingresado debe ser un numero entero!")
    
    @marca.setter
    def marca(self, nueva_marca):
        self._marca = nueva_marca
    
    @categoria.setter
    def categoria(self, nueva_categoria):
        self._categoria = nueva_categoria
        
    
    def to_dict(self):
        return {
            "codigo_producto": self.codigo_producto,
            "nombre": self._nombre,
            "precio": self._precio,
            "stock": self._stock,
            "marca": self._marca,
            "categoria": self._categoria
        }
    
    def __str__(self):
        return f"""========== Detalles Producto ==========
Codigo: {self._codigo_producto}
Nombre: {self._nombre}
Precio: {self._precio}
Stock: {self._stock}
Marca: {self._marca}
Categoria: {self._categoria}
"""
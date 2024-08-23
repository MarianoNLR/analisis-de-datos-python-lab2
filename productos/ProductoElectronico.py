from multiprocessing import Value
from productos.Producto import Producto


class ProductoElectronico(Producto): 
    def __init__(self, codigo_producto, nombre, precio, stock, marca, categoria, color, meses_garantia):
        super().__init__(codigo_producto, nombre, precio, stock, marca, categoria)
        self.color = color
        self.meses_garantia = meses_garantia
    
    @property
    def color(self):
        return self._color
    
    @property
    def meses_garantia(self): 
        return self._meses_garantia
    
    @color.setter
    def color(self, color):
        self._color = color
    
    @meses_garantia.setter
    def meses_garantia(self, nuevo_meses_garantia):
        try:
            self._meses_garantia = int(nuevo_meses_garantia)
        except ValueError as error:
            raise ValueError("La cantidad de meses de garantia debe ser un número entero!")
        
    
    
    def to_dict(self):
        data = super().to_dict()
        data["color"] = self.color
        data["meses_garantia"] = self.meses_garantia
        
        return data
    
    def __str__(self):
        return f"""{super().__str__()}Color: {self.color}
Garantia: {self.meses_garantia} (Meses)"""
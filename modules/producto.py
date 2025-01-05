class Producto:
    def __init__(self,id_producto,nombre,precio,color,imagen,cantidad):
        self.id_producto=id_producto
        self.nombre=nombre
        self.precio=precio
        self.color=color
        self.imagen=imagen  
        self.cantidad=cantidad
        
        
    def ProductoDBCollection(self):
        return{
            "id_producto":self.id_producto,
            "nombre":self.nombre,
            "precio":self.precio,
            "color":self.color,
            "imagen":self.imagen,
            "cantidad":self.cantidad,
        }
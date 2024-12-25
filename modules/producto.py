class Producto:
    def __init__(self,id_producto,nombre,precio,color,img,cantidad):
        self.id_producto=id_producto
        self.nombre=nombre
        self.precio=precio
        self.color=color
        self.img=img  
        self.cantidad=cantidad
        
        
    def ProductoDBCollection(self):
        return{
            "id_producto":self.id_producto,
            "nombre":self.nombre,
            "precio":self.precio,
            "color":self.color,
            "img":self.img,
            "cantidad":self.cantidad,
        }
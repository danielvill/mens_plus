class Marca:
    def __init__(self,id_marca,nombre,proveedor,comentario):
        self.id_marca=id_marca
        self.nombre=nombre
        self.proveedor=proveedor
        self.comentario=comentario
        
        
    def MarcaDBCollection(self):
        return{
            "id_marca":self.id_marca,
            "nombre":self.nombre,
            "proveedor":self.proveedor,
            "comentario":self.comentario,
        }
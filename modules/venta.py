class Venta:
    def __init__(self,id_venta,n_cliente,n_apellido,direccion,cedula,fecha,n_productos,color,cantidad,precio,resultado,total):
        self.id_venta=id_venta
        self.n_cliente=n_cliente
        self.n_apellido=n_apellido
        self.direccion=direccion
        self.cedula=cedula
        self.fecha=fecha
        self.n_productos=n_productos
        self.color=color
        self.cantidad=cantidad
        self.precio=precio
        self.resultado=resultado
        self.total=total

        
    def VentaDBCollection(self):
        return{
            'id_venta': self.id_venta,
            'n_cliente': self.n_cliente,
            'n_apellido': self.n_apellido,
            'direccion': self.direccion,
            'cedula': self.cedula,
            'fecha': self.fecha,
            'n_productos': self.n_productos,
            'color': self.color,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'resultado': self.resultado,
            'total': self.total
        }
class Venta:
    def __init__(self,id_venta,n_cliente,n_apellido,direccion,cedula,fecha,hora,n_productos,talla,color,cantidad,precio,resultado,total,usuario):
        self.id_venta=id_venta
        self.n_cliente=n_cliente
        self.n_apellido=n_apellido
        self.direccion=direccion
        self.cedula=cedula
        self.fecha=fecha
        self.hora=hora
        self.n_productos=n_productos
        self.talla=talla
        self.color=color
        self.cantidad=cantidad
        self.precio=precio
        self.resultado=resultado
        self.total=total
        self.usuario=usuario
        
        
    def VentaDBCollection(self):
        return{
            'id_venta': self.id_venta,
            'n_cliente': self.n_cliente,
            'n_apellido': self.n_apellido,
            'direccion': self.direccion,
            'cedula': self.cedula,
            'fecha': self.fecha,
            'hora': self.hora,
            'n_productos': self.n_productos,
            'talla': self.talla,
            'color': self.color,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'resultado': self.resultado,
            'total': self.total,
            'usuario': self.usuario
        }
class Cliente:
    def __init__(self,id_cliente,nombre,apellido,cedula,direccion,telefono,correo):
        self.id_cliente=id_cliente
        self.nombre=nombre
        self.apellido=apellido
        self.cedula=cedula  
        self.direccion=direccion
        self.telefono=telefono
        self.correo=correo
        
    def ClienteDBCollection(self):
        return{
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "correo": self.correo,
        }
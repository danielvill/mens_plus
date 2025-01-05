class Cliente:
    def __init__(self,nombre,apellido,cedula,direccion,telefono,correo):
        
        self.nombre=nombre
        self.apellido=apellido
        self.cedula=cedula  
        self.direccion=direccion
        self.telefono=telefono
        self.correo=correo
        
    def ClienteDBCollection(self):
        return{
            
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "correo": self.correo,
        }
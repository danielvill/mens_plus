class User:
    def __init__(self,user,cedula,contraseña):
        self.user=user
        self.cedula=cedula
        self.contraseña=contraseña
        
        
    def UserDBCollection(self):
        return{
            'user':self.user,
            'cedula':self.cedula,
            'contraseña':self.contraseña,
        }
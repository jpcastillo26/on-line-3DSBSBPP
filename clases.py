class Caja:
    num_cajas=0
    conteo_de_cajas=0
    seq=[]
    def __init__(self, num, dx, dy, dz,posx,posy,posz):
        self.num = num
        self.dx = dx
        self.dy = dy
        self.dz = dz
        # self.seq = seq

        #temp
        self.posx = posx
        self.posy = posy
        self.posz = posz
        self.rot = []
        Caja.conteo_de_cajas += 1
        
    
    @property
    def posx2(self):
        return self.posx + self.dx
    @property
    def posy2(self):
        return self.posy + self.dy
    @property
    def posz2(self):
        return self.posz + self.dz

    def agregar_rotaciones(self,todas=True):
        # self.rot=rot
        
        dx, dy, dz = self.dx, self.dy, self.dz
        #   rot=='y':
            # self.posx=self.posx+self.dx-self.dz
        #TODO mejorar
        if not todas:
            self.rot.append(caja_rot(self.num,dx,dy,dz,self.posx,self.posy,self.posz,0,'zz'))
        else:
            #  original:
            self.rot.append(caja_rot(self.num,dx,dy,dz,self.posx,self.posy,self.posz,0,'zz'))
            #  rot=='y':
            self.rot.append(caja_rot(self.num,dz,dy,dx,self.posx,self.posy,self.posz,1,'y'))
            #  rot=='x':
            self.rot.append(caja_rot(self.num,dx,dz,dy,self.posx,self.posy,self.posz,2,'x'))
            #  rot=='z':
            self.rot.append(caja_rot(self.num,dx,dy,dz,self.posx,self.posy,self.posz,3,'z'))
            #  rot=='yz':
            self.rot.append(caja_rot(self.num,dy,dz,dx,self.posx,self.posy,self.posz,4,'yz'))
            #  rot=='xz':
            self.rot.append(caja_rot(self.num,dz,dx,dy,self.posx,self.posy,self.posz,5,'xz'))
            
        
    def print_rotaciones(self):
        for i in self.rot:
            print('Rotacion:',i.num,i.dx,i.dy,i.dz,i.posx,i.posy,i.posz,i.rot)


    def actualizar_pos(self,x,y,z):
        self.posx, self.posy, self.posz = x, y, z
        for orientacion in self.rot:
            orientacion.posx, orientacion.posy, orientacion.posz = x, y, z

    def __str__(self) -> str:
        return "num:{},dx:{},dy:{},dz:{},posx:{},posy:{},posz:{}".format(self.num,self.dx,self.dy,self.dz,self.posx,self.posy,self.posz)

    #constructor alternativo
    @classmethod
    def from_file(cls,dato):
        num = dato[0]
        dx = dato[1]
        dy = dato[2]
        dz = dato[3]
        posx = 0
        posy=0
        posz=0
        return cls(num, dx, dy, dz,posx,posy,posz)

class caja_rot(Caja):
    def __init__(self, num, dx, dy, dz,posx,posy,posz,rot=0,rot_codigo=None):
        super().__init__(num, dx, dy, dz,posx,posy,posz)
        self.num_rot=rot
        self.rot_codigo=rot_codigo

    def __str__(self) -> str:
        return "num:{},num_rot:{},rot:{},dx:{},dy:{},dz:{},posx:{},posy:{},posz:{}".format(
            self.num,self.num_rot,self.rot_codigo,self.dx,self.dy,self.dz,self.posx,self.posy,self.posz)



class Contenedor:
    dimensiones= [0,0,0]
    def __init__(self,num) -> None:
        self.num=num
        self.cajas=[]
        self.espacios=[]

    

class Esquina:
    def __init__(self,num,x,y,z) -> None:
        self.num=num
        self.x=x
        self.y=y
        self.z=z
        
    @property
    def distX(self):
        return min(Contenedor.dimensiones[0]-self.x,self.x)
    
    @property
    def distY(self):
        return min(Contenedor.dimensiones[1]-self.y,self.y)
    
    def __str__(self) -> str:
        return "({},{},{})".format(self.x,self.y,self.z)


class Espmax:
    dimension= [0,0,0]
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
    
        # self.hijos = []
        self.esquinas=[Esquina(1,x1,y1,z1),Esquina(2,x2,y1,z1),Esquina(3,x1,y2,z1),Esquina(4,x2,y2,z1)]
        # self.esq2=Esquina(x2,y1)
        # self.esq3=Esquina(x1,y2)
        # self.esq4=Esquina(x2,y2)
    

    #constructor alternativo
    @classmethod
    def inic_from_file(cls,dato):
        x1 = 0
        x2 = dato[0]
        y1 = 0
        y2 = dato[1]
        z1 = 0
        z2 = dato[2]
        return cls(x1, x2, y1, y2, z1, z2)
    

    @property
    def dx(self):
        return self.x2-self.x1
    @property
    def dy(self):
        return self.y2-self.y1
    @property
    def dz(self):
        return self.z2-self.z1
    
    

    # def crear_hijo(self,otro):
    #     self.hijos.append(otro)
        
    # def separados(self,otro):
    #     if otro.posx > espacios[0].x2 or espacios[0].x1 > (otro.posx+otro.dx)  or sel.posy > espacios[0].y2 or espacios[0].y1 > (sel.posy+sel.dy):
    #     pass

    # def duplicar(self):
    #     espacios.append(Espmax(self.x1,self.x2,self.y1,self.y2,self.z1,self.z2))

    def unir(self, otro):
        pass
    
    def actualizarEsp():
        pass

    def __str__(self) -> str:
        return "x:{},{} y:{},{} z:{},{}".format(self.x1,self.x2,self.y1,self.y2,self.z1,self.z2)
    def __repr__(self) -> str:
        return "Espmax({},{},{},{},{},{})".format(self.x1,self.x2,self.y1,self.y2,self.z1,self.z2)
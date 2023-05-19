from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
# from matplotlib import colors as mcolors
from clases import Caja
from clases import Espmax
from clases import Contenedor
# import numpy as np
# plt.rcParams['figure.figsize'] = [4, 3]
#genera un color aleatorio
def gen_random_hex_color():
    hex_digits = '0123456789ABCDEF'

    return '#' + ''.join(
        random.choice(hex_digits)
        for _ in range(6)
    )

def plotear2D(elem,largo,ancho,numero=1):
    # Get the current reference
    plt.figure(num=numero)
    plt.plot()
    currentAxis = plt.gca()
    lista={}
    for i in range(0,len(elem)):
        #cajas
        if isinstance(elem[i],Caja):
            currentAxis.add_patch(Rectangle((elem[i].posx, elem[i].posy), elem[i].dx, elem[i].dy,
                                             fill=True,  edgecolor='black', facecolor='#69b422', lw=1, alpha=1))
        #espacios_max
        elif isinstance(elem[i],Espmax):
            currentAxis.add_patch(Rectangle((elem[i].x1, elem[i].y1), elem[i].dx, elem[i].dy,
                                            fill=None, edgecolor='r', alpha=1,))
    plt.xlim([-7,largo+7])
    plt.ylim([-7,ancho+7])
    plt.show()

# def cc(arg):
#     return mcolors.to_rgba(arg, alpha=0.6)

def plotear3D(elem,largo,ancho,alto,multicolor=False,ejes_iguales=False,numero=1):

    fig = plt.figure(num=numero)
    ax = fig.add_subplot(111, projection='3d')
    poly3d=[]
    for i in range(0,len(elem)):
        if isinstance(elem[i],Caja):
            e=elem[i]
            x = [e.posx, e.posx2, e.posx2, e.posx, e.posx, e.posx2, e.posx2, e.posx]
            y = [e.posy, e.posy, e.posy2, e.posy2, e.posy, e.posy, e.posy2, e.posy2]
            z = [e.posz, e.posz, e.posz, e.posz, e.posz2, e.posz2, e.posz2, e.posz2]
            alfa=0.8
            edge='k'

        elif isinstance(elem[i],Espmax):
            e=elem[i]
            x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
            y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
            z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
            alfa=0
            edge='r'

        vertices = [[0,1,2,3], [0,1,5,4], [0,3,7,4], [2,3,7,6], [1,2,6,5], [4,5,6,7]]

        tupleList = list(zip(x, y, z))
        # print(tupleList)

        poly3d =  [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
        if multicolor==True:
            color=gen_random_hex_color()
        else:
            color='#69b422'
        ax.add_collection3d(Poly3DCollection(poly3d, edgecolors=edge, facecolors=color, linewidths=1, alpha=alfa))#zorder=100-i))
        # print(poly3d)
    # ax.scatter(x,y,z)
    #'#69b422'

    if ejes_iguales==False:
        ax.set_xlim(0,largo)
        ax.set_ylim(0,ancho)
        ax.set_zlim(0,alto)
    else:
        ax.set_xlim(0,max(largo,alto,ancho))
        ax.set_ylim(0,max(largo,alto,ancho))
        ax.set_zlim(0,max(largo,alto,ancho))
        # ax.axis('equal')
    
    plt.show()


def visualizar(contenedores,paso=False,contenedor_especifico=None,multicolor=False,ejes_iguales=False,dim=3):
    fig_num=0
    if dim==2:
        demo=[]
        for obj in contenedores[0].cajas:
            demo.append(obj)
        demo.append(contenedores[0].espacios[0])
        for obj in contenedores[0].espacios:
            fig_num+=1
            demo.pop()
            demo.append(obj)
            # logger.debug(obj.esquinas[0].distX)
            plotear2D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],numero=fig_num)
    else:
        if contenedor_especifico is not None:
            demo=[]
            c=contenedor_especifico
            for obj in contenedores[c].cajas:
                demo.append(obj)
            if paso==True:
                demo.append(contenedores[c].espacios[0])
                for obj in contenedores[c].espacios:
                    fig_num+=1
                    demo.pop()
                    demo.append(obj)
                    plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales,fig_num)
            else:
                plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales)
        else:
            for c in range(0,len(contenedores)):
                demo=[]
                fig_num+=1
                for obj in contenedores[c].cajas:
                    demo.append(obj)
                if paso==True:
                    demo.append(contenedores[c].espacios[0])
                    for obj in contenedores[c].espacios:
                        
                        demo.pop()
                        demo.append(obj)
                        plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales,fig_num)
                else:
                    plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales,fig_num)
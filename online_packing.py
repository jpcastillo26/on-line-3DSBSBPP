import numpy as np
from plots import *
from clases import *
from pathlib import Path
import logging


logger = logging.getLogger(__name__)
# logging.basicConfig(filename="sbsbpp.log",filemode='w', level=logging.DEBUG)

cajas=[]
# contenedores[cont]espacios=[]
contenedores=[Contenedor(0)]
unir=True
expandir=True

def cargarArchivo(file_name,demo=False):

    base_path = Path(__file__).parent

    #Modo demo, lee los archivos de prueba WithOutRotation_5_0.txt
    if demo:
        file_path = (base_path / "./Instances/Prueba/{}".format(file_name)).resolve()
        with open(file_path) as f:
            contents = f.read()
        
        contents = contents.splitlines()
    
        for i in range(0,len(contents)):
            contents[i] = contents[i].strip('\n')
            contents[i] = contents[i].strip()
            contents[i] = contents[i].split('\t')
            #convertir cada dato en lista de int
            contents[i] = list(map(int,contents[i]))
            #num de cajas que debe haber
            if i == 0:
                Caja.num_cajas=contents[0][0]
            #tamano del contenedor
            elif i == 1:
                Contenedor.dimensiones = contents[i]
                contenedores[0].espacios.append(Espmax.inic_from_file(contents[i]))
            #crear la caja y agregarla a la lista de cajas
            elif 1 < i < len(contents)-1:
                cajas.append(Caja.from_file(contents[i]))
                cajas[i-2].agregar_rotaciones()
            #crear la secuencia
            else:
                Caja.seq = contents[i]

    # Modo real, lee las instancias oficiales
    else:
        file_path = (base_path / "./Instances/Solutions/Solutions/{}".format(file_name)).resolve()

        logger.info(file_path)
        with open(file_path) as f:
            contents = f.read()

        contents = contents.splitlines()
        
        for i in range(0,len(contents)):
            contents[i] = contents[i].split(' ')
            #convertir cada dato en lista de int
            contents[i] = list(map(int,contents[i]))
            #num de cajas que debe haber
            if i == 0:
                Caja.num_cajas=contents[0][0]
            #tamano del contenedor
            elif i == 1:
                Contenedor.dimensiones = contents[i]
                contenedores[0].espacios.append(Espmax.inic_from_file(contents[i]))
            #crear la caja y agregarla a la lista de cajas
            elif 1 < i < len(contents)-1:
                cajas.append(Caja.from_file(contents[i]))
                cajas[i-2].agregar_rotaciones()
            #crear la secuencia
            else:
                Caja.seq = contents[i]

    # return contents



# TODO optimizar
def unir_esp(cont=0):
    global contenedores
    # logger.debug(contenedores[cont].espacios)
    nuevos_esp=[]
    
    seguir_uniendo=True
    while unir and seguir_uniendo==True:
        seguir_uniendo=False
        i=0
        while i < len(contenedores[cont].espacios):
            resp=False
            # ei=contenedores[cont].espacios[i]
            j=0
            while j < len(contenedores[cont].espacios):
                ei=contenedores[cont].espacios[i]
                ej=contenedores[cont].espacios[j]

                #TODO contenedores[cont].espacios en dos dim
            
                if i != j and ej.z1==ei.z1 and ej.z2==ei.z2:
                    # Unir contenedores[cont].espacios con X iguales y Y diferentes
                    if ej.x1==ei.x1 and ej.x2==ei.x2 and unir:
                        if not (ej.y2<ei.y1 or ej.y1>ei.y2):
                            logger.debug('Match: %s, %s',ej,ei)
                            del contenedores[cont].espacios[j]
                            if i>j: i-=1
                            if j!=0: j-=1
                            nuevos_esp.append(Espmax(ei.x1,ei.x2,min(ej.y1,ei.y1),max(ej.y2,ei.y2),ei.z1,ei.z2))
                            resp, seguir_uniendo=True,True
                            continue

                    # Unir contenedores[cont].espacios con Y iguales y X diferentes
                    elif ej.y1==ei.y1 and ej.y2==ei.y2 and unir:
                        #TODO pueden estar invertidos, hacer mas general para poder eliminar el nuevo loop con seguir_uniendo
                        if not (ej.x2<ei.x1 or ej.x1>ei.x2):
                            logger.debug('Match: %s, %s',ej,ei)
                            del contenedores[cont].espacios[j]
                            if i>j: i-=1
                            if j!=0: j-=1
                            nuevos_esp.append(Espmax(min(ej.x1,ei.x1),max(ej.x2,ei.x2),ei.y1,ei.y2,ei.z1,ei.z2))
                            resp, seguir_uniendo=True,True
                            continue

                    # expandir ej con ei
                    elif ei.x1 <= ej.x1 and ei.x2 >= ej.x2 and expandir:
                        if not (ei.y1 > ej.y2 or ei.y2 < ej.y1):
                            min_y=min(ei.y1,ej.y1)
                            max_y=max(ei.y2,ej.y2)
                            if ej.y1 != min_y or ej.y2 != max_y:
                                logger.debug('Expandiendo %s en Y con %s',ej,ei)
                                contenedores[cont].espacios[j].y1=min_y
                                contenedores[cont].espacios[j].y2=max_y

                    elif ei.y1 <= ej.y1 and ei.y2 >= ej.y2 and expandir:
                        if not (ei.x1 > ej.x2 or ei.x2 < ej.x1):
                            min_x=min(ei.x1,ej.x1)
                            max_x=max(ei.x2,ej.x2)
                            if ej.x1 != min_x or ej.x2 != max_x:
                                logger.debug('Expandiendo %s en X con %s',ej,ei)
                                contenedores[cont].espacios[j].x1=min_x
                                contenedores[cont].espacios[j].x2=max_x

                    # expandir ei con ej
                    elif ei.x1 >= ej.x1 and ei.x2 <= ej.x2 and expandir:
                        if not (ei.y1 > ej.y2 or ei.y2 < ej.y1):
                            min_y=min(ei.y1,ej.y1)
                            max_y=max(ei.y2,ej.y2)
                            if ej.y1 != min_y or ej.y2 != max_y:
                                logger.debug('Expandiendo %s en Y con %s',ei,ej)
                                contenedores[cont].espacios[i].y1=min_y
                                contenedores[cont].espacios[i].y2=max_y

                    elif ei.y1 >= ej.y1 and ei.y2 <= ej.y2 and expandir:
                        if not (ei.x1 > ej.x2 or ei.x2 < ej.x1):
                            min_x=min(ei.x1,ej.x1)
                            max_x=max(ei.x2,ej.x2)
                            if ej.x1 != min_x or ej.x2 != max_x:
                                logger.debug('Expandiendo %s en X con %s',ei,ej)
                                contenedores[cont].espacios[i].x1=min_x
                                contenedores[cont].espacios[i].x2=max_x

                    
                j+=1

            if resp == False:
                nuevos_esp.append(ei)
            i+=1

        # print('Nueva lista de espacios:',nuevos_esp)
        # print('\n')          
        contenedores[cont].espacios=nuevos_esp
        nuevos_esp=[]
    logger.debug('Nueva lista de espacios: %s',contenedores[cont].espacios)
        

def caja_espacio_inter(caja_sel,esp):
    if caja_sel.posx >= esp.x2 or esp.x1 >= caja_sel.posx2  or caja_sel.posy >= esp.y2 or esp.y1 >= caja_sel.posy2:
        return False
    else:
        return True

def caja_cabe_en_esp(caja_sel,esp):
    if caja_sel.dx<=esp.dx and caja_sel.dy<=esp.dy and caja_sel.dz<=esp.dz:
        return True
    else:
        return False
    

def ponerCaja(caja_sel,x,y,z,cont=0):
    global contenedores
    temp=[]


    # caja_sel.posx, caja_sel.posy, caja_sel.posz = x, y, z
    cajas[caja_sel.num].actualizar_pos(x,y,z)

    # TODO buscar en caja_rot y retornarla, es el nuevo indice
    
    contenedores[cont].cajas.append(caja_sel)
    logger.debug('Poniendo caja %s',caja_sel)
    for i in range(0,len(contenedores[cont].espacios)):
        esp=contenedores[cont].espacios[i]
        # print(esp)

        if caja_espacio_inter(caja_sel,esp) == True:
            if caja_sel.posx2 > esp.x1 and caja_sel.posx2 < esp.x2: #refinar
                nuevo = Espmax(caja_sel.posx2,esp.x2,esp.y1,esp.y2,esp.z1,esp.z2)
                temp.append(nuevo)

            #puede fallar si la caja ocupa toda una dimension
            if caja_sel.posy2 > esp.y1 and caja_sel.posy2 < esp.y2: #refinar
                nuevo= Espmax(esp.x1,esp.x2,caja_sel.posy2,esp.y2,esp.z1,esp.z2)
                temp.append(nuevo)
            
            if caja_sel.posx < esp.x2 and caja_sel.posx > esp.x1 and caja_sel.posx != 0: #refinar
                nuevo = Espmax(esp.x1,caja_sel.posx,esp.y1,esp.y2,esp.z1,esp.z2)
                temp.append(nuevo)

            if caja_sel.posy < esp.y2 and caja_sel.posy > esp.y1 and caja_sel.posy != 0: #refinar
                nuevo= Espmax(esp.x1,esp.x2,esp.y1,caja_sel.posy,esp.z1,esp.z2)
                temp.append(nuevo)

        else:
            temp.append(esp)
    #espacio encima de la caja
    if caja_sel.posz2 != esp.z2:
        esp_encima= Espmax(caja_sel.posx,caja_sel.posx2,caja_sel.posy,caja_sel.posy2,caja_sel.posz2,esp.z2)
        temp.append(esp_encima)
    contenedores[cont].espacios=temp
    temp=[]
    unir_esp(cont)
            

def first_corner(esp):
    # closest_corner=[]
    # for i in range(0,len(contenedores[cont].espacios)):
        # esp=contenedores[cont].espacios[i]
        
    fc=esp.esquinas[0]
    fc_dist=fc.distX+fc.distY
    for j in range(0,4):
        if (esp.esquinas[j].distX + esp.esquinas[j].distY) < fc_dist:
            fc=esp.esquinas[j]
            fc_dist=esp.esquinas[j].distX+esp.esquinas[j].distY

    # closest_corner.append([i,fc_num,fc_dist])
        
    # print('Esquinas:',closest_corner)
    # closest_corner.sort(key=lambda x: x[2])
    # print('Esquinas ordenadas:',closest_corner)
    return fc


def worstFit(caja_sel,cont=0):
    diff=[]
    for i in range(len(contenedores[cont].espacios)):
        ei=contenedores[cont].espacios[i]
        if caja_cabe_en_esp(caja_sel,ei):
            diff.append(tuple((i,caja_sel.num,caja_sel.num_rot,ei.vol-caja_sel.vol)))

    if diff: logger.debug('Lista de espacios: %s',diff)
    # diff.sort(key=lambda x: x[1],reverse=True)
    # logger.debug('Lista ordenada: %s',diff)s

    return diff

def bestFit(caja_sel,cont=0):
    diff=[]
    for i in range(len(contenedores[cont].espacios)):
        ei=contenedores[cont].espacios[i]
        if caja_cabe_en_esp(caja_sel,ei):
            # espacio, numero de caja, num de rotacion, distancia a los bordes
            diff.append(tuple((i,caja_sel.num,caja_sel.num_rot,ei.vol-caja_sel.vol)))

    if diff: logger.debug('Lista de espacios: %s',diff)
    # diff.sort(key=lambda x: x[1],reverse=False)
    # logger.debug('Lista ordenada: %s',diff)

    return diff

# Es el mismo metodo que esta en plot, este solo esta para compatibilidad o pruebas pero no se nesecita
def viz_paso_a_paso(paso=True,contenedor=None,multicolor=False,ejes_iguales=False,dim=3):
    global contenedores
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
            logger.debug(obj.esquinas[0].distX)
            plotear2D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],numero=fig_num)
    else:
        if contenedor is not None:
            demo=[]
            c=contenedor
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


def porcentaje_ocupacion(contenedores):
    xs,ys,zs=[],[],[]
    for cont in contenedores:
        for caja_sel in cont.cajas:
            xs.append(caja_sel.dx)
            ys.append(caja_sel.dy)
            zs.append(caja_sel.dz)
    np_xs=np.array(xs)
    np_ys=np.array(ys)
    np_zs=np.array(zs)
    D = np.random.random((5, 333))
    occup=(np_xs*np_ys).dot(np_zs)
    total=len(contenedores)*Contenedor.dimensiones[0]*Contenedor.dimensiones[1]*Contenedor.dimensiones[2]
    return occup/total


# La condicion all_rotaciones anula las demas rotaciones
def bin_packing(metodo,instancia,num_cajas=None,rot_x=False,rot_y=False,rot_z=False,all_rotaciones=False,unir_esp=True,expandir_esp=True,modo_demo=False,viz=False,p_occup=False):
    global unir
    global expandir
    global contenedores
    contenedores.clear()
    contenedores=[Contenedor(0)]
    cajas.clear()
    cargarArchivo(instancia,demo=modo_demo)
    
    unir=unir_esp
    expandir=expandir_esp
    
    if num_cajas is None:
        num_cajas=Caja.num_cajas
    
    for indice in range(num_cajas):
        i=Caja.seq[indice]
        cupo=False
        
        # cajas[i].print_rotaciones()

        #TODO completar comb
        #TODO tener en cuenta el orden
        if not (rot_x or rot_y or rot_z):r=0
        elif rot_y and not (rot_x or rot_z):r=1
        elif rot_x and not (rot_y or rot_z):r=2
        elif rot_z and not (rot_x or rot_y):r=3
        elif (rot_y and rot_z and not rot_x) or (rot_x and rot_y and not rot_z):r=4
        elif rot_x and rot_z and not rot_y:r=5
        
        lista_ord=[]

        # ------ Fist Fit en los contenedores ------
        for c in range(len(contenedores)):

            if all_rotaciones:
                rango_inf=0
                rango_sup=6
            elif r != 0:
                rango_inf=r
                rango_sup=r+1
            else:
                rango_inf=0
                rango_sup=1

            if metodo=="best fit":
                for j in range(rango_inf,rango_sup):

                    lista=bestFit(cajas[i].rot[j],c)

                    for ii in lista:
                        lista_ord.append(ii)
   
                if lista_ord:
                    logger.debug('Lista de espacios: %s',lista_ord)
                    lista_ord.sort(key=lambda x: x[3],reverse=False)
                    logger.debug('Lista ordenada: %s',lista_ord)

            elif metodo=="worst fit":
                for j in range(rango_inf,rango_sup):

                    lista=worstFit(cajas[i].rot[j],c)

                    for ii in lista:
                        lista_ord.append(ii)

                if lista_ord: 
                    logger.debug('Lista de espacios: %s',lista_ord)
                    lista_ord.sort(key=lambda x: x[3],reverse=True)
                    logger.debug('Lista ordenada: %s',lista_ord)

            else:
                raise ValueError("El metodo seleccionado no es correcto")
            
            if len(lista_ord)>0:
                cupo=True
                break
        
        
        # si no cabe crear un nuevo contenedor
        if cupo==False:
            x2,y2,z2= Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2]
            contenedores.append(Contenedor(c+1))
            contenedores[c+1].espacios.append(Espmax(0,x2,0,y2,0,z2))
            if metodo=="best fit":
                lista_ord=bestFit(cajas[i].rot[r],c+1)
            if metodo=="worst fit":
                lista_ord=worstFit(cajas[i].rot[r],c+1)
            c=c+1
            del x2,y2,z2

        caja_rotada=cajas[i].rot[lista_ord[0][2]]

        ej=contenedores[c].espacios[lista_ord[0][0]]

        # Busca la esquina mas cercana a las paredes del cont y coloca la caja ahi
        fc=first_corner(ej)
        num_esq=fc.num
        num_esp=lista_ord[0][0]

        if num_esq==2:
            x,y,z = fc.x-caja_rotada.dx, fc.y, fc.z

        elif num_esq==3:
            x,y,z = fc.x, fc.y-caja_rotada.dy, fc.z

        elif num_esq==4:
            x,y,z = fc.x-caja_rotada.dx, fc.y-caja_rotada.dy, fc.z

        else:
            x,y,z = fc.x, fc.y, fc.z


        logger.debug('Espacio: %s Esquina: %s -> %s',num_esp,num_esq,fc)
        ponerCaja(caja_rotada,x,y,z,c)

        
    if viz:
        visualizar(contenedores,ejes_iguales=True)
    # print("\n") 
    if p_occup:
        p_occupacion=porcentaje_ocupacion(contenedores)
    else: p_occupacion=0
    
    return len(contenedores),p_occupacion

# bin_packing("worst fit",instancia='WithOutRotation_5_0.txt',all_rotaciones=True,num_cajas=400,rot_x=True,rot_y=True,rot_z=False,unir_esp=True,expandir_esp=True,modo_demo=True,viz=True,p_occup=True)
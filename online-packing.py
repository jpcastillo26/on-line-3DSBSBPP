# import numpy as np
# # import random
# import pandas as pd
from plots import *
from clases import *
from pathlib import Path


cajas=[]
# contenedores[cont]espacios=[]
contenedores=[Contenedor(0)]
temp=[]
unir=True
expandir=True

def cargarArchivo(file_name):

    # with open('C:\\Users\juanp\OneDrive - Universidad de los andes\PG2\Instances\WithOutRotation_5_0.txt') as f:
    base_path = Path(__file__).parent
    file_path = (base_path / "./Instances/{}".format(file_name)).resolve()
    # print(file_path)
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
            Caja.num_cajas=contents[0]
        #tamano del contenedor
        elif i == 1:
            Contenedor.dimensiones = contents[i]
            # Espmax.dimension = contents[i]
            # Esquina.dimensiones = contents[i]
            contenedores[0].espacios.append(Espmax.inic_from_file(contents[i]))
        #crear la caja y agregarla a la lista de cajas
        elif i>1 and i<len(contents)-1:
            cajas.append(Caja.from_file(contents[i]))
        #crear la secuencia
        else:
            Caja.seq = contents[i]

    # return contents



# TODO expandir contenedores[cont].espacios
# TODO optimizar
def unir_esp(cont=0):
    global contenedores
    # print(contenedores[cont].espacios)
    nuevos_esp=[]
    
    seguir_uniendo=True
    while unir and seguir_uniendo==True:
        seguir_uniendo=False
        i=0
        while i < len(contenedores[cont].espacios):
            resp=False
            ei=contenedores[cont].espacios[i]
            j=0
            while j < len(contenedores[cont].espacios):
                ej=contenedores[cont].espacios[j]

                #TODO contenedores[cont].espacios en dos dim
            
                if i != j and ej.z1==ei.z1 and ej.z2==ei.z2:
                    # Unir contenedores[cont].espacios con X iguales y Y diferentes
                    if ej.x1==ei.x1 and ej.x2==ei.x2 and unir:
                        if not (ej.y2<ei.y1 or ej.y1>ei.y2):
                            print('Match',ej,ei)
                            del contenedores[cont].espacios[j]
                            j = j-1
                            nuevos_esp.append(Espmax(ei.x1,ei.x2,min(ej.y1,ei.y1),max(ej.y2,ei.y2),ei.z1,ei.z2))
                            resp, seguir_uniendo=True,True

                    # Unir contenedores[cont].espacios con Y iguales y X diferentes
                    elif ej.y1==ei.y1 and ej.y2==ei.y2 and unir:
                        #TODO pueden estar invertidos, hacer mas general para poder eliminar el nuevo loop con seguir_uniendo
                        if not (ej.x2<ei.x1 or ej.x1>ei.x2):
                            print('Match',ej,ei)
                            del contenedores[cont].espacios[j]
                            j = j-1
                            nuevos_esp.append(Espmax(min(ej.x1,ei.x1),max(ej.x2,ei.x2),ei.y1,ei.y2,ei.z1,ei.z2))
                            resp, seguir_uniendo=True,True

                    # expandir ej con ei
                    elif ei.x1 <= ej.x1 and ei.x2 >= ej.x2 and expandir:
                        if not (ei.y1 > ej.y2 or ei.y2 < ej.y1):
                            min_y=min(ei.y1,ej.y1)
                            max_y=max(ei.y2,ej.y2)
                            if ej.y1 != min_y or ej.y2 != max_y:
                                print('Expandiendo',ej,'en Y con',ei)
                                contenedores[cont].espacios[j].y1=min_y
                                contenedores[cont].espacios[j].y2=max_y

                    elif ei.y1 <= ej.y1 and ei.y2 >= ej.y2 and expandir:
                        if not (ei.x1 > ej.x2 or ei.x2 < ej.x1):
                            min_x=min(ei.x1,ej.x1)
                            max_x=max(ei.x2,ej.x2)
                            if ej.x1 != min_x or ej.x2 != max_x:
                                print('Expandiendo',ej,'en X con',ei)
                                contenedores[cont].espacios[j].x1=min_x
                                contenedores[cont].espacios[j].x2=max_x

                    # expandir ei con ej
                    elif ei.x1 >= ej.x1 and ei.x2 <= ej.x2 and expandir:
                        if not (ei.y1 > ej.y2 or ei.y2 < ej.y1):
                            min_y=min(ei.y1,ej.y1)
                            max_y=max(ei.y2,ej.y2)
                            if ej.y1 != min_y or ej.y2 != max_y:
                                print('Expandiendo',ei,'en Y con',ej)
                                contenedores[cont].espacios[i].y1=min_y
                                contenedores[cont].espacios[i].y2=max_y

                    elif ei.y1 >= ej.y1 and ei.y2 <= ej.y2 and expandir:
                        if not (ei.x1 > ej.x2 or ei.x2 < ej.x1):
                            min_x=min(ei.x1,ej.x1)
                            max_x=max(ei.x2,ej.x2)
                            if ej.x1 != min_x or ej.x2 != max_x:
                                print('Expandiendo',ei,'en X con',ej)
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
    print('Nueva lista de espacios:',contenedores[cont].espacios)
        
def juntar_esp():
    pass

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
    
# def distancia_borde_espacio(caja_sel,esp,esq):
#     # print('Espacio:',j,'Esquina:',num_esq,'->',fc)
#     if num_esq==1:
#         esp

#         ponerCaja(cajas[i],fc.x-cajas[i].dx,fc.y,fc.z)
#     elif num_esq==2:
#         ponerCaja(cajas[i],fc.x,fc.y-cajas[i].dy,fc.z)
#     elif num_esq==3:
#         ponerCaja(cajas[i],fc.x-cajas[i].dx,fc.y-cajas[i].dy,fc.z)
#     else:
#     #Si la mejor esquina esta a la derecha la caja se pondra fuera del cont
#         ponerCaja(cajas[i],fc.x,fc.y,fc.z)
#     pass


# print('cajas esperadas:' + str(caja.num_cajas[0]))
# print('cajas creadas:' + str(caja.num_cajas_act))
# # print(caja.seq)
# print('dimensiones contenedor:' + str(Espmax.dim0))

def ponerCaja(caja_sel,x,y,z,cont=0):
    global contenedores
    global temp
    # print(rot)
    #TODO checkear si ya hay una caja ahi o solo poner dentro del espacio
    #TODO checkear si la caja entra en los limites del contenedor o del espacio

    # TODO rotar caja
    # if rot != None:
    #     rotar_caja(caja_sel,rot)
    

    # caja_sel.posx, caja_sel.posy, caja_sel.posz = x, y, z
    cajas[caja_sel.num].actualizar_pos(x,y,z)

    # TODO buscar en caja_rot y retornarla, es el nuevo indice
    
    contenedores[cont].cajas.append(caja_sel)
    print('Poniendo caja',caja_sel)
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


def bestFit(caja_sel,cont=0):

    diff=[]
    #TODO que pasa si no hay nigun espacio
    for i in range(0,len(contenedores[cont].espacios)):
        ei=contenedores[cont].espacios[i]
        if caja_cabe_en_esp(caja_sel,ei):
            diff.append([i,abs(caja_sel.dy-ei.dy)+abs(caja_sel.dx-ei.dx)])

    print('Lista de espacios:',diff)
    diff.sort(key=lambda x: x[1],reverse=True)
    print('Lista ordenada:',diff)

    # abs(esp.dx-caja_sel)
    return diff

def worstFit(caja_sel,cont=0):

    diff=[]
    #TODO que pasa si no hay nigun espacio
    for i in range(0,len(contenedores[cont].espacios)):
        ei=contenedores[cont].espacios[i]
        if caja_cabe_en_esp(caja_sel,ei):
            diff.append([i,abs(caja_sel.dy-ei.dy)+abs(caja_sel.dx-ei.dx)])

    print('Lista de espacios:',diff)
    diff.sort(key=lambda x: x[1],reverse=False)
    print('Lista ordenada:',diff)

    # abs(esp.dx-caja_sel)
    return diff

def viz_paso_a_paso(vf=True,contenedor=None,multicolor=False,ejes_iguales=False):
    global contenedores
    
    
    if contenedor is not None:
        demo=[]
        c=contenedor
        for obj in contenedores[c].cajas:
                demo.append(obj)
        if vf==True:
            demo.append(contenedores[c].espacios[0])
            for obj in contenedores[c].espacios:
                demo.pop()
                demo.append(obj)
                plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales)
        else:
            plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales)
    else:
        for c in range(0,len(contenedores)):
            demo=[]
            for obj in contenedores[c].cajas:
                    demo.append(obj)
            if vf==True:
                demo.append(contenedores[c].espacios[0])
                for obj in contenedores[c].espacios:
                    demo.pop()
                    demo.append(obj)
                    plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales)
            else:
                plotear3D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1],Contenedor.dimensiones[2],multicolor,ejes_iguales)

def bin_packing(metodo,instancia,num_cajas=None,rot_x=False,rot_y=False,rot_z=False,unir_esp=True,expandir_esp=True):
    global unir
    global expandir
    cargarArchivo(instancia)
    unir=unir_esp
    expandir=expandir_esp
    if num_cajas is None:
        num_cajas=Caja.num_cajas[0]
    

    for indice in range(0,num_cajas):
        i=Caja.seq[indice]
        #55
        cupo=False
        #revisar si cabe en el espacio
        #TODO diccionario con cada espacio y su equina mas cercana a los bordes (combinaciones)
        #TODO retornar lista ordenada con los contenedores[cont].espacios con esquinas mas cercanas
        
        cajas[i].agregar_rotaciones()
        cajas[i].print_rotaciones()

        #TODO completar comb
        #TODO tener en cuenta el orden
        if not (rot_x or rot_y or rot_z):r=0
        elif rot_y and not (rot_x or rot_z):r=1
        elif rot_x and not (rot_y or rot_z):r=2
        elif rot_z and not (rot_x or rot_y):r=3
        elif (rot_y and rot_z and not rot_x) or (rot_x and rot_y and not rot_z):r=4
        elif rot_x and rot_z and not rot_y:r=5
        
        caja_rotada=cajas[i].rot[r]
        for c in range(0,len(contenedores)):
            if metodo=="best fit":
                lista_ord=bestFit(caja_rotada,c)
            elif metodo=="worst fit":
                lista_ord=worstFit(caja_rotada,c)
            else:
                raise ValueError("El metodo seleccionado no es correcto")
            if len(lista_ord)>0:
                cupo=True
                break

        if cupo==False:
            x2= Contenedor.dimensiones[0]
            y2= Contenedor.dimensiones[1]
            z2= Contenedor.dimensiones[2]
            contenedores.append(Contenedor(c+1))
            contenedores[c+1].espacios.append(Espmax(0,x2,0,y2,0,z2))
            lista_ord=[[0,0]]
            c=c+1
            del x2,y2,z2

        for j in range(0,len(lista_ord)):
            ej=contenedores[c].espacios[lista_ord[j][0]]
            # num_esq=first_corner(ej)
            fc=first_corner(ej)
            # num_esq=first_corner(ej).num

            num_esq=fc.num
            if num_esq==2:
                x,y,z = fc.x-caja_rotada.dx, fc.y, fc.z

            elif num_esq==3:
                x,y,z = fc.x, fc.y-caja_rotada.dy, fc.z

            elif num_esq==4:
                x,y,z = fc.x-caja_rotada.dx, fc.y-caja_rotada.dy, fc.z

            else:
                x,y,z = fc.x, fc.y, fc.z

            # if caja_cabe_en_esp(caja_rotada,ej): #and contenedores[cont].espacios[j].z1==0:
            #     cupo=True

            print('Espacio:',j,'Esquina:',num_esq,'->',fc)
            ponerCaja(caja_rotada,x,y,z,c)

            print('\n')
            break
                
        
        #TODO si la caja no cabe colocarla en otro contenedor
        # if cupo==False:
        #     print("no cabe")
        #     continue
        
        # viz_paso_a_paso(ejes_iguales=True)

# cargarArchivo('WithOutRotation_5_0.txt')

#-------------------------------------------------------
#---------------        Pruebas         ----------------
#-------------------------------------------------------



bin_packing("worst fit",instancia='WithOutRotation_5_0.txt',rot_x=True,rot_y=False,rot_z=True,unir_esp=True,expandir_esp=True)


viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)

print("Las cajas caben en:",len(contenedores),"contenedores","\n")







# ---------- rotaciones ------------------
# cajas[30].agregar_rotaciones()
# ponerCaja(cajas[30],0,0,0)
# ponerCaja(cajas[74],0,100-35,0)
# cajas[74].agregar_rotaciones()
# cajas[75].agregar_rotaciones()
# ponerCaja(cajas[75],120-48,0,0)
# ponerCaja(cajas[76],120-48,100-35,0)

# # # # #demo 3d
# # # ponerCaja(caja(100,25,38,16,5,5,16),5,5,16)
# # # ponerCaja(caja(101,20,33,16,0,0,0),5,5,32)
# # # ponerCaja(caja(102,15,25,16,0,0,0),5,5,48)
# # # ponerCaja(caja(103,10,20,16,0,0,0),5,5,64)

# first_corner()
# ponerCaja(cajas[30],0,0,0)
# first_corner()
# paso_a_paso()

# ponerCaja(cajas[74],0,100-35,0)
# first_corner()
# paso_a_paso()

# ponerCaja(cajas[75],120-48,0,0)
# first_corner()
# paso_a_paso()


# #----------- Caso 2D --------------
# demo.append(contenedores[cont].espacios[0])
# for obj in contenedores[cont].espacios:
#     demo.pop()
#     demo.append(obj)
#     print(obj.esquinas[0].distX)
#     plotear2D(demo,Contenedor.dimensiones[0],Contenedor.dimensiones[1])#,Contenedor.dimensiones[2])


# cajas[30].print_rotaciones()
# cajas[74].print_rotaciones()
# cajas[75].print_rotaciones()
# cajas[76].print_rotaciones()



#------------ Error ESPMAX ------------

# for i in range(0,3):

#     for e in range(0,4):
#         BF=contenedores[cont].espacios[0].esquinas[0]
#         if contenedores[cont].espacios[0].esquinas[e].distX < BF.distX:
#             BF=contenedores[cont].espacios[0].esquinas[e]
        
    
#     ponerCaja(cajas[i],BF.x,BF.y,0)


#woodboxall1 poner 7 cajas
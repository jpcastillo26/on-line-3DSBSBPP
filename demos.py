from online_packing import *
from plots import *
from clases import *
from pathlib import Path
import os
from time import perf_counter
from statistics import mean

#-------------------------------------------------------
#---------------        Pruebas         ----------------
#-------------------------------------------------------



# bin_packing("worst fit",instancia='WithOutRotation_5_0.txt',rot_x=True,rot_y=False,rot_z=True,unir_esp=True,expandir_esp=True)


# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)

# print("Las cajas caben en:",len(contenedores),"contenedores","\n")

# Demo 0
# cargarArchivo('WithOutRotation_5_0.txt')
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)

# Demo 1
# cargarArchivo('WithOutRotation_5_0.txt')
# cajas[30]=Caja(30,40,40,20,0,0,0)
# ponerCaja(cajas[30],40,30,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)

# Demo 2
# cargarArchivo('WithOutRotation_5_0.txt')
# ponerCaja(cajas[30],0,0,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)
# ponerCaja(cajas[75],120-48,0,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)

# demo 3
# cargarArchivo('WithOutRotation_5_0.txt')
# unir=True
# expandir=True
# ponerCaja(cajas[30],0,0,0)
# # viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)
# ponerCaja(cajas[74],0,100-35,0)
# # viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)
# ponerCaja(cajas[75],120-48,0,0)
# # viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)
# # ponerCaja(cajas[76],120-48,100-35,0)
# ponerCaja(cajas[31],120-34,100-48,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=True,dim=2)

# demo 4
# cargarArchivo('WithOutRotation_5_0.txt')
# ponerCaja(cajas[30],0,0,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=False)
# ponerCaja(cajas[74],0,100-35,0)
# ponerCaja(cajas[75],120-48,0,0)
# ponerCaja(cajas[76],120-48,100-35,0)
# viz_paso_a_paso(True,multicolor=False,ejes_iguales=False)

# demo 5
# bin_packing("best fit",instancia='WithOutRotation_5_0.txt',num_cajas=2,rot_x=True,rot_y=False,rot_z=False,unir_esp=True,expandir_esp=True)
# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)
# reiniciar()
# bin_packing("best fit",instancia='WithOutRotation_5_0.txt',num_cajas=2,rot_x=False,rot_y=True,rot_z=False,unir_esp=True,expandir_esp=True)
# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)
# reiniciar()
# bin_packing("best fit",instancia='WithOutRotation_5_0.txt',num_cajas=2,rot_x=False,rot_y=False,rot_z=True,unir_esp=True,expandir_esp=True)
# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)
# reiniciar()
# bin_packing("best fit",instancia='WithOutRotation_5_0.txt',num_cajas=2,rot_x=True,rot_y=True,rot_z=False,unir_esp=True,expandir_esp=True)
# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)
# reiniciar()
# bin_packing("best fit",instancia='WithOutRotation_5_0.txt',num_cajas=2,rot_x=True,rot_y=False,rot_z=True,unir_esp=True,expandir_esp=True)
# viz_paso_a_paso(False,multicolor=False,ejes_iguales=True)

# with open('C:\\Users\juanp\OneDrive - Universidad de los andes\PG2\Instances\WithOutRotation_5_0.txt') as f:
base_path = Path(__file__).parent
# file_path = (base_path / "./Instances/{}".format(file_name)).resolve()
# print(file_path)
# folder path
dir_path = (base_path / "./Instances/Solutions/Solutions/").resolve()
# dir_path = r'E:\\account\\'

# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
# print(res)

resultado=[]
t1_start = perf_counter()

for file_name in res:
    fl=file_name.split("_")[0]
    end=file_name.split("_")[4]
    N_items=int(end[:-4])
    
    if fl.count('I') == 1 and N_items==20:
        num=int(fl.replace('I',''))
        if num<50:
            print(fl,N_items)

            resultado.append(bin_packing("worst fit",instancia=file_name))

            # f"Las cajas caben en: {len(contenedores)} contenedores"
t1_stop = perf_counter()

print("Tiempo de procesamiento:",t1_stop-t1_start)

print(resultado)
avg=mean(resultado)
print(avg)
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
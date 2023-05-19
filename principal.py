from online_packing import *
from plots import *
from clases import *
from pathlib import Path
import os
from time import perf_counter
from statistics import mean
import logging

# Solo poner en DEBUG si son muy pocas instancias!!!
logging.basicConfig(filename="sbsbpp.log",filemode='w', level=logging.INFO)

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





#-------------------------------------------------------
#---------------      Resultados        ----------------
#-------------------------------------------------------

# with open('C:\\Users\juanp\OneDrive - Universidad de los andes\PG2\Instances\WithOutRotation_5_0.txt') as f:
base_path = Path(__file__).parent
# file_path = (base_path / "./Instances/{}".format(file_name)).resolve()
# print(file_path)
# folder path
dir_path = (base_path / "./Instances/Solutions/Solutions/").resolve()


# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
# print(res)


tipo_I_20=[]
tipo_I_40=[]
tipo_I_60=[]
tipo_I_80=[]
tipo_I_1000=[]
tipo_II_20=[]
tipo_II_40=[]
tipo_II_60=[]
tipo_II_80=[]
tipo_II_1000=[]
tipo_III_20=[]
tipo_III_40=[]
tipo_III_60=[]
tipo_III_80=[]
tipo_III_1000=[]
tipo_IV_40=[]
tipo_IV_1000=[]

archivos_agrupados=[]

for file_name in res:
    tipo=file_name.split("_")[0]
    N_items=int(file_name.split("_")[4][:-4])
    
    if tipo.count('I') == 1 and tipo.count('V') == 0:
        if N_items==20:
            tipo_I_20.append(file_name)
        elif N_items==40:
            tipo_I_40.append(file_name)
        elif N_items==60:
            tipo_I_60.append(file_name)
        elif N_items==80:
            tipo_I_80.append(file_name)
        elif N_items==1000:
            tipo_I_1000.append(file_name)
        else:
            raise ValueError("Error leyendo las instancias")

    elif tipo.count('I') == 2 and tipo.count('V') == 0:
        if N_items==20:
            tipo_II_20.append(file_name)
        elif N_items==40:
            tipo_II_40.append(file_name)
        elif N_items==60:
            tipo_II_60.append(file_name)
        elif N_items==80:
            tipo_II_80.append(file_name)
        elif N_items==1000:
            tipo_II_1000.append(file_name)
        else:
            raise ValueError("Error leyendo las instancias")

    elif tipo.count('I') == 3 and tipo.count('V') == 0:
        if N_items==20:
            tipo_III_20.append(file_name)
        elif N_items==40:
            tipo_III_40.append(file_name)
        elif N_items==60:
            tipo_III_60.append(file_name)
        elif N_items==80:
            tipo_III_80.append(file_name)
        elif N_items==1000:
            tipo_III_1000.append(file_name)
        else:
            raise ValueError("Error leyendo las instancias")

    elif tipo.count('V') == 1:
        if N_items==40:
            tipo_IV_40.append(file_name)
        elif N_items==1000:
            tipo_IV_1000.append(file_name)
        else:
            raise ValueError("Error leyendo las instancias")

# if fn.count('I') == 1 and N_items==20:
#     num=int(fl.replace('I',''))
#     if num<50:
#         print(fl,N_items)
#         resultado.append(bin_packing("worst fit",instancia=file_name))
#         # f"Las cajas caben en: {len(contenedores)} contenedores"


archivos_agrupados.append(tipo_I_20)
archivos_agrupados.append(tipo_I_40)
archivos_agrupados.append(tipo_I_60)
archivos_agrupados.append(tipo_I_80)
archivos_agrupados.append(tipo_I_1000)
archivos_agrupados.append(tipo_II_20)
archivos_agrupados.append(tipo_II_40)
archivos_agrupados.append(tipo_II_60)
archivos_agrupados.append(tipo_II_80)
archivos_agrupados.append(tipo_II_1000)
archivos_agrupados.append(tipo_III_20)
archivos_agrupados.append(tipo_III_40)
archivos_agrupados.append(tipo_III_60)
archivos_agrupados.append(tipo_III_80)
archivos_agrupados.append(tipo_III_1000)
archivos_agrupados.append(tipo_IV_40)
archivos_agrupados.append(tipo_IV_1000)

del tipo_I_20
del tipo_I_40
del tipo_I_60
del tipo_I_80
del tipo_I_1000
del tipo_II_20
del tipo_II_40
del tipo_II_60
del tipo_II_80
del tipo_II_1000
del tipo_III_20
del tipo_III_40
del tipo_III_60
del tipo_III_80
del tipo_III_1000
del tipo_IV_40
del tipo_IV_1000

resultados={'avg num contenedores':[],'tiempo':[]}
for data_set in archivos_agrupados:
    num_contenedores=[]
    t1_start = perf_counter()

    for archivo_instancia in data_set:
        #revisar en 20
        num_contenedores.append(bin_packing("worst fit",instancia=archivo_instancia))

    t1_stop = perf_counter()
    tiempo=t1_stop-t1_start
    print("Tiempo de procesamiento:",tiempo)

    avg=mean(num_contenedores)

    resultados['avg num contenedores'].append(avg)
    resultados['tiempo'].append(tiempo)

# pr=bin_packing("best fit",instancia='I1_30_30_30_1000.txt')
# viz_paso_a_paso(False)
# print(pr)
# # print(archivos_agrupados)
print(resultados)


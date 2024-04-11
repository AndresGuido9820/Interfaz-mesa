import os
import numpy as np

def leer_archivo(nombre):
    carpeta_archivos = 'Archivos_sismos'
    ruta_carpeta = os.path.join(os.getcwd(), carpeta_archivos)
    
    nombre_archivo = nombre


    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
    
   
# Verificar si el archivo existe
    if os.path.exists(ruta_archivo):
    # Leer el archivo AT2
        with open(ruta_archivo, 'r') as archivo:
        # Saltar las primeras 3 líneas
            for _ in range(4):
             next(archivo)
        
       
            datos_aceleracion = []
            for linea in archivo:
               
                values = [float(value) for value in linea.split()]
                datos_aceleracion.extend(values)

        

       
        aceleracion = np.array(datos_aceleracion)
        

    
        npts = len(aceleracion)
        dt = 0.001 

   
        tiempo = np.arange(0, npts*dt, dt)
        return aceleracion,tiempo

    
    
    else:
        print(f"El archivo '{nombre_archivo}' no existe en la carpeta '{carpeta_archivos}'.")


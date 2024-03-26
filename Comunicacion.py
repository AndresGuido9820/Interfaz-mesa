import serial, serial.tools.list_ports 
from threading import Thread, Event
from tkinter import StringVar
class comunicacion():
    def __init__(self,*args):
        super().__init__(*args)
        self.datos_recibidos= StringVar()
        self.arduino=serial.Serial()
        self.arduino.timeout=0.5
        self.puertos=[]
        self.baudrates=['1200','2400','4800', '9600','19200','38400','115200']
        self.señal=Event()
        self.hilo=None
        
    def puertos_disponibles(self):
        self.puertos=[port.device for port in serial.tools.list_ports.comports()]
       # prueba=[port.device for port in serial.tools.list_ports.comports()]
       # for i in prueba:
        #    print(i)
        #print(self.puertos)
        
    def conexion_serial(self):
        try:
            self.arduino.open()
        except:
            pass
        if(self.arduino.is_open):
            self.iniciar_hilo()
            print("conectado")
        
            
    def enviar_datos(self,data):
        if(self.arduino.is_open):
            self.dato=str(data)+"/n"
            self.arduino.write(self.datos.encode())
        else:
            print("error")
    
    def leer_datos(self):
        try:
            while(self.señal.isSet() and self.arduino.is_open):
                data=self.arduino.readline().decode("utf-8").strip()
                if (len(data)>1):
                    set.datos_recibidos.set(data)
        except TypeError:
            pass
    
    def iniciar_hilo(self):
        self.hilo= Thread(target=self.leer_datos)
        self.hilo.setDaemon(1)
        self.señal.set()
        self.hilo.start()
    def stop_hilo(self):
        if(self.hilo is not None ):
            self.señal.clear()
            self.hilo.join()
            self.hilo=None
        
    def desconectar(self):
        self.arduino.close()
        self.stop_hilo()
        
        
        
            
            
        
            
        
        
        
        

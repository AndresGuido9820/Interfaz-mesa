from tkinter import Tk, Frame, Button, Button,Label,ttk, PhotoImage,Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib. animation as animation 
from Comunicacion import comunicacion
import collections
class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)
        
        self.datos_arduino=comunicacion()# objeto que servirá para usar metodods de comunicación con arduino 
        self.actualizar_puertos()
        print(self.datos_arduino.puertos)
        self.muestra=100
        self.datos=0.0
        
        self.fig,ax= plt.subplots(facecolor="#FF69B4", dpi=100, figsize=(4,2))
        plt.title("grafica desplazamiento vs tiempo ", color="white", size=12, family='Arial')
        ax.tick_params(direction='out',length=5, width=2, color="white", grid_color='r', grid_alpha=0.5 )
        self.line=ax.plot([],[], color='m', marker= 'o', linewidth=12, markersize=1, markeredgecolor='m')
        self.line2= ax.plot([],[], color='g', marker= 'o', linewidth=2, markersize=1, markeredgecolor='g')
        plt.xlim(0, self.muestra)
        plt.ylim(0, 10)
        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color("red")
        ax.spines['left'].set_color('red')
        ax.spines['right'].set_color('red')
        ax.spines['top'].set_color('red')
        self.datos_señal1=collections.deque([0]*self.muestra, maxlen=self.muestra)
        self.datos_señal2=collections.deque([0]*self.muestra, maxlen=self.muestra)
        self.widgets()
    
    def animate(self, i):
        self.datos=(self.datos_arduino.datos_recibidos.get())
        dato=self.datos.split(",")
        dato1=float(dato[0])
        datos2=float(dato[1])
        self.datos_señal1.append(dato1)
        self.datos_señal2.append(datos2)
        self.line.set_data(range(self.muestra), self.datos_señal1)
        self.line.set_data(range(self.muestra), self.datos_señal2)
        
    def iniciar(self):
        self.ani=animation.FuncAnimation(self.fig, self.animate, interval=100, blit=False)
        self.bt_graficar.config(state='disable')
        self.bt_pausar.config(state='normal')
        self.canvas.draw()
    def pausar(self):
        self.ani.event_source.stop()
        self.bt_reanudar.config(state='normal')
    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state='disable')
    
    def widgets(self):
        frame= Frame(self.master, bg='lavender', bd=2)
        frame.grid(column=0, columnspan=2, row=0, sticky='nsew')
        frame1=Frame(self.master, bg='lavender')
        frame1.grid(column=2, row=0, sticky='nsew')
        frame4=Frame(self.master, bg='lavender')
        frame4.grid(column=0, row=1, sticky='nsew')
        frame2=Frame(self.master, bg='lavender')
        frame2.grid(column=1, row=1, sticky='nsew')
        frame3=Frame(self.master, bg='lavender')
        frame3.grid(column=2, row=1, sticky='nsew')
        
        
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=1)
        self.master.columnconfigure(2,weight=1)
        
        self.master.rowconfigure(0,weight=5)
        self.master.rowconfigure(1,weight=1)
        
        
        
        self.canvas=FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(padx=0,pady=0,expand=True, fill='both')
        
        self.bt_graficar=Button(frame4, text='graficar', font=( 'arial', 12, 'bold'), width=12, bg='pink', fg='black', command=self.iniciar)
        self.bt_graficar.pack(pady=5, expand=1)
        self.bt_pausar=Button(frame4, state='disabled', text='pausar', font=( 'arial', 12, 'bold'), width=12, bg='pink', fg='black', command=self.pausar)
        self.bt_pausar.pack(pady=5,expand=1)
        
        self.bt_reanudar=Button(frame4,state='disabled', text=' reanudar',font=('arial', 12,'bold'),width=12,bg='pink',fg='light blue', command=self.reanudar )
        self.bt_reanudar.pack(pady=5, expand=1)
        
        
        
        self.logo=PhotoImage(file='logo.png').subsample(3,3)
        Label(frame2, text='Amplitud:', font=('arial', 12,'bold'), bg='lavender', fg='VioletRed1').pack(pady=5, expand=1)
        self.amplitud_entry = Entry(frame2, font=('arial', 12,))
        self.amplitud_entry.pack(pady=5, expand=1)

        Label(frame2, text='Velocidad:', font=('arial', 12,'bold'), bg='lavender', fg='VioletRed1').pack(pady=5, expand=1)
        self.velocidad_entry = Entry(frame2, font=('arial', 12))
        self.velocidad_entry.pack(pady=5, expand=1)

        self.bt_enviar_amplitud = Button(frame2, text='Enviar Amplitud', font=('arial', 12, 'bold'), width=15, bg='pink', fg='black', command=self.dato_amplitud)
        self.bt_enviar_amplitud.pack(pady=5, expand=1)

        self.bt_enviar_velocidad = Button(frame2, text='Enviar Velocidad', font=('arial', 12, 'bold'), width=15, bg='pink', fg='black', command=self.dato_velocidad)
        self.bt_enviar_velocidad.pack(pady=5, expand=1)
        
        
        
        port=self.datos_arduino.puertos
        baud= self.datos_arduino.baudrates
        
        Label(frame1, text='Puertos Entrada', bg='lavender', fg='VioletRed1', font=('Arial',12, 'bold')).pack(padx=5,expand=1)
        
        self.combobox_port=ttk.Combobox(frame1, values=port, justify='center', width=12, font='Arial' )
        self.combobox_port.pack(pady=0, expand=1)
        #self.combobox_port.current(0)
        Label(frame1,text='Braudates', bg='lavender', fg='VioletRed1', font=('Arial',12,'bold')).pack(pady=0,expand=1)
        
        
    
    

       
        self.combobox_baud=ttk.Combobox(frame1, values=baud, justify='center',width=12, font='Arial')
        self.combobox_baud.pack(padx=20, expand=1)
        self.combobox_baud.current(3)
        
        
        self.bt_conectar=Button(frame1, text='conectar', font=('Arial', 12, 'bold'), width=12, bg='pink', command=self.conectar_serial)
        
        self.bt_conectar.pack(pady=5,expand=1)
       
        self.bt_actualizar=Button(frame1, text='actualizar', font=('Arial',12,'bold'),width=12,bg='pink', command=self.actualizar_puertos)
       
        self.bt_actualizar.pack(pady=5,expand=1)
        
        self.bt_desconectar=Button(frame1, text='desconectar', font=('Arial',12, 'bold'), width=12,bg='pink', command=self.desconectar_serial )
        
        self.bt_desconectar.pack(pady=5,expand=1)
        Label(frame3, image=self.logo, bg='black').pack(pady=5,expand=1)
        
        
        
    def actualizar_puertos(self):
        #print("hola")
        self.datos_arduino.puertos_disponibles()
    
    def conectar_serial(self):
        self.bt_conectar.config(state='disable')
        self.bt_desconectar.config(state='normal')
        
        self.bt_graficar.config(state='normal')
        self.bt_reanudar.config(state='disabled')
        
        self.datos_arduino.arduino.port=self.combobox_port.get()
        self.datos_arduino.arduino.baudrate=self.combobox_baud.get()
        self.datos_arduino.conexion_serial()
    
    
    def desconectar_serial(self):
        self.bt_conectar.config(state='normal')
        self.bt_desconectar.config(state='disabled')
        self.slider_uno.config(state='disabled')
        self.slider_dos.config(state='disabled')
        self.bt_pausar.config(state='disabled')
        
        
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_arduino.desconectar()
        
    def dato_amplitud(self):
        amplitud = '1' + self.amplitud_entry.get()
        self.datos_arduino.enviar_datos(amplitud)
    
    def dato_velocidad(self):
        velocidad = '2' + self.velocidad_entry.get()
        self.datos_arduino.enviar_datos(velocidad)


if __name__=="__main__":
    ventana=Tk()
    ventana.geometry('742x535')
    ventana.config(bg='gray30', bd=4)
    ventana.wm_title("grafica animacion")
    ventana.minsize(width=700,height=400)
    ventana.call('wm','iconphoto',ventana._w, PhotoImage(file='logo.png'))
    app=Grafica(ventana)
    app.mainloop()
    
    
        
        
        
        
        
         
        
        
        
        
        
        
    

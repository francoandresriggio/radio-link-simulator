from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from manipulacion_archivo import *
from calculos import *

def buscarArchivo():

	archivo=filedialog.askopenfilename(title="Abrir archivo de coordenadas")
	directorio.set(archivo)


def activarSimulacion():
	k=factorK.get()
	n=nFresnel.get()
	porc=porc_n_Fresnel.get()
	lambdaSimu=lambdaSimulacion.get()
	ganan=ganacia.get()
	eirp=eirpAntena.get()

	latitud, longitud, altura = extraer_info(directorio.get())

	#Obtengo la distancia entre 2 puntos (sin considerar las alturas). Esto aplica tanto entre extremos de enlace como puntos intermedios:
	dist=calculo_distancia(latitud, longitud)


	#Calculo la pendiente entre los 2 puntos en donde van a estar las antenas:
	pendiente=pendiente_extremos(altura, dist[-1])

	#Calculo la distancia entre los extremos del radioenlace y los puntos intermedios, considerando la pendiente calculada recientemente:
	dist_radio= distancia_radioenlaces(pendiente, dist)

	#Calculo la altura aparente de los obstaculos, el radio superior de fresnel (usando la distancia y la pendiente entre las antenas)
	#y la recta que une a las antenas:
	radio_sup, recta, altura_apar = recta_alturaRecta_radioFres(n, lambdaSimu, k, pendiente, dist_radio, altura, dist)

	#Giro el radio de Fresnel y calculo los radios superior e inferior de Fresnel:
	radio_inf, radio_sup = giro_calculoRadios(dist_radio, pendiente, radio_sup, recta, len(altura))

	#Calculo la altura de las antenas. Para eso, subo la antena hasta que este más arriba que la altura aparente del obstaculo:
	recta, radio_sup, radio_inf = alturaAntenas(recta, radio_sup, radio_inf, len(altura), porc, altura_apar) 

	#Calculo de Potencias:
	potRx = calculo_potencia(eirp, ganan, dist[-1], lambdaSimu) 
	
	#Grafico el resultado final:
	ax.clear()
	ax.plot(dist,recta, color='green',label="Enlace")
	ax.plot(dist,radio_sup,'--', color='red', label="Radio de Fresnel")
	ax.plot(dist,radio_inf, '--' , color='red')
	ax.plot(dist,altura, color='black',label="Altura del terreno")
	ax.plot(dist,altura_apar,'--', color='orange' ,label="Altura aparente del terreno")
	ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',ncol=2, mode="expand", borderaxespad=0.)
	ax.grid(True)
	ax.set_xlabel('$Distancia(metros)$')
	ax.set_ylabel('$Altura(metros)$')
	line.draw()
	altAntLabel.config(text="La altura de las antenas sera de "+str(int(float(recta[0])-float(altura[0])))+" metros")
	potRxLabel.config(text="La potencia recibida sera de "+str(round(potRx,3))+" dBm")


#---------------------------------------DEFINO RAIZ-----------------------------------------#

raiz = Tk()
raiz.resizable(0,0)
raiz.geometry("610x800")
raiz.title("Simulacion de Enlace")

#----------------------------------DECLARO VARIABLES DE GUI---------------------------------#

directorio=StringVar()
nFresnel=IntVar()
porc_n_Fresnel=DoubleVar()
lambdaSimulacion=DoubleVar()
factorK=DoubleVar()
ganacia=DoubleVar()
eirpAntena=DoubleVar()

#-----------------------DELCARO FRAME ----------------#

frameSimulacion=Frame(raiz, width=400, height=300)
frameSimulacion.pack(side="top", fill="x")

#---------------------GUI DE ARCHIVO------------------#

tituloSeleccion=Label(frameSimulacion, text="SIMULACIÓN")
tituloSeleccion.grid(row=0, column=0, padx=5, pady=5, columnspan=5)
tituloSeleccion.config(font=("MS PMincho", 15), justify="center")

rutaArchivo=Label(frameSimulacion, text="Ruta: ").grid(row=1, column=0, sticky="e", padx=5, pady=10)
cuadroRuta=Entry(frameSimulacion, width=50, textvariable=directorio).grid(row=1, column=1, padx=5, pady=5, columnspan=3)
botonRuta=Button(frameSimulacion,text="Seleccionar", width=10, command=buscarArchivo).grid(row=1, column=4, padx=5, pady=5, columnspan=4)

#--------------------GUI DE PARAMETROS-----------------#

radioFresnel=Label(frameSimulacion, text="Radio de Fresnel (n):").grid(row=2, column=0, sticky="e", pady=5)
cuadroRadioFresnel=Entry(frameSimulacion, textvariable=nFresnel).grid(row=2, column=1, pady=5)

lambdaLabel=Label(frameSimulacion, text="Lambda(mm):").grid(row=2, column=3, sticky="e", pady=5)
cuadroLambda=Entry(frameSimulacion, textvariable=lambdaSimulacion).grid(row=2, column=4, pady=5)

porc_n_radio=Label(frameSimulacion, text="Pocentaje del radio(%):").grid(row=3, column=0, sticky="e", pady=5)
cuadro_porc_n_radio=Entry(frameSimulacion, textvariable=porc_n_Fresnel).grid(row=3, column=1, pady=5)

factorKLabel=Label(frameSimulacion, text="Factor de corrección K:").grid(row=3, column=3, sticky="e", pady=5)
cuadroFactorK=Entry(frameSimulacion, textvariable=factorK).grid(row=3, column=4, pady=5)

gananciaAntena=Label(frameSimulacion, text="Ganancia de la antena (dBi):").grid(row=4, column=0, sticky="e", pady=5)
cuadroGananciaAntena=Entry(frameSimulacion, textvariable=ganacia).grid(row=4, column=1, pady=5)

EIRPLabel=Label(frameSimulacion, text="EIRP (dBm):").grid(row=4, column=3, sticky="e", pady=5)
cuadroEIRP=Entry(frameSimulacion, textvariable=eirpAntena).grid(row=4, column=4, pady=5)

botonCalcular=Button(frameSimulacion, text="Calcular Simulacion", width=30, command=activarSimulacion).grid(row=5, column=0, padx=5, pady=5, columnspan=5)

#----------------------AGREGO GRAFICO A LA GUI----------------------------#

figure=plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
ax.grid(True)
ax.set_xlabel('$Distancia(m)$')
ax.set_ylabel('$Altura(m)$')
line = FigureCanvasTkAgg(figure, frameSimulacion)
line.get_tk_widget().grid(row=6, column=0, padx=5, columnspan=5)


#----------------------AGREGO DATOS DEL GRAFICO A LA GUI----------------------------#

altAntLabel=Label(frameSimulacion, text="La altura de las antenas sera de 0 metros")
altAntLabel.config(font="Verdana 8 bold")
altAntLabel.grid(row=7, column=0, columnspan=2)

potRxLabel=Label(frameSimulacion, text="La potencia recibida sera de 0 dBm")
potRxLabel.config(font="Verdana 8 bold")
potRxLabel.grid(row=7, column=3, columnspan=2)

raiz.mainloop()
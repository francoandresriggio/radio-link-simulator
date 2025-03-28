import math

RADIO_TIERRA = 6372.795477598

def calculo_distancia(latitud, longitud):

	dist=[]
	rad=math.pi/180 #Convierte grados en radianes

	for i in range(len(latitud)):
		dlat=latitud[i]-latitud[0]
		dlon=longitud[i]-longitud[0]
		a=(math.sin(rad*dlat/2))**2 + math.cos(rad*latitud[0])*math.cos(rad*latitud[i])*(math.sin(rad*dlon/2))**2
		dist.append(2*RADIO_TIERRA*math.asin(math.sqrt(a))*1000) #el 1000 convierte de Km a m

	return dist

def pendiente_extremos(altura, distExtremos):

	dif_alt=altura[-1]-altura[0]
	return dif_alt/distExtremos

def distancia_radioenlaces(pendiente, dist):

	dist_radio = []
	angulo=math.atan(pendiente)

	for i in range(len(dist)):
		dist_radio.append(dist[i]/math.cos(angulo))

	return dist_radio

def recta_alturaRecta_radioFres(n, lambdaSimu, k, pendiente, dist_radio, altura, dist):
	radio_sup = []
	recta = []
	altura_apar = []

	lambdaSimu=lambdaSimu*0.001

	for i in range(len(dist)):
		radio_sup.append(math.sqrt((n*lambdaSimu*dist_radio[i]*(dist_radio[-1]-dist_radio[i]))/(dist_radio[i]+(dist_radio[-1]-dist_radio[i]))))
		recta.append(pendiente*dist[i]+altura[0])
		altura_apar.append( ((dist[i]*(dist[-1]-dist[i]) * lambdaSimu * n)/(2*k*RADIO_TIERRA*1000)) + altura[i] )

	return radio_sup, recta, altura_apar

def giro_calculoRadios(dist_radio, pendiente, radio_sup, recta, muestras):
	angulo=math.atan(-pendiente)

	radio_inf= []

	for i in range(muestras):
		radio_inf.append((-dist_radio[i]*math.sin(angulo))+(-radio_sup[i]*math.cos(angulo))+recta[0])
		radio_sup[i]=((-dist_radio[i]*math.sin(angulo))+(radio_sup[i]*math.cos(angulo))+recta[0])

	return radio_inf, radio_sup

def alturaAntenas(recta, radio_sup, radio_inf, muestras, porc, altura_apar):
	i = 0
	while i<muestras:
		if altura_apar[i]>radio_inf[i]+((recta[i]-radio_inf[i])*(1-porc/100)):
			for j in range(muestras):
				recta[j]+=1
				radio_sup[j]+=1
				radio_inf[j]+=1
			i=0
		i=i+1

	return recta, radio_sup, radio_inf

def calculo_potencia(eirp, ganan, dist, lambdaSimu):
	ael=20*math.log10(float(4*math.pi*dist)/(lambdaSimu*0.001))
	return eirp+ganan-ael
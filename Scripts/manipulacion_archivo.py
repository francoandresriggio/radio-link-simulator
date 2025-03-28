from io import open

def extraer_info(ruta):

	archivo=open(ruta,"r")
	archivo.seek(len(archivo.readline()))
	lista=archivo.readlines()
	archivo.close()

	latitud=[]
	longitud=[]
	altura=[]

	for linea in lista:
		valor=linea.split("\t")
		latitud.append(float(valor[1]))
		longitud.append(float(valor[2]))
		altura.append(float(valor[3]))

	return latitud, longitud, altura
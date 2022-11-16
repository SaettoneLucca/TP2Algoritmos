from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim

import speech_recognition as sr
r = sr.Recognizer()

import csv

ARCHIVO_MULTAS = "csvtest.txt"
ARCHIVO_DIRECCIONES = "csv2.txt"

def menu()->None:
    operaciones:tuple = ("Denuncias cerca de estadios", "Denuncias en cuadrante", "Localizar autos robados", "Ubicacion infraccion por patente", "Grafico mensual de denuncias", "Salir")

    for i in range(len(opciones)):
        print(f"{i + 1} - {operaciones[i]}")

#Manipulacion de archivos
def leer_archivo(nombre_archivo:str)->list:
    """Pre: Recibe una ruta de archivo y una lista de datos vacia
    Post: Rellena la lista vacia con los datos del archivo"""
    datos_archivo:list = []
    try:    
        with open(nombre_archivo, "r",newline="",encoding="UTF-8") as archivo:
            csv_reader = csv.reader(archivo, delimiter=",")
            for linea in csv_reader:
                datos_archivo.append(linea)
    except IOError:
        print("Hubo un problema operando con el archivo")
    
    return datos_archivo

def escribir_archivo(datos_archivo:list,nombre_archivo:str)->None:
    """Pre: Recibe una ruta de un archivo y una lista con datos
    Post: Reescribe el archivo con los datos de la lista"""
    try:
        with open(nombre_archivo, "w", newline="",encoding="UTF-8") as archivo:
            csv_writer = csv.writer(archivo, delimiter=",")
            for line in datos_archivo:
                csv_writer.writerow(line)
    except IOError:
        print("Hubo un problema operando con el archivo")


#Geopy
def geolocalizador(coordenada):
    """Pre: Recibe una coordenada
    Post:convierte latitud y longitud a una dirreccion"""
    geolocator = Nominatim(user_agent="multas")
    ubicacion_coordenada = geolocator.reverse(coordenada)
    x = str(ubicacion_coordenada).split(",")
    y = x[0:4]

    return y

def ubicacion(datos_csv)->list:
    lista_datos:list = []

    for dato in datos_csv:
        aux:list = []
        coordenada = dato[2:4]
        u = (geolocalizador(coordenada))#ubicacion
        direccion_aux:list = u[0:2]
        direccion:str = ("".join(direccion_aux))
        localidad:str = u[2]
        provincia:str = u[3]
        aux.extend(dato)
        aux.pop(2)
        aux.insert(3,direccion)
        aux.insert(4,localidad)
        aux.insert(5,provincia)
        aux.pop(2)
        lista_datos.append(aux)

    return lista_datos

def geolocalizador_I(ubicacion):
    """Pre: Recibe una ubicacion de una multa
    Post:Convierte una direccion a coordenadas"""
    geolocator = Nominatim(user_agent="multas")
    coordenadas=geolocator.geocode(ubicacion)
    x = (coordenadas.latitude, coordenadas.longitude)
    return x

def distancia(datos_archivo:list)->None:
    """Pre: Recibe una lista con datos de multas
    Post: Lista las denuncias relaizadas en un radio de 1km al rededor del estadio de boca y river"""
    denuncias_boca:list =[]
    denuncias_river:list = []
    estadio_boca =(-34.63606363146764, -58.36482460201631)
    estadio_river =(-34.54479432316617, -58.458104102018275)
    for dato in datos_archivo:
        ubicacion:list = []
        aux:list = dato[2].split(' ')
        ubicacion.append(aux[0])
        ubicacion.append(aux[1])
        ubicacion.append(dato[3])
        ubicacion.append(dato[4])
        punto = geolocalizador_I(ubicacion)
        if GD(estadio_boca,punto).km <= 1:
            denuncias_boca.append(dato)

        elif GD(estadio_river,punto).km <= 1:
            denuncias_river.append(dato)
    
    print("Denuncias cerca de los estadios de boca y river: \n")
    print("Denuncias a 1km del estadio de Boca:")
    if len(denuncias_boca) == 0:
        print("No hay denuncias cerca de la cancha de Boca\n")
    else:    
        for multa in denuncias_boca:
                print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente: {multa[5]}, {multa[6]}, {multa[7]}\n")

    print("Denuncias a 1km del estadio de River:")
    if len(denuncias_river) == 0:
        print("No hay denuncias cerca de la cancha de River\n")
    else:    
        for multa in denuncias_river:
                print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente: {multa[5]}, {multa[6]}, {multa[7]}\n")


#Speech recognition
def transcribir_audio(ruta_audio:str)->str:
    """Pre: Recibe una ruta de un audio
    Post: Printea en pantalla la trasncripcion del audio"""
    texto:str = "-"
    open_audio=sr.AudioFile(ruta_audio)
    try:
        with open_audio as source:
            audio = r.record(source)
        s = r.recognize_google(audio, language="es-AR")
        texto = s
    except IOError:
        print("Hubo un problema al operar con el archivo de audio")
    except Exception as e:
        print("Exception: "+str(e))
    
    return texto

def audio_a_texto(datos_multas)->None:
    print("Convirtiendo audios a textos . . .\n")
    for multa in datos_multas:
        ruta_audio:str = multa[6]
        transcripcion:str = transcribir_audio(ruta_audio)
        multa[6] = transcripcion


#accion == 2
def cuadrante(datos_multas:list,datos_direcciones:list)->None:
    """Pre: Recibe una lista cargada con multas
    Post: Imprime por pantalla las multas en el cuadrante dado por las avenidas"""
    
    #El cuadrante formado por las avenidas forma una especie de cuadrado,
    #entonces puedo tomar los datos de las long y latitudes max y min.
    longitud_max:float = -58.3711
    longitud_min:float = -58.39203
    latitud_max:float = -34.59841
    latitud_min:float = -34.60916
    lista_multas_cuadrante:list = []

    for i in range(len(datos_multas)):   
        coordenada:list = []
        coordenada.append(float(datos_multas[i][2]))
        coordenada.append(float(datos_multas[i][3]))

        if ((coordenada[0]>latitud_min) and (coordenada[0]<latitud_max)) and ((coordenada[1]>longitud_min) and (coordenada[1]<longitud_max)):
            lista_multas_cuadrante.append(datos_direcciones[i])

    if len(lista_multas_cuadrante) == 0:
        print("No hay multas cargadas en el cuadrante\n")
    else:
        print("Multas en el cuadrante de las Avenidas:\n")
        for multa in lista_multas_cuadrante:
            print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente{multa[5]}, {multa[6]}, {multa[7]}\n")


def main()->None:
    #Comenzamos cargando la informacion de los archivos en listas, para su posterior manipulacion
    datos_multas:list = leer_archivo(ARCHIVO_MULTAS)
    audio_a_texto(datos_multas)

    datos_direcciones:list = ubicacion(datos_multas)
    escribir_archivo(datos_direcciones, ARCHIVO_DIRECCIONES)

    menu()
    accion:int = int(input(("Que desea realizar? ")))
    while (accion != 6):
        if accion == 1:
            distancia(datos_direcciones)
        elif accion == 2:
            cuadrante(datos_multas,datos_direcciones)
        elif accion == 3:
            pass
        elif accion == 4:
            pass
        elif accion == 5:
            pass

        menu()
        accion = int(input(("Que desea realizar? ")))

main()
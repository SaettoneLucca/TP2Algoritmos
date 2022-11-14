from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim

import speech_recognition as sr
r = sr.Recognizer()

import csv

ARCHIVO_MULTAS = "csvtest.txt"
ARCHIVO_DIRECCIONES = "csv2.txt"
ARCHIVO_ESTADIOS = "denuncias_estadios.txt"

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
        aux = []
        coordenada = dato[2:4]
        u = (geolocalizador(coordenada))#ubicacion
        aux.extend(dato)
        aux.pop(2)
        aux.insert(3,u)
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

def distancia(datos_archivo:list)->list:
    """Pre: Recibe una lista con datos de multas
    Post: Lista las denuncias relaizadas en un radio de 1km al rededor del estadio de boca y river"""
    denuncias:list =[]
    estadio_boca =(-34.63606363146764, -58.36482460201631)
    estadio_river =(-34.54479432316617, -58.458104102018275)
    for ubicacion in datos_archivo:
        punto = geolocalizador_I(ubicacion[2])
        if GD(estadio_boca,punto).km <= 1:
            denuncias.append(ubicacion)

        elif GD(estadio_river,punto).km <= 1:
            denuncias.append(ubicacion)

    return denuncias


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
    print("Conviritnedo audios a textos . . .")
    for multa in datos_multas:
        ruta_audio:str = multa[6]
        transcripcion:str = transcribir_audio(ruta_audio)
        multa[6] = transcripcion


def main()->None:
    #Comenzamos cargando la informacion de los archivos en listas, para su posterior manipulacion
    datos_multas:list = leer_archivo(ARCHIVO_MULTAS)
    audio_a_texto(datos_multas)

    datos_direcciones:list = ubicacion(datos_multas)
    escribir_archivo(datos_direcciones, ARCHIVO_DIRECCIONES)

    datos_denuncias_estadios:list = distancia(datos_direcciones)
    escribir_archivo(datos_denuncias_estadios, ARCHIVO_ESTADIOS)

main()
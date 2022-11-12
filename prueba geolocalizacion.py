#geolocalizador
import csv
from geopy.geocoders import Nominatim

ARCHIVO_MULTAS = "C:/Algo1/TP2/TP2Algoritmos-main/csvtest.txt"
ARCHIVO_2 = "C:/Algo1/TP2/TP2Algoritmos-main/csv2.txt"

def leer_archivo(archivo_multas:str,datos_csv:list)->None:
    """Pre: Recibe una ruta de archivo y una lista de datos vacia
    Post: Rellena la lista vacia con los datos del archivo"""
    try:    
        with open(archivo_multas, "r",newline="",encoding="UTF-8") as archivo:
            csv_reader = csv.reader(archivo, delimiter=",")
            for linea in csv_reader:
                datos_csv.append(linea)
    except IOError:
        print("Hubo un problema operando con el archivo")

def geolocalizador(coordenada):
    """Pre: Recibe una coordenada
    Post:convierte latitud y longitud a una dirreccion"""
    geolocator = Nominatim(user_agent="multas")
    ubicacion_coordenada = geolocator.reverse(coordenada)
    x = str(ubicacion_coordenada).split(",")
    y = x[0:4]

    return y

def ubicacion(datos_csv,lista_nueva)->list:
    for dato in datos_csv:
        aux = []
        coordenada = dato[2:4]
        u = (geolocalizador(coordenada))#ubicacion
        aux.extend(dato)
        aux.pop(2)
        aux.insert(3,u)
        aux.pop(2)
        lista_nueva.append(aux)
    print(lista_nueva)
    return lista_nueva

def write_archivo(lista_nueva:list,archivo_2:str)->None:
    """Pre: Recibe una ruta de un archivo y una lista con datos
    Post: Reescribe el archivo con los datos de la lista"""
    try:
        with open(archivo_2, "w", newline="",encoding="UTF-8") as archivo:
            csv_writer = csv.writer(archivo, delimiter=",")
            for line in lista_nueva:
                csv_writer.writerow(line)
    except IOError:
        print("Hubo un problema operando con el archivo")

def main()->None:
    lista_nueva:list = []
    datos_csv:list = []

    leer_archivo(ARCHIVO_MULTAS,datos_csv)
    ubicacion(datos_csv,lista_nueva)
    write_archivo(lista_nueva,ARCHIVO_2)
main()

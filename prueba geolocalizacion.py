#geolocalizador
import csv
from geopy.geocoders import Nominatim


def leer_archivo(archivo_multas,datos_csv:list):
    with open("csvtest.txt", "r") as archivo:
        csv_reader = csv.reader(archivo, delimiter=",")
        for linea in csv_reader:
            datos_csv.append(linea)

def coordenadas(datos_csv:list):
    #crea una lista con la latitud y longitud
    lat_lon:list = []
    for datos in datos_csv:
        if datos[1] not in lat_lon:
            aux:list = []
            aux.append(datos[2])
            aux.append(datos[3])
        lat_lon.append(aux)
    
    return lat_lon

def geolocalizador(datos_csv:list):
    #convierte latitud y longitud a una dirreccion
    direccion:list = []
    lista:list = coordenadas(datos_csv)
    geolocator = Nominatim(user_agent="multas")
    for i in lista:
        ubicacion=geolocator.reverse(i)
        direccion.append(ubicacion)
    print(direccion)

    
def write_archivo(datos_csv):
    pass
    lista = geolocalizador(datos_csv)


def main():
    datos_csv:list =[]
    archivo_multas = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csvtest.txt")
    leer_archivo(archivo_multas,datos_csv)
    coordenadas(datos_csv)
    geolocalizador(datos_csv)
main()
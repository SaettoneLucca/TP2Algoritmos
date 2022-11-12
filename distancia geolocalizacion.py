from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim
import csv

ARCHIVO_2 = "C:/Algo1/TP2/TP2Algoritmos-main/csv2.txt"
DENUNCIAS_ESTADIOS = "C:/Algo1/TP2/TP2Algoritmos-main/denuncias_estadios.txt"

def leer_archivo(archivo_2,datos_csv):
    """Pre: Recibe una ruta de un archivo y una lista vacia de datos
    Post: Rellena la lista con los datos del archivo"""
    try:
        with open(archivo_2, "r",newline="",encoding="UTF-8") as archivo:
            csv_reader = csv.reader(archivo, delimiter=",")
            for linea in csv_reader:
                datos_csv.append(linea)
    except IOError:
        print("Hubo un problema al operar con el archivo")

def distancia(datos_csv):
    """Pre: Recibe una lista con datos de multas
    Post: Lista las denuncias relaizadas en un radio de 1km al rededor del estadio de boca y river"""
    denuncias:list =[]
    estadio_boca =(-34.63606363146764, -58.36482460201631)
    estadio_river =(-34.54479432316617, -58.458104102018275)
    for ubicacion in datos_csv:
        punto = geolocalizador_I(ubicacion[2])
        if GD(estadio_boca,punto).km <= 1:
            print("Esta denucnia fue realizada a menos de 1km del estadio boca: ", GD(estadio_boca,punto).km)
            denuncias.append(ubicacion)

        elif GD(estadio_river,punto).km <= 1:
            print("Esta denuncia fue realizada a menos de 1km del estadio river: ", GD(estadio_river,punto).km)
            denuncias.append(ubicacion)

        else:
            print("esta denuncia no es relevante")

    return denuncias    

def geolocalizador_I(ubicacion):
    """Pre: Recibe una ubicacion de una multa
    Post:Convierte una direccion a coordenadas"""
    geolocator = Nominatim(user_agent="multas")
    coordenadas=geolocator.geocode(ubicacion)
    x = (coordenadas.latitude, coordenadas.longitude)
    return x

def write_archivo(denunicas_estadios,datos_csv):
    """Pre: Recibe una ruta de un archivo y una lista de datos
    Post: Reescribe el archivo con los datos de la lista"""
    lista:list = distancia(datos_csv)
    try:    
        with open(denunicas_estadios, "w", newline="",encoding="UTF-8") as archivo:
            csv_writer = csv.writer(archivo, delimiter=",", quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
            for line in lista:
                csv_writer.writerow(line)
    except IOError:
        print("Hubo un problema al operar con el archivo")

def main():
    datos_csv:list = []
    
    leer_archivo(ARCHIVO_2,datos_csv)
    distancia(datos_csv)
    write_archivo(DENUNCIAS_ESTADIOS,datos_csv)
main()

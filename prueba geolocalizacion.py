#geolocalizador
import csv
from geopy.geocoders import Nominatim


def leer_archivo(archivo_multas,datos_csv:list):
    with open("csvtest.txt", "r") as archivo:
        csv_reader = csv.reader(archivo, delimiter=",")
        for linea in csv_reader:
            datos_csv.append(linea)


def geolocalizador(coordenada):
    #convierte latitud y longitud a una dirreccion
    geolocator = Nominatim(user_agent="multas")
    ubicacion=geolocator.reverse(coordenada)
    x = str(ubicacion).split(",")
    y = x[0:4]

    return y

def ubicacion(datos_csv,lista_nueva):
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

def write_archivo(lista_nueva,archivo_2):
    with open("csv2.txt", "w", newline="") as archivo:
        csv_writer = csv.writer(archivo, delimiter=",", quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        for line in lista_nueva:
            csv_writer.writerow(line)


def main():
    lista_nueva:list = []
    datos_csv:list =[]
    archivo_multas = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csvtest.txt")
    archivo_2 = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csv2.txt")
    leer_archivo(archivo_multas,datos_csv)
    ubicacion(datos_csv,lista_nueva)
    write_archivo(lista_nueva,archivo_2)
main()
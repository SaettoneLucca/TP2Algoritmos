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
    return ubicacion

def a(datos_csv):
    lista_nueva:list = []
    for dato in datos_csv:
        aux = []
        coordenada = dato[2:4]
        u = (geolocalizador(coordenada)[0])
        aux.append(u)
        aux.extend(dato)
        lista_nueva.append(aux)
    print(lista_nueva)

def main():
    datos_csv:list =[]
    archivo_multas = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csvtest.txt")
    archivo_2 = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csv2.txt")
    leer_archivo(archivo_multas,datos_csv)
    a(datos_csv)
main()
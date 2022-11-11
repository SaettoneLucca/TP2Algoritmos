#geolocalizador
import csv


def leer_archivo(archivo_multas,datos_csv:list):
    with open("csvtest.txt", "r") as archivo:
        csv_reader = csv.reader(archivo, delimiter=",")
        for linea in csv_reader:
            datos_csv.append(linea)

def coordenadas(datos_csv:list):
    lat_lon:list = []
    for datos in datos_csv:
        if datos[1] not in lat_lon:
            aux:list = []
            aux.append(datos[2])
            aux.append(datos[3])
        lat_lon.append(aux)
    
    print(lat_lon)

def main():
    datos_csv:list =[]
    archivo_multas = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csvtest.txt")
    leer_archivo(archivo_multas,datos_csv)
    coordenadas(datos_csv)

main()
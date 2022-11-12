from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim
import csv

def leer_archivo(archivo_2,datos_csv):
    with open("csv2.txt", "r") as archivo:
        csv_reader = csv.reader(archivo, delimiter=",")
        for linea in csv_reader:
            datos_csv.append(linea)



def distancia(datos_csv):
    #lista las denuncias relaizadas en un radio de 1km al rededor del estadio de boca y river
    denuncias:list =[]
    Estadio_boca =(-34.63606363146764, -58.36482460201631)
    Estadio_river =(-34.54479432316617, -58.458104102018275)
    for ubicacion in datos_csv:
        punto = geolocalizador_I(ubicacion[2])
        if GD(Estadio_boca,punto).km <= 1:
            print(f"esta denucnia fue realizada a menos de 1km del estadio boca: ", GD(Estadio_boca,punto).km)
            denuncias.append(ubicacion)

        elif GD(Estadio_river,punto).km <= 1:
            print("esta denuncia fue realizada a menos de 1km del estadio river: ", GD(Estadio_river,punto).km)
            denuncias.append(ubicacion)

        else:
            print("esta denuncia no es reelevante")

    return denuncias    


def geolocalizador_I(ubicacion):
    #convierte una direccion a coordenadas
    geolocator = Nominatim(user_agent="multas")
    coordenadas=geolocator.geocode(ubicacion)
    x = (coordenadas.latitude, coordenadas.longitude)
    return x

def write_archivo(denunicas_estadios,datos_csv):
    lista:list = distancia(datos_csv)
    with open("denuncias_estadios.txt", "w", newline="") as archivo:
        csv_writer = csv.writer(archivo, delimiter=",", quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        for line in lista:
            csv_writer.writerow(line)



def main():
    datos_csv:list = []
    archivo_2 = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\csv2.txt")
    denunicas_estadios = open("C:\\Users\\lucca\\OneDrive\\Escritorio\\fiuba\\algoritmos 1\\TP2\\denuncias_estadios.txt")
    leer_archivo(archivo_2,datos_csv)
    distancia(datos_csv)
    write_archivo(denunicas_estadios,datos_csv)
main()
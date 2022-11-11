#geolocalizador

from geopy.geocoders import Nominatim 

def geolocalizador():
    #convierte latitud y longitud a una dirreccion
    geolocator = Nominatim(user_agent="multas")
    ubicacion=geolocator.geocode("Facultad de Ingeniería, Avenida Paseo Colón, Buenos Aires")
    print(ubicacion.address)
    print((ubicacion.latitude, ubicacion.longitude))

def main():
    


main
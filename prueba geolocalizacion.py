from geopy.geocoders import Nominatim 

geolocator = Nominatim()

location = geolocator.geocode("Calle del Universo, 3, Valladolid") 
print(location.address) 
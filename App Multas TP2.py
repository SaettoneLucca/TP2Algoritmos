#import de librerias
from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim
from gmplot import gmplot
import webbrowser
import cv2
import numpy as np 
import argparse
import time
import imutils
import keras_ocr
import matplotlib.pyplot as plt
import csv
import speech_recognition as sr
r = sr.Recognizer()
from termcolor import colored

#INICIO DEL CODIGO
FILE_FINE = "csvtest.txt"
FILE_DIRECTIONS = "csv2.txt"
FILE_STOLEN = "robados.txt"

def validate_numeric_valor(validate_value: str) -> int:
    """ Pre: Comprueba que el número ingresado por el usuario sea un valor númerico
        Post: Una vez que el usuario ingresa un número, lo transforma a numero entero y lo devuelve."""
    while not validate_value.isnumeric():
        validate_value = input("Error no ingresó un numero. Ingrese un número correspondiente : ")
    return int(validate_value)

def validate_option_range(validate_value: int, start_value: int, final_value: int) -> int:
    """ Pre: Comprueba que el número ingresado por el usuario se encuentro entre un cierto rango
        Post: Una vez que el usuario ingresa un número en este rango, lo transforma a numero entero y lo devuelve."""
    while ( validate_value < start_value or validate_value > final_value):
        validate_value = int(validate_numeric_valor(input(f"Error. No eligió ninguna de las opciones. Eliga una de las opciones de {start_value} a {final_value}: ")))
    return validate_value

def menu() -> None:
    operation: tuple = ("Denuncias cerca de estadios", "Denuncias en el cuadrante", "Localizar autos robados", 
                         "Ubicacion infraccion por patente", "Grafico mensual de denuncias", "Salir")
    for i in range(len(operation)):
        print(f"{i + 1} - {operation[i]}")

#Manipulacion de archivos
def read_file(name_file: str) -> list:
    """ Pre: Recibe una ruta de archivo y una lista de datos vacia.
        Post: Rellena la lista vacia con los datos del archivo."""
    data_file: list = []
    try:    
        with open(name_file, "r", newline = "", encoding = "UTF-8") as file:
            csv_reader = csv.reader(file, delimiter = ",")
            for line in csv_reader:
                data_file.append(line)
    except IOError:
        print("Hubo un problema operando con el archivos")
    return data_file

def write_file(data_file: list, name_file: str) -> None:
    """ Pre: Recibe una ruta de un archivo y una lista con datos.
        Post: Reescribe el archivo con los datos de la lista."""
    try:
        with open(name_file, "w", newline = "", encoding = "UTF-8") as file:
            csv_writer = csv.writer(file, delimiter = ",")
            for line in data_file:
                csv_writer.writerow(line)
    except IOError:
        print("Hubo un problema operando con el archivo")


#Geopy
def geolocalizator(coordinate):
    """ Pre: Recibe una coordenada.
        Post: Convierte latitud y longitud a una direccion."""
    geolocator = Nominatim(user_agent = "multas")
    coordinate_location = geolocator.reverse(coordinate)
    x = str(coordinate_location).split(",")
    y = x[0:4]
    return y

def location(info_cvs)->list:
    data_list: list = []
    for data in info_cvs:
        aux: list = []
        coordinate = data[2:4]
        u = (geolocalizator(coordinate)) #ubicacion
        location_aux: list = u[0:2]
        location: str = ("".join(location_aux))
        locality: str = u[2]
        province: str = u[3]
        aux.extend(data)
        aux.pop(2)
        aux.insert(3, location)
        aux.insert(4, locality)
        aux.insert(5, province)
        aux.pop(2)
        data_list.append(aux)
    return data_list

def geolocalizator_I(location):
    """ Pre: Recibe una ubicacion de una multa.
        Post: Convierte una ubicacion a coordenadas."""
    geolocator = Nominatim(user_agent = "multas")
    coordinates = geolocator.geocode(location)
    x = (coordinates.latitude, coordinates.longitude)
    return x

#action == 1
def distance(data_file: list) -> None:
    """ Pre: Recibe una lista con datos de multas.
        Post: Lista las denuncias realizadas en un radio de 1 km alrededor del estadio de Boca y River."""
    fines_Boca: list = []
    fines_River: list = []
    Boca_stadium = (-34.63606363146764, -58.36482460201631)
    River_stadium = (-34.54479432316617, -58.458104102018275)
    for data in data_file:
        location: list = []
        location.append(data[2])
        location.append(data[3])
        location.append(data[4])
        dot = geolocalizator_I(location)
        if GD(Boca_stadium, dot).km <= 1:
            fines_Boca.append(data)
        elif GD(River_stadium, dot).km <= 1:
            fines_River.append(data)

    print("Denuncias cerca de los estadios de Boca y River:\n")
    print("Denuncias a 1 km del Estadio de Boca:")
    if len(fines_Boca) == 0:
        print("No hay denuncias cerca del Estadio de Boca\n")
    else:    
        for fines in fines_Boca:
                print(f"Timestamp: {fines[0]}, Teléfono: {fines[1]}, Dirección de la infracción: {fines[2]}, Localidad: {fines[3]}, Provincia: {fines[4]}, Patente: {fines[5]}, {fines[6]}, {fines[7]}\n")
    print("Denuncias a 1 km del Estadio de River:")
    if len(fines_River) == 0:
        print("No hay denuncias cerca del Estadio de River\n")
    else:    
        for fines in fines_River:
                print(f"Timestamp: {fines[0]}, Teléfono: {fines[1]}, Dirección de la infracción: {fines[2]}, Localidad: {fines[3]}, Provincia: {fines[4]}, Patente: {fines[5]}, {fines[6]}, {fines[7]}\n")

#action == 2
def quadrant(data_fines: list, data_directions: list) -> None:
    """Pre: Recibe una lista cargada con multas.
    Post: Imprime por pantalla las multas en el cuadrante dado por las avenidas."""
    #El cuadrante formado por las avenidas forma una especie de cuadrado,
    #entonces puedo tomar los datos de las longitud y latitudes max y min.
    length_max: float = -58.3711
    length_min: float = -58.39203
    latitude_max: float = -34.59841
    latitude_min: float = -34.60916
    list_fines_quadrant: list = []
    for i in range(len(data_fines)):   
        coordinate: list = []
        coordinate.append(float(data_fines[i][2]))
        coordinate.append(float(data_fines[i][3]))
        if ((coordinate[0] > latitude_min) and (coordinate[0] < latitude_max)) and ((coordinate[1] > length_min)
             and (coordinate[1] < length_max)):
            list_fines_quadrant.append(data_directions[i])
    if len(list_fines_quadrant) == 0:
        print("No hay multas cargadas en el cuadrante\n")
    else:
        print("Multas en el cuadrante de las Avenidas:\n")
        for fines in list_fines_quadrant:
            print(f"Timestamp: {fines[0]}, Teléfono: {fines[1]}, Dirección de la infracción: {fines[2]}, Localidad: {fines[3]}, Provincia: {fines[4]}, Patente: {fines[5]}, {fines[6]}, {fines[7]}\n")

def map(coordinates):
    """ Pre: Recibe una coordenada.
        Post: Devuelve un mapa web con el marcador."""
    coordinates_aux = list(coordinates)
    #Inicializamos el mapa con una coordenada xy cualesquiera
    gmap = gmplot.GoogleMapPlotter(-34.611377315283946, -58.3741883957914,13)
    #Agregamos la coordinate
    gmap.marker(coordinates_aux[0], coordinates_aux[1], 'cornflowerblue')
    #Pasamos el mapa a un archivo html
    gmap.draw("my_map.html")
    #Abrimos el mapa en google
    webbrowser.open("my_map.html")

def patent_photo(photo_route):
    """ Pre: Recibe una ruta de imagen. 
        Post: La imprime por pantalla."""
    cv2.imshow("Image", photo_route)
    cv2.waitKey(0)

#action == 4
def patent_map(data_directions, data_fines):
    """ Pre: Recibe una lista con datos de multas.
        Post: Devuelve la foto asociada a esa patente y un mapa de google indicando donde fue realizada la denuncia."""
    patent_x = input("Ingrese la patente a localizar: ")
    for data in data_directions:
            if patent_x == data[5]:
                location: list = []
                location.append(data[2])
                location.append(data[3])
                location.append(data[4])
                coordinates = geolocalizator_I(location)
                map = map(coordinates)
                for i in data_fines:
                    aux: tuple = (i[2],i[3])
                    if GD(coordinates, aux).km <= 0.01:
                        photo_route = cv2.imread(i[4])
                        foto = patent_photo(photo_route)


#action == 3
def list_of_stolen(data_directions):
    """ Pre: Recibe una lista de infracciones
        Post: Devuelve una alerta con tiempo y ubicación si una patente de los robados coincide con uno en infración"""
    message: str = "ALERTA! AUTOS CON INFRACCIONES QUE COINCIDEN CON AUTOS EN PEDIDO DE CAPTURA"
    match: list = []
    stolen: list = read_file(FILE_STOLEN)
    for stole in stolen:
        for patent in stole:
            for data in data_directions:
                if patent == data[5]:
                    aux: list = []
                    aux.append(data[0])
                    aux.append(data[2])
                    aux.append(data[3])
                    aux.append(data[4])
                    aux.append(data[5])
                    match.append(aux)
    if match != None:
        print(colored(message, 'red'))
        for i in range(len(match)):
                print(colored(match[i], 'blue'))


#Speech recognition
def transcrip_audio(audio_route: str) -> str:
    """ Pre: Recibe una ruta de un audio.
        Post: Printea en pantalla la trasncripcion del audio."""
    text: str = "-"
    open_audio = sr.AudioFile(audio_route)
    try:
        with open_audio as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
        text = r.recognize_google(audio, language = "es-AR")
    except IOError:
        print("Hubo un problema al operar con el archivo de audio.")
    except Exception as e:
        print("Excepsión: " + str(e))
    return text

def audio_to_text(data_fines) -> None:
    print("Convirtiendo audios a textos . . .\n")
    for fines in data_fines:
        audio_route: str = fines[6]
        transcripcion: str = transcrip_audio(audio_route)
        fines[6] = transcripcion


## YOLO Obj Detection
def load_yolo():
    #Importamos los weight de yolo , los cfg y los coc.names
	net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	classes = []
	with open("coco.names", "r") as f:
		classes = [line.strip() for line in f.readlines()] 
	output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
	colors = np.random.uniform(0, 255, size = (len(classes), 3))
	return net, classes, colors, output_layers
	
def load_image(img_route):
	""" Pre: Toma la ruta de una imagen.
        Post: Devuelve la imagen reconocida y le aplica un resize(cambio de tamaño)."""
	img = cv2.imread(img_route)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor = 0.00392, size = (320, 320), mean = (0, 0, 0), swapRB = True, crop = False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids

def draw_labels(boxes, confs, colors, class_ids, classes, img): 
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			color = colors[i]
			cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
			cv2.putText(img, label, (x, y - 5), font, 1, color, 1)	
	return label
   
def image_detect(img_route):
    """Post: Devuelve el objeto encontrado en la foto."""
    model, classes, colors, output_layers = load_yolo()
    image, height, width, channels = load_image(img_route)
    blob, outputs = detect_objects(image, model, output_layers)
    boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
    draw_labels(boxes, confs, colors, class_ids, classes, image)
    obj = draw_labels(boxes, confs, colors, class_ids, classes, image)
    return obj

def obj_detection(data_fines, data_directions):
    """ Pre: Recibe una lista de infracciones.
        Post: Llama a la funcion patent_to_text si se detecta un auto en la foto."""
    for fines in data_directions:
        img_route: str = fines[5]
        imagen = cv2.imread(img_route)
        obj: str = image_detect(img_route)
        print("Opening " + img_route + " .... ")
        if obj == "car":
            print("Se ha detectado un auto en la foto. Extrayendo patente...")
            fines[5] = patent_to_text(imagen, data_fines)
        else:
            print("No se ha detectado un auto en la foto.")


## Keras&Opencv extraccion de patent
def patent_to_text(imagen, data_fines): 
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #Convertimos la imagen a blanco y negro
    tresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1] #Pasamos la foto a blanco y negros puros(imagen binaria)
    #Buscamos contornos de la imagen(formas)
    contours = cv2.findContours(tresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]                              
    #Aspect ratio de las patentes argentinas 400/130 = 3.07692307692
    license_ratio = 3.07692307692
    min_w = 80
    max_w = 110
    min_h = 25
    max_h = 52
    #Iteramos sobre los contronos y nos quedamos con los que tengan una relacion de aspecto parecida
    candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if (np.isclose(aspect_ratio, license_ratio, atol = 0.7) and
            (max_w > w > min_w) and (max_h > h > min_h)):
            candidates.append(cnt)
    """Para estar seguro de que nos quedamos con la patente, nos quedamos con la forma que 
    este más abajo de la imagen, hay que las patentes se encuentran en la parte inferior del auto"""
    ys = []
    for cnt in candidates:
        x, y, w, h = cv2.boundingRect(cnt)
        ys.append(y)
    license = candidates[np.argmax(ys)]
    #Croppeamos la patente del resto
    x, y, w, h = cv2.boundingRect(license)
    Cropped = imagen[y : y + h, x : x + w]
    #Volvemos a pasarlo a blanco y negro
    gray_cropped = cv2.cvtColor(Cropped, cv2.COLOR_BGR2GRAY)
    tresh_cropped = cv2.adaptiveThreshold(gray_cropped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)
    #Guardamos la patente
    plate = cv2.imwrite("patent.jpeg", Cropped)
    #Extraemos el text de la patentw
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(img) for img in ["patent.jpeg"]]
    prediction_groups = pipeline.recognize(images)
    patent = []
    predicted_image = prediction_groups[0]
    for text, box in predicted_image:
        patent.append(text)
    joined = "".join(patent)
    print(joined)

    return joined

def main() -> None:
    #Comenzamos cargando la informacion de los archivos en listas, para su posterior manipulacion
    data_fines : list = read_file(FILE_FINE)
    audio_to_text(data_fines)
    data_directions: list = location(data_fines)
    obj_detection(data_fines, data_directions)
    write_file(data_directions, FILE_DIRECTIONS)
    #print(data_fines)
    #print(data_directions)

    menu()
    action: int = int(validate_numeric_valor(input("¿Qué desea realizar?")))
    action = int(validate_option_range(action, 1, 6))
    while (action != 6):
        if action == 1:
            distance(data_directions)
        elif action == 2:
            quadrant(data_fines, data_directions)
        elif action == 3:
            list_of_stolen(data_directions)
        elif action == 4:
            patent_map(data_directions, data_fines)
        elif action == 5:
            pass
        menu()
        action: int = int(validate_numeric_valor(input("¿Qué desea realizar?")))
        action = int(validate_option_range(action, 1, 6))
main()
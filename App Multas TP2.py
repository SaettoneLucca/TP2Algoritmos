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
ARCHIVO_MULTAS = "csvtest.txt"
ARCHIVO_DIRECCIONES = "csv2.txt"
ARCHIVO_ROBADOS = "robados.txt"

def menu() -> None:
    operation: tuple = ("Denuncias cerca de estadios", "Denuncias en cuadrante", "Localizar autos robados", 
                         "Ubicacion infraccion por patente", "Grafico mensual de denuncias", "Salir")
    for i in range(len(operation)):
        print(f"{i + 1} - {operation[i]}")

#Manipulacion de archivos
def leer_archivo(nombre_archivo: str) -> list:
    """Pre: Recibe una ruta de archivo y una lista de datos vacia
    Post: Rellena la lista vacia con los datos del archivo"""
    datos_archivo: list = []
    try:    
        with open(nombre_archivo, "r", newline = "", encoding = "UTF-8") as archivo:
            csv_reader = csv.reader(archivo, delimiter = ",")
            for linea in csv_reader:
                datos_archivo.append(linea)
    except IOError:
        print("Hubo un problema operando con el archivo")
    return datos_archivo

def escribir_archivo(datos_archivo: list, nombre_archivo: str) -> None:
    """Pre: Recibe una ruta de un archivo y una lista con datos
    Post: Reescribe el archivo con los datos de la lista"""
    try:
        with open(nombre_archivo, "w", newline = "", encoding = "UTF-8") as archivo:
            csv_writer = csv.writer(archivo, delimiter = ",")
            for line in datos_archivo:
                csv_writer.writerow(line)
    except IOError:
        print("Hubo un problema operando con el archivo")



#Geopy
def geolocalizador(coordenada):
    """Pre: Recibe una coordenada
    Post:convierte latitud y longitud a una dirreccion"""
    geolocator = Nominatim(user_agent = "multas")
    ubicacion_coordenada = geolocator.reverse(coordenada)
    x = str(ubicacion_coordenada).split(",")
    y = x[0:4]
    return y

def ubicacion(datos_csv)->list:
    lista_datos: list = []
    for dato in datos_csv:
        aux: list = []
        coordenada = dato[2:4]
        u = (geolocalizador(coordenada)) #ubicacion
        direccion_aux: list = u[0:2]
        direccion: str = ("".join(direccion_aux))
        localidad: str = u[2]
        provincia: str = u[3]
        aux.extend(dato)
        aux.pop(2)
        aux.insert(3, direccion)
        aux.insert(4, localidad)
        aux.insert(5, provincia)
        aux.pop(2)
        lista_datos.append(aux)
    return lista_datos

def geolocalizador_I(ubicacion):
    """Pre: Recibe una ubicacion de una multa
    Post:Convierte una direccion a coordenadas"""
    geolocator = Nominatim(user_agent = "multas")
    coordenadas = geolocator.geocode(ubicacion)
    x = (coordenadas.latitude, coordenadas.longitude)
    return x

#accion == 1
def distancia(datos_archivo: list) -> None:
    """Pre: Recibe una lista con datos de multas
    Post: Lista las denuncias relaizadas en un radio de 1km al rededor del estadio de boca y river"""
    denuncias_boca: list = []
    denuncias_river: list = []
    estadio_boca = (-34.63606363146764, -58.36482460201631)
    estadio_river = (-34.54479432316617, -58.458104102018275)
    for dato in datos_archivo:
        ubicacion: list = []
        ubicacion.append(dato[2])
        ubicacion.append(dato[3])
        ubicacion.append(dato[4])
        punto = geolocalizador_I(ubicacion)
        if GD(estadio_boca,punto).km <= 1:
            denuncias_boca.append(dato)
        elif GD(estadio_river,punto).km <= 1:
            denuncias_river.append(dato)
    
    print("Denuncias cerca de los estadios de boca y river: \n")
    print("Denuncias a 1km del estadio de Boca:")
    if len(denuncias_boca) == 0:
        print("No hay denuncias cerca de la cancha de Boca\n")
    else:    
        for multa in denuncias_boca:
                print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente: {multa[5]}, {multa[6]}, {multa[7]}\n")

    print("Denuncias a 1km del estadio de River:")
    if len(denuncias_river) == 0:
        print("No hay denuncias cerca de la cancha de River\n")
    else:    
        for multa in denuncias_river:
                print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente: {multa[5]}, {multa[6]}, {multa[7]}\n")

#accion == 2
def cuadrante(datos_multas: list, datos_direcciones: list) -> None:
    """Pre: Recibe una lista cargada con multas
    Post: Imprime por pantalla las multas en el cuadrante dado por las avenidas"""
    
    #El cuadrante formado por las avenidas forma una especie de cuadrado,
    #entonces puedo tomar los datos de las long y latitudes max y min.
    longitud_max: float = -58.3711
    longitud_min: float = -58.39203
    latitud_max: float = -34.59841
    latitud_min: float = -34.60916
    lista_multas_cuadrante: list = []

    for i in range(len(datos_multas)):   
        coordenada: list = []
        coordenada.append(float(datos_multas[i][2]))
        coordenada.append(float(datos_multas[i][3]))

        if ((coordenada[0]>latitud_min) and (coordenada[0]<latitud_max)) and ((coordenada[1]>longitud_min)
             and (coordenada[1]<longitud_max)):
            lista_multas_cuadrante.append(datos_direcciones[i])

    if len(lista_multas_cuadrante) == 0:
        print("No hay multas cargadas en el cuadrante\n")
    else:
        print("Multas en el cuadrante de las Avenidas:\n")
        for multa in lista_multas_cuadrante:
            print(f"Timestamp: {multa[0]},Teléfono: {multa[1]}, Dirección de la infracción: {multa[2]}, Localidad: {multa[3]}, Provincia: {multa[4]}, patente{multa[5]}, {multa[6]}, {multa[7]}\n")

def mapa(coordenadas):
    """Pre: recibe una coordenada
    Post: devuelve un mapa web con el marcador
    """
    coordenadas = list(coordenadas)
    #inicializamos el mapa con una cordeenada xy cualesquiera
    gmap = gmplot.GoogleMapPlotter(-34.611377315283946, -58.3741883957914,13)

    #Agregamos la coordenada
    gmap.marker(coordenadas[0],coordenadas[1], 'cornflowerblue')

    # Pasamos el mapa a un archivo html
    gmap.draw("my_map.html")

    #abrimos el mapa en google
    webbrowser.open("my_map.html")

def foto_patente(ruta_foto):
    #pre: recibe una ruta de imagen
    #la imprime por pantalla
    cv2.imshow("Image", ruta_foto)
    cv2.waitKey(0)

#accion == 4
def patente_mapa(datos_direcciones, datos_multas):
    """Pre: Recibe una lista con datos de multa
    Post: Devuelve la foto asociada a esa patente y un mapa de google indicando donde fue relaizada la denuncia
    """
    patente_x = input("ingrese la patente a localizar: ")
    for dato in datos_direcciones:
            if patente_x == dato[5]:
                ubicacion: list = []
                ubicacion.append(dato[2])
                ubicacion.append(dato[3])
                ubicacion.append(dato[4])
                coordenadas = geolocalizador_I(ubicacion)
                map = mapa(coordenadas)
                for i in datos_multas:
                    aux: tuple = (i[2],i[3])
                    if GD(coordenadas,aux).km <= 0.01:
                        ruta_foto = cv2.imread(i[4])
                        foto = foto_patente(ruta_foto)


#accion == 3
def list_of_stolen(datos_direcciones):
    """pre: recibe una lista de infracciones
        post: devuelve una alerta,timestamp y ubiccacion si una patente de los robados coincide con uno en infracion"""

    message: str = "ALERTA! AUTOS CON INFRACCIONES QUE COINCIDEN CON AUTOS EN PEDIDO DE CAPTURA"
    match: list = []
    robados: list = leer_archivo(ARCHIVO_ROBADOS)
    for robado in robados:
        for patente in robado:
            for dato in datos_direcciones:
                if patente == dato[5]:
                    aux: list = []
                    aux.append(dato[0])
                    aux.append(dato[2])
                    aux.append(dato[3])
                    aux.append(dato[4])
                    aux.append(dato[5])
                    match.append(aux)
    if match != None:
        print(colored(message, 'red'))
        for i in range(len(match)):
                print(colored(match[i], 'blue'))


#Speech recognition
def transcribir_audio(ruta_audio: str) -> str:
    """Pre: Recibe una ruta de un audio
    Post: Printea en pantalla la trasncripcion del audio"""
    texto: str = "-"
    open_audio = sr.AudioFile(ruta_audio)
    try:
        with open_audio as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
        s = r.recognize_google(audio, language="es-AR")
        texto = s
    except IOError:
        print("Hubo un problema al operar con el archivo de audio")
    except Exception as e:
        print("Exception: "+str(e))
    return texto

def audio_a_texto(datos_multas)->None:
    print("Convirtiendo audios a textos . . .\n")
    for multa in datos_multas:
        ruta_audio: str = multa[6]
        transcripcion: str = transcribir_audio(ruta_audio)
        multa[6] = transcripcion


## YOLO Obj Detection
def load_yolo():
    #importamos los weight de yolo , los cfg y los coc.names
	net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	classes = []
	with open("coco.names", "r") as f:
		classes = [line.strip() for line in f.readlines()] 
	
	output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
	colors = np.random.uniform(0, 255, size = (len(classes), 3))
	return net, classes, colors, output_layers
	
def load_image(ruta_imagen):
	#pre: toma la ruta de una imagen
    #post: devuelve la imagen reconocida y le aplica un resize
	img = cv2.imread(ruta_imagen)
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
   
def image_detect(ruta_imagen):
    #POST:devuelve el objeto encontrado en la foto 
	model, classes, colors, output_layers = load_yolo()
	image, height, width, channels = load_image(ruta_imagen)
	blob, outputs = detect_objects(image, model, output_layers)
	boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
	draw_labels(boxes, confs, colors, class_ids, classes, image)
	objeto = draw_labels(boxes, confs, colors, class_ids, classes, image)
	return objeto

def obj_detection(datos_multas, datos_direcciones):
    #pre:recibe una lista de infracciones
    #Post: llama a la funcion patente_a_str si se detecta un auto en la foto
    for multa in datos_direcciones:
        ruta_imagen: str = multa[5]
        imagen = cv2.imread(ruta_imagen)
        objeto: str = image_detect(ruta_imagen)
        print("Opening " + ruta_imagen + " .... ")
        if objeto == "car":
            print("Se ha detectado un auto en la foto. Extrayendo patente...")
            multa[5] = patente_a_str(imagen, datos_multas)
        else:
            print("No se ha detectado un auto en la foto")


## Keras&Opencv extraccionde patente
def patente_a_str(imagen,datos_multas): 
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #convertimos la imagen a blanco y negro
    tresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1] #pasamos la foto a blanco y negros puros(imagen binaria)
    #buscamos contornos de la imagen(formas)
    contours = cv2.findContours(tresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]                              
    #aspect ratio de las patentes argentinas 400/130 = 3.07692307692
    license_ratio = 3.07692307692
    min_w = 80
    max_w = 110
    min_h = 25
    max_h = 52
    #iteramos sobre los contronos y nos quedamos con los que tengan una relacion de aspecto parecida
    candidates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if (np.isclose(aspect_ratio, license_ratio, atol=0.7) and
            (max_w > w > min_w) and (max_h > h > min_h)):
            candidates.append(cnt)
    #para estar seguro de que nos quedamos con la patente, nos quedamos con la forma que este mas abajo de la imagen, ay que las patentes
    #se encuentran en la parte inferior del auto
    ys = []
    for cnt in candidates:
        x, y, w, h = cv2.boundingRect(cnt)
        ys.append(y)
    license = candidates[np.argmax(ys)]
    #croppeamos la patente del resto
    x, y, w, h = cv2.boundingRect(license)
    Cropped = imagen[y : y + h, x : x + w]
    #volvemos a pasarlo a blanco y negro
    gray_cropped = cv2.cvtColor(Cropped, cv2.COLOR_BGR2GRAY)
    tresh_cropped = cv2.adaptiveThreshold(gray_cropped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)
    #guardamos la patnete
    plate = cv2.imwrite("patente.jpeg", Cropped)
    #extraemos el texto de la patente
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(img) for img in ["patente.jpeg"]]
    prediction_groups = pipeline.recognize(images)
    patente = []
    predicted_image = prediction_groups[0]
    for text, box in predicted_image:
        patente.append(text)
    joined = "".join(patente)
    print(joined)

    return joined

def main() -> None:
    #Comenzamos cargando la informacion de los archivos en listas, para su posterior manipulacion
    datos_multas : list = leer_archivo(ARCHIVO_MULTAS)
    audio_a_texto(datos_multas)
    datos_direcciones:list = ubicacion(datos_multas)
    obj_detection(datos_multas,datos_direcciones)
    escribir_archivo(datos_direcciones, ARCHIVO_DIRECCIONES)
    #print(datos_multas)
    #print(datos_direcciones)

    menu()
    accion: int = int(input(("Que desea realizar? ")))
    while (accion != 6):
        if accion == 1:
            distancia(datos_direcciones)
        elif accion == 2:
            cuadrante(datos_multas,datos_direcciones)
        elif accion == 3:
            list_of_stolen(datos_direcciones)
        elif accion == 4:
            patente_mapa(datos_direcciones,datos_multas)
        elif accion == 5:
            pass

        menu()
        accion = int(input(("Que desea realizar? ")))

main()
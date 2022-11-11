
import speech_recognition as sr
 
 
 
 
def main():
    sound = "audiodemo.wav"
    r = sr.Recognizer()
 
    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print("Convirtiendo Audio a Texto ..... ")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Audio Convertido : \n" + r.recognize_google(audio, language="es-AR"))
 
    except Exception as e:
        print("Error {} : ".format(e) )
 
 

main()
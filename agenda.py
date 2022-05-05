import speech_recognition as sr
import pyttsx3
import datefinder as df
import difflib as dif
from googletrans import Translator


recog = sr.Recognizer()

translator = Translator()

def SpeakText(text):
    out = pyttsx3.init()
    out.say(text)
    print(text)
    out.runAndWait()

def ContainsStr(text, compare):
    resposta = dif.get_close_matches(text, [compare])
    return len(resposta) > 0 

def Listening():
    try:
        with sr.Microphone() as mic:
            recog.adjust_for_ambient_noise(mic, 1)          
            print("Ouvindo...")
            audio = recog.listen(mic)
            return recog.recognize_google(audio, language='pt-BR')
    except sr.RequestError as e:
        print("Não foi possível requisitar o pedido: {0}".format(e))
        Listening()
    except: 
        Listening()

def confirma():
    while(True):
        resposta = Listening()
        print(resposta)
        if resposta == "sim":
            SpeakText("Ok!")
            return True
        elif resposta == "não":
            SpeakText("Ok!")
            return False
        else:
            SpeakText("Não entendi! Diga Sim para confirmar ou não para tentar novamente")

def findDate(text):
    translateEn = translator.translate(text, dest= 'en', src ='pt')
    matches = df.find_dates(translateEn.text)
    for match in matches:
        return match.strftime("%d/%m/%Y")

def ReadDate():
    while(True):
        try:
            SpeakText("Diga a data do evento:") 
            dataText = Listening()
            print(dataText)
            dataFormat = findDate(dataText)
            SpeakText("Você disse: " + dataFormat + "?")
            if confirma():
                return dataFormat 
        except:
            SpeakText("Não foi possível identificar a data")

def ReadDescription():
    while(True):
        try:
            SpeakText("Diga a descrição do evento:") 
            descText = Listening()
            return descText
        except:
            SpeakText("Não entendi")


def CriarEvento(date):
    if date is None:
        SpeakText("Ok, vamos criar um novo evento")
        date = ReadDate()
    else:
        SpeakText("Deseja  criar um evento  na data " + date + "?")
        if not confirma():
            date = ReadDate()
    desc = ReadDescription()
    SpeakText("Confirma a criação do evento " + desc + " na data " + date + "?")
    if confirma():
        SpeakText("Ok! evento salvo")
        f = open("dados.txt", "a")
        f.write(date + ";" + desc + "\n")
        f.close()

def ReadEvents(date):
    if date is None:
        SpeakText("Ok, vamos criar um novo evento")
        date = ReadDate()
    with open('dados.txt') as f:
        lista = []
        for line in f.readlines():
            dateLine = line.split(";")[0]
            if dateLine == date:
                lista.append(line.split(";")[1])
        SpeakText("Os eventos da data " + date + "são")
        for desc in lista:
            SpeakText(desc)

def Command(command):
    if ContainsStr("desligar", command):
       SpeakText("Ok! Estou desligando...")
    elif ContainsStr("Criar evento", command):
        date = findDate(command) 
        CriarEvento(date)
    elif ContainsStr("listar eventos", command):
        date = findDate(command) 
        ReadEvents(date)
    else:
        SpeakText("Não entendi (" + command +")")

text = ""
while(text != "desligar"):
    try:
        with sr.Microphone() as mic:
            recog.adjust_for_ambient_noise(mic)
            SpeakText("Diga o que deseja fazer:")
            audio = recog.listen(mic)
            text = recog.recognize_google(audio, language='pt-BR')
            Command(text)
    except sr.RequestError as e:
        print("Não foi possível requisitar o pedido: {0}".format(e))
    except sr.UnknownValueError:
        print("Um erro desconhecido ocorreu")






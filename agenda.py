import speech_recognition as sr
import pyttsx3
import datefinder as df
import re
from googletrans import Translator


recog = sr.Recognizer()
translator = Translator()

#trasnsforma o texto em audio e também imprime no console
def SpeakText(text):
    out = pyttsx3.init()
    out.say(text)
    print(text)
    out.runAndWait()

#Compara às duas string, se uma contém em outra, retorna True
def ContainsStr(text, compare):
    return re.search(text, compare)

#transforma o áudio em texto, fica ouvindo até o retorno ser diferente de nulo
def Listening():
    while(True):
        try:
            with sr.Microphone() as mic:
                recog.adjust_for_ambient_noise(mic, 1)          
                print("Ouvindo...")
                audio = recog.listen(mic)
                text = recog.recognize_google(audio, language='pt-BR')
                if text:
                    return text 
        except sr.RequestError as e:
            print("Não foi possível requisitar o pedido: {0}".format(e))
        except:
            print("Erro") 

#Espera uma confirmação do usuário através de voz, se 'sim', retorna True, se 'não' retorna False 
def Confirm():
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
            SpeakText("Não entendi! Diga 'sim' para confirmar ou 'não' para tentar novamente")

#Procura uma data na string, se contém retorna a primeira encontrada. Formatada em dd/mm/yyyy
def FindDate(text):
    #traduzimos o texto para inglês, pois a lib datefinder somente suporta datas em inglês
    translateEn = translator.translate(text, dest= 'en', src ='pt')
    matches = df.find_dates(translateEn.text)
    for match in matches:
        return match.strftime("%d/%m/%Y")

#Espera uma data através de um comando de voz
def ReadDate():
    while(True):
        try:
            SpeakText("Diga a data do evento:") 
            dataText = Listening()
            print(dataText)
            dataFormat = FindDate(dataText)
            SpeakText("Você disse: " + dataFormat + "?")
            if Confirm():
                return dataFormat 
        except:
            SpeakText("Não foi possível identificar a data")

#Espera uma descrição
def ReadDescription():
    while(True):
        try:
            SpeakText("Diga a descrição:") 
            descText = Listening()
            return descText
        except:
            SpeakText("Não entendi")


#Cria um evento, salvando em um arquivo .txt
def CreateEvent(date):
    if date is None:
        SpeakText("Ok, vamos criar um novo evento")
        date = ReadDate()
    else:
        SpeakText("Deseja criar um evento na data " + date + "?")
        if not Confirm():
            date = ReadDate()
    desc = ReadDescription()
    SpeakText("Confirma a criação do evento " + desc + " na data " + date + "?")
    if Confirm():
        #salva o agendamento em um arquivo .txt com o seguinte formato dd/MM/yyyy;descrição;
        f = open("dados.txt", "a")
        f.write(date + ";" + desc + "\n")
        f.close()
        SpeakText("Evento salvo!")

#Lista os eventos através da voz, tanto por data quanto pela descrição
def ReadEvents():
    SpeakText("Diga a data ou descrição do evento:")
    text = Listening()
    date = FindDate(text)
    if date is None:
        #se não encontrou nenhuma data no texto, buscamos por descrição no arquivo
        with open('dados.txt') as f:
            lista = []
            for line in f.readlines():
                desc = line.split(";")[1]
                desc = desc.replace("\n", "")
                if ContainsStr(text, desc):
                    lista.append(line.split(";")[0] + ": " + line.split(";")[1])
            if len(lista) > 0:     
                SpeakText("Encontrei as seguintes datas para a descrição " + text + ":")
                for data in lista:
                    SpeakText(data)
            else:
                SpeakText("Não encontrei nenhum evento com a descrição " + text)
    else:
        #se encontrou alguma data no texto, buscamos por ela no aqruivo
        with open('dados.txt') as f:
            lista = []
            for line in f.readlines():
                dateLine = line.split(";")[0]
                if dateLine == date:
                   lista.append(line.split(";")[0] + ": " + line.split(";")[1])
            if len(lista) > 0:
                SpeakText("Encontrei os seguintes agendamentos para a data " + date + ":")
                for desc in lista:
                    SpeakText(desc)
            else:
                SpeakText("Não encontrei nenhum agendamentos na data " + date )

#Recebe os comandos a serem executados
def Command(command):
    command = command.lower()
    if ContainsStr(command,"desligar"):
       SpeakText("Ok! Estou desligando...")
    elif ContainsStr(command,"criar evento"):
        date = FindDate(command) 
        CreateEvent(date)
    elif ContainsStr(command,"listar evento"):
        ReadEvents()
    elif ContainsStr(command,"ajuda"):
         SpeakText("Você pode dizer os seguintes comandos:\n"
                   + " Criar Evento, para criar um evento em uma data específica;\n"
                   + " Listar Evento, para listar os eventos de uma data, ou listar as datas através de uma descrição;\n"
                   + " Desligar, para encerar o programa;")
    else:
        SpeakText("Não entendi (" + command +")")

#Início da execução, espera o comando do usuário através da voz 
SpeakText("Olá, Bem vindo")

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
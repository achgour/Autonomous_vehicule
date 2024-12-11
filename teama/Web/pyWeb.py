import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response
import datetime
GPIO.setmode(GPIO.BCM)
dataPin=[i for i in range(2,28)]
for dp in dataPin: GPIO.setup(dp,GPIO.IN) #,pull_up_down=GPIO.PUD_UP)
data=[]

#Partie surle temps
now=datetime.datetime.now()
timeString=now.strftime("%Y-%m-%d %H:%M")
templateData={
    'title':'Raspberry Pi 3B+ Web Controller',
    'time':timeString,
    'data':data,
}


def getData(): 
    ''' la fonction permet de return un liste data qui donne l'etat de chacun des pines

    GPIO.input permet de lire l'état actuel d'une broche
    dataPin est l'indice de chaque broche''' 
    data=[]
    for i,dp in enumerate(dataPin): data.append(GPIO.input(dataPin[i]))
    return data


app=Flask(__name__)


@app.route('/')  #Dès que quelq'un est sur le lien, la fct index se lance
def index():
    '''Cette fonction génère une page web dynamique, en affichant le titre, la date 
    et l'heure actuels, ainsi que des données provenant de broches GPIO sur un Raspberry Pi 
    en utilisant la fonction getData(). 
    La page web générée est basée sur le modèle HTML "htmlWeb.html".'''
    now=datetime.datetime.now()  #permet d'avoir la date et l'heure actuelles
    timeString=now.strftime("%Y-%m-%d %H:%M")  #permet de formater l'objet now pour obtenir la date et l'heure sous forme d'une chaîne de caractères "AAAA-MM-JJ HH:MM"
    data=getData()
    templateData={
        'title':'Raspberry Pi 3B+ Web Controller',
        'time':timeString,
        'data':data,
    }
    return render_template('htmlWeb.html',**templateData) #**templateData permet d'avoir les arguments du dictionnaire templateData
         
@app.route('/<actionid>') 
def handleRequest(actionid):
    print("Button pressed : {}".format(actionid)) #print Button pressed : actionid
    return "OK 200"   



if __name__=='__main__':   
    '''le code sous cette condition ne sera exécuté que si le script est 
    exécuté directement et non s'il est importé en tant que module dans un autre script.'''
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/

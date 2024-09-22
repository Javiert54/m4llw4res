import winreg
import os


# Iterar y mostrar los resultados
def getApps(file:str = 'files_exploits.csv'):

    # Obtener el objeto WMI
    uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    installed_apps = []

    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, subkey_name) as subkey:
                try:
                    app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    app_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    installed_apps.append((app_name, app_version))
                except FileNotFoundError:
                    continue

    return installed_apps

def getUsers():
    return set(os.listdir('C:\\Users'))

#print(getUsers())
#print([(app.Name, app.Version) for app in getApps()])
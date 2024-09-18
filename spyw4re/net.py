import requests
import socket
from scapy.all import ARP, Ether, srp, sr, IP, ICMP
import subprocess
import re
import paramiko
import os

def getPublicIP():
    try:
        # Hacer una solicitud a un servicio que devuelve la IP pública
        respuesta = requests.get('https://api64.ipify.org?format=json')
        datos = respuesta.json()
        ip_publica = datos['ip']
        return ip_publica
    except Exception as e:
        return str(e)

def getLocalIP():
    # Crear un socket temporal
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectar a una dirección IP arbitraria en Internet
        s.connect(("8.8.8.8", 80))
        # Obtener la dirección IP local
        ip_privada = s.getsockname()[0]
    except Exception as e:
        ip_privada = "No se pudo obtener la IP privada"
    finally:
        s.close()
    return ip_privada

def getInterfacesInfo():
    salida = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True).stdout
    net = {}
    mascara = ''
    puerta_enlace = ''
    intefaz = ''
    # Buscar y guardar todas las máscaras de subred y puertas de enlace predeterminadas
    for linea in salida.split('\n'):
        if 'Descripci¢n' in linea:
            intefaz = linea.split(':')[-1].strip()
            net[intefaz] = (puerta_enlace, mascara)
            mascara = ''
            puerta_enlace = ''
            
        elif 'scara de subred' in linea:
            mascara = linea.split(':')[-1].strip()
            net[intefaz] = (puerta_enlace, mascara)
        elif 'Puerta de enlace predeterminada' in linea:
            puerta_enlace = linea.split(':')[-1].strip()
            net[intefaz] = (puerta_enlace, mascara)
        
    return net


 #  --------------------
 #       SCANING
 #  --------------------
 
def hostDiscovery(ip_range):
    # Crear un paquete ARP
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    # Enviar el paquete y recibir las respuestas
    result = srp(packet, timeout=2.3, verbose=False)[0]
    # Crear una lista de hosts encontrados
    hosts = {}
    for sent, received in result:
        hosts[received.psrc] = received.hwsrc
    return hosts




system_ports = {
    20: 'FTP',
    21: 'FTP Control',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMPT',
    53: 'DNS',
    67: 'DHCP Server',
    68: 'DHCP Client',
    69: 'TFTP',
    80: 'HTTP',
    110: 'POP3',
    119: 'NNTP',
    139: 'NetBIOS',
    143: 'IMAP',
    389: 'LDAP',
    443: 'HTTPS',
    445: 'SMB',
    465: 'SMTP',
    569: 'MSN',
    587: 'SMTP',
    990: 'FTPS',
    993: 'IMAP',
    995: 'POP3',
    1080: 'SOCKS',
    1194: 'OpenVPN',
    3306: 'MySQL',
    3389: 'RDP',
    3689: 'DAAP',
    5432: 'PostGreSQL',
    5800: 'VNC',
    5900: 'VNC',
    6346: 'Grutella',
    8080: 'HTTP'
}

# portScannerTarget = socket.gethostbyname(input("Introduce la dirección IP o el nombre del host: "))
def portScanner(ip, delay=1, portRange=1024 ):
    print(f"Escaneando la ip: {ip}")

    for puerto in range(1, portRange):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(delay)
        resultado = s.connect_ex((ip, puerto))
        if resultado == 0:
            yield puerto, system_ports.get(puerto, "Servicio desconocido")
        s.close()

# h = portScanner("192.168.1.143", delay=0.08)
# for port, service in h:
#     print(f"puerto: {port} /  servicio: {service}")

#---------------------------
#-------   SSH   -----------
#---------------------------
def transfer_folder(local_folder, remote_folder, remote_host, remote_user, password):
    try:
        # Crear un cliente SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_host, username=remote_user, password=password)

        # Crear una sesión SFTP
        sftp = ssh.open_sftp()

        # Recorrer todos los archivos en la carpeta local
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_folder)
                remote_path = os.path.join(remote_folder, relative_path)

                # Crear directorios remotos si no existen
                remote_dir = os.path.dirname(remote_path)
                try:
                    sftp.stat(remote_dir)
                except FileNotFoundError:
                    sftp.mkdir(remote_dir)

                # Transferir el archivo
                sftp.put(local_path, remote_path)

        sftp.close()
        print("Carpeta transferida con éxito.")
    except Exception as e:
        print(f"Error al transferir la carpeta: {e}")
    finally:
        ssh.close()
from __future__ import print_function
import os,time,json,shlex,subprocess,argparse,random,sys, getopt
from termcolor import colored

def info():
		# print('\033[1m' + '' + '\033[0m')
	print(" " + '\033[1m' + colored("╔" + "═" * 75 + "╗" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("█" ,"blue") + " " * 75 + '\033[0m' + '\033[1m' +  colored("█" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("█" ,"blue") + '\033[1m' +  '{: ^84}'.format("Code made By: " + colored("DrakkoFire", "yellow")) + '\033[1m' + colored("█" ,"blue") )
	print(" " + '\033[1m' + colored("█" ,"blue") + '\033[1m' +  '{: ^84}'.format("GitHub: " + colored("https://github.com/DrakkoFire", "yellow")) + '\033[1m' + colored("█" ,"blue") )
	print(" " + '\033[1m' + colored("█" ,"blue") + '\033[1m' +  '{: ^84}'.format("Freelancer: " + colored("https://www.freelancer.com/u/DrakkoFire","yellow")) + '\033[1m' + colored("█" ,"blue") )
	print(" " + '\033[1m' + colored("█" ,"blue") + '\033[0m' + " " * 75 + '\033[1m' + colored("█" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("╚" + "═" * 75 + "╝","blue") + '\033[0m')

def clear():
	os.system("clear")

def getIP(interf):
	data = []
	sub = subprocess.Popen(['/bin/sh', '-c', "ip -j addr"], stdout=subprocess.PIPE)
	stdout = sub.stdout.read()
	json_data = json.loads(stdout)
	for i in range(0,len(json_data)):
		if json_data[i]['ifname'] == interf:
			data.append(json_data[i]['address'])
			x = json_data[i]["addr_info"]
	data.append(x[0]['prefixlen'])
	data.append(x[0]['local'])

	return data

def displayInt():
	nics = []
	sub = subprocess.Popen(['/bin/sh', '-c', "ip -j token"], stdout=subprocess.PIPE)
	stdout = sub.stdout.read()
	json_data = json.loads(stdout)
	print('{: ^80}'.format("Es aconsejable usar conexión por cable, la inalámbrica puede ser inestable"))
	print(" " + '\033[1m' + colored("╔" + "═" * 31 + "╗" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("║" ,"blue") + '\033[1m' +  '{: ^31}'.format("Tarjetas de red") + '\033[1m' + colored("║" ,"blue") )
	print(" " + '\033[1m' + colored("╠" + "═" * 5 + "╦" + "═" * 25 + "╣" ,"blue") + '\033[0m')
	# print(" " + '\033[1m' + colored("╔" + "═" * 5 + "╦" + "═" * 25 + "╗" ,"blue") + '\033[0m')
	for i in range(0,len(json_data)):
		x = json_data[i]["ifname"]
		nics.append(x)
		print(" " + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^5}'.format(i) + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^25}'.format(x) + '\033[1m' + colored("║" ,"blue") )
		if i + 1 == len(json_data):
			print(" " + '\033[1m' + colored("╚" + "═" * 5 + "╩" + "═" * 25 + "╝" ,"blue") + '\033[0m')
		else:
			print(" " + '\033[1m' + colored("╠" + "═" * 5 + "╬" + "═" * 25 + "╣" ,"blue") + '\033[0m')
		# print(" " + '\033[1m' + colored("║" ,"blue") + " " * 5 + x + " " * 10 + '\033[0m' + '\033[1m' +  colored("║" ,"blue") + '\033[0m')
	return nics


def getPieces(ip):
	a = ip.split(".")
	return a

def selInterface(data):
	a = True
	while a:
		try:
		    x = int(input(" Interfaz [0] ➮ "))
		    if x >= len(data):
		    	print('\033[1m' + colored("Error, la interfaz seleccionada no está en la lista", "red"))
		    else:
		    	print("Interfaz " + '\033[1m' + colored(data[x],"green") + '\033[0m' + " seleccionada")
		    	a = False
		    	return data[x]
		    break
		except ValueError:
			print("Interfaz "  + colored(data[0], "green") + " seleccionada")
			a = False
			return data[0]
		    # print(colored("[+]","green") + " Interfaz " + colored(b,"green"))

def printData(interf,ip,mac,netmask):
	print(" " + '\033[1m' + colored("╔" + "═" * 75 + "╗" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("║" ,"blue") + '\033[1m' +  '{: ^75}'.format("Configuración") + '\033[1m' + colored("║" ,"blue") )
	print(" " + '\033[1m' + colored("╠" + "═" * 10 + "╦" + "═" * 22 + "╦" + "═"*20 + "╦" + "═"*20 + "╣" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^10}'.format("Interfaz") + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^22}'.format("IP") + '\033[1m' + colored("║" ,"blue")+ '\033[1m' + '{: ^20}'.format("MAC") + '\033[1m' + colored("║" ,"blue")+ '\033[1m' + '{: ^20}'.format("Máscara") + '\033[1m' + colored("║" ,"blue") )
	print(" " + '\033[1m' + colored("╠" + "═" * 10 + "╬" + "═" * 22 + "╬" + "═"*20 + "╬" + "═"*20 + "╣" ,"blue") + '\033[0m')
	print(" " + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^10}'.format(interf) + '\033[1m' + colored("║" ,"blue") + '\033[1m' + '{: ^22}'.format(ip) + '\033[1m' + colored("║" ,"blue")+ '\033[1m' + '{: ^20}'.format(mac) + '\033[1m' + colored("║" ,"blue")+ '\033[1m' + '{: ^20}'.format(netmask) + '\033[1m' + colored("║" ,"blue") )
	print(" " + '\033[1m' + colored("╚" + "═" * 10 + "╩" + "═" * 22 + "╩" + "═"*20 + "╩" + "═"*20 + "╝" ,"blue") + '\033[0m')

def checkIp(ip):
	r = os.system("ping -c 2 %s > /dev/null 2>&1" % ip)
	if r == 0:
		return True
	else:
		return False

def getGw():
	sub = subprocess.Popen(['/bin/sh', '-c', "ip -j route"], stdout=subprocess.PIPE)
	stdout = sub.stdout.read()
	json_data = json.loads(stdout)
	return json_data[0]["gateway"]

SEPARATORS = {
    'colon': ':',
    'dash': '-',
    'none': '',
    'space': ' ',
}

# def parse_args():
#     parser = argparse.ArgumentParser(description='Generate random MAC address')
#     parser.add_argument('-s', '--separator',
#                         choices=sorted(SEPARATORS.keys()), default='colon',
#                         help='What separator to use between the bytes in the output.')
#     return parser.parse_args()

def macGenerator():
    # args = parse_args()
    separator = ":"

    mac = [ random.randint(0, 255) for x in range(0, 6) ]
    mac[0] = (mac[0] & 0xfc) | 0x02
    mac = separator.join([ '{0:02x}'.format(x) for x in mac ])
    return mac

def netmask(n):
	nm = ""
	resto = (32 - n) / 8
	n = n/8
	for i in range(0,int(n)):
		nm += "255."
	for j in range(0,int(resto)):
		nm += "0."
	nm = nm[0:-1]
	return nm

def archivoRed(interf,ip,gw,prefix):
	nm = netmask(prefix)
	r = "\n\n#Tarjeta de red estática"
	r += "\nauto %s" % interf
	r += "\niface %s inet static" % interf
	r += "\naddress %s" % ip 
	r += "\nnetmask %s" % nm
	r += "\ngateway %s" % gw
	return r

def copia(archivo, revert = False):
	backup = "/root/DrakkoTools/backup/copia-interfaces"
	backup_dir = "/root/DrakkoTools/backup"
	if revert == True:
		print(colored("[ ]","blue") + "Moviendo " + colored(backup,"blue") + " -> " + colored(archivo,"green"), end="\r")
		os.system("cp " + backup + " " + archivo)
		print(colored("[+]","green"))
		print(colored("[ ]","blue") + "Eliminando %s" % colored(backup,"red"), end="\r")
		os.system("rm -R %s" % backup_dir)
		print(colored("[+]","green"))
		return True
	else:
		if os.path.exists(backup):
			print(colored("[+]","green") + "Existe")
			print(colored("[ ]","blue") + "Restaurando copia de seguridad...", end="\r")
			os.system("cp " + backup + " " + archivo)
			print(colored("[+]","green") + "Copias de seguridad restauradas con éxito")
			return True
		else:
			print(colored("[-]","red") + "No existe")
			print(colored("[ ]","blue") + "Realizando copia de seguridad...", end="\r")
			if not os.path.exists(backup_dir):
				os.system("mkdir %s" % backup_dir + " && cp " + archivo + " " + backup)
			else:
				os.system("cp " + archivo + " " + backup)
			print(colored("[+]","green") + "Copia de seguridad hecha con éxito \rRuta: " + colored(backup,"yellow") )
			return True	

def configurarRed(interf, ip,prefix,gw,mac):
	archivo = "/etc/network/interfaces"
	time.sleep(1)
	conf = archivoRed(interf, ip,gw,prefix)
	print("\n" + colored("---[","blue") + "Iniciando configuración" + colored("]---","blue") + "\n")
	time.sleep(.25)
	print(colored("[+] Gateway ","green") + gw)
	time.sleep(.25)
	print(colored("[+] IP ","green") + ip)
	time.sleep(.25)
	print(colored("[+] Máscara ","green") + str(prefix))
	time.sleep(.25)
	mac = macGenerator()
	print(colored("[+] MAC ","green") + "%s" % mac)
	print("\n" + colored("---[","green") + "comprobando si hay copias de seguridad" + colored("]---","green"))
	copia(archivo)
	print(colored("[ ]","blue") + "Limpiando lista de direcciones...", end="\r")
	os.system("ip addr flush dev %s" % interf)
	os.system("ip route flush dev %s" % interf)
	print(colored("[+]","green") + "Lista de direcciones limpiada con éxito")
	time.sleep(.5)
	print(colored("[ ]","blue") + "Aplicando los cambios de red...", end="\r")
	os.system("echo \"%s\" >> " % conf + archivo)
	time.sleep(1)
	print(colored("[+]","green") + "Aplicando los cambios de red...")

	try:
		print(colored("[ ]","blue") + "Reiniciando servicios de red..." , end="\r")
		os.system("/etc/init.d/networking restart")
	except:
		print(("[-]","red") + "Hubo un error" + " " * 20)

	print(colored("[ ]","blue") + "Cambiando la MAC...", end="\r")
	os.system("ifconfig %s down" % interf)
	time.sleep(1)
	os.system("macchanger -m {0} {1}".format(mac,interf))
	time.sleep(1)
	os.system("ifconfig %s up" % interf)
	print(colored("[+]","green") + "MAC cambiada con éxito")
	print(colored("[ ]","blue") + "configurando la puerta de enlace...")
	os.system("route add default gw %s" % gw)
	print(colored("[+]","green") + "Puerta de enlace configurada correctamente")


if __name__ == '__main__':
	printData("eth0","192.168.1.8","b0:6e:bf:57:cf:46","255.255.255.0")
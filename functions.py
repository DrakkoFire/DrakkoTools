from __future__ import print_function
import os,time,json,shlex,subprocess,argparse,random,sys, getopt
from termcolor import colored

def info():
	print(colored("----------------------------------------------------------------","blue"))
	print("Code made By: " + colored("DrakkoFire", "red"))
	print("GitHub: " + colored("https://github.com/DrakkoFire", "red"))
	print("Freelancer: " + colored("https://www.freelancer.com/u/DrakkoFire","red"))
	print(colored("----------------------------------------------------------------","blue"))
	print("(¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) (¬‿¬) \n")

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

def getPieces(ip):
	a = ip.split(".")
	return a

def selInterface():
	a = True
	while a:
		try:
		    b = input("Selecciona la interfaz [eth0]: ")
		    if not b:
		        b = "eth0"
		        raise ValueError(colored("[+]","green")  + ' Interfaz ' +  colored(b,"green") + ' seleccionada')
		    else:
		    	print('Interfaz ' +  colored(b,"green") + ' seleccionada')
		    	return b
		    	a = False
		except ValueError as e:
		    print(e)
		    return b
		    a = False


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

def parse_args():
    parser = argparse.ArgumentParser(description='Generate random MAC address')
    parser.add_argument('-s', '--separator',
                        choices=sorted(SEPARATORS.keys()), default='colon',
                        help='What separator to use between the bytes in the output.')
    return parser.parse_args()

def macGenerator():
    args = parse_args()
    separator = SEPARATORS[args.separator]

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
	backup = "/root/cmac/backup/copia-interfaces"
	backup_dir = "/root/cmac/backup"
	if revert == True:
		print(colored("---[","blue") + "Moviendo " + colored(backup,"blue") + " -> " + colored(archivo,"green"))
		os.system("cp " + backup + " " + archivo)
		print(colored("---[","red") + "Eliminando %s" % colored(backup,"red"))
		os.system("rm -R %s" % backup_dir)
	else:
		if os.path.exists(backup):
			print(colored("---[","green") + "Existe")
			print(colored("---[","blue") + "Restaurando copia de seguridad...")
			os.system("cp " + backup + " " + archivo)
			print(colored("---[","green") + "Restaurado con éxito")
			return True
		else:
			print(colored("---[","red") + "No existe" + "\n" + colored("---[","blue") + "Realizando copia de seguridad...")
			if not os.path.exists(backup_dir):
				os.system("mkdir %s" % backup_dir + " && cp " + archivo + " " + backup)
			else:
				os.system("cp " + archivo + " " + backup)
			print(colored("---[","green") + "Copia de seguridad hecha en " + colored(backup,"blue") )
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
	print(colored("---[","blue") + "Limpiando lista de direcciones...")
	os.system("ip addr flush dev %s" % interf)
	os.system("ip route flush dev %s" % interf)
	print(colored(	"---[","green") + "Lista limpiada con éxito")
	time.sleep(.5)
	print(colored("---[","blue") + "Aplicando los cambios de red...")
	os.system("echo \"%s\" >> " % conf + archivo)
	time.sleep(1)

	try:
		print(colored("---[","blue") + "Reiniciando servicios de red...")
		os.system("/etc/init.d/networking restart")
	except:
		print(("---[","red") + "Hubo un error")

	#os.system("route add default gw %s" % gw)
	print("\n\n" + colored("---[","yellow") + "Cambiando la MAC" + colored("]---","yellow") + "\n\n")
	os.system("ifconfig %s down" % interf)
	time.sleep(1)
	os.system("macchanger -m {0} {1}".format(mac,interf))
	time.sleep(1)
	os.system("ifconfig %s up" % interf)
	print("\n\n" + colored("---[","blue") + "configurando la puerta de enlace...")
	os.system("route add default gw %s" % gw)


if __name__ == '__main__':
    #configurarRed("eth0","192.168.1.18", 24,"192.168.1.1", macGenerator())
    #info()
    copia("/etc/network/interfaces", revert=True)
    #getGw()
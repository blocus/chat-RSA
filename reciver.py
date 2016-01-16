#!/usr/bin/env python
# coding: utf-8
from time import localtime, strftime, time
import socket, string, random, subprocess
def now():
	return strftime("%H:%M:%S", localtime())

def egcd(a,b):
	x,y,u,v = 0,1,1,0
	while a != 0:
		q,r = b//a, b%a
		m,n = x-u*q, y-v*q
		b,a,x,y,u,v = a,r,u,v,m,n
	gcd = b
	return gcd, x, y
	
def modinv(a,m):
	gcd ,x,y = egcd(a,m)
	if gcd != 1:
		return None
	return x%m

def lpowmod(x,y,n):
	result = 1
	while y>0:
		if y&1>0:
			result = (result*x)%n
		y >>= 1
		x = (x*x)%n
	return result

def RSA(message,pub,mod):
	t = ""
	lenmod = len(hex(mod))-2
	print lenmod
	for char in message:
		RSAchar= hex(lpowmod(ord(char),pub,mod))[2:]
		t += "0"*(lenmod-len(RSAchar))+RSAchar
	return t

def DRSA(message,sec,mod):
	t = ""
	chars = []
	lenmod = len(hex(mod))-2
	while message != "":
		chars.append(message[:lenmod])
		message = message[lenmod:]
	for char in chars:
		t += chr(lpowmod(int(char,16),sec,mod))
	return t

def clear_list(l):
	tmp = []
	for e in l:
		if e != "":
			tmp.append(e)
	return tmp

def isan(ch):
	for i in ch:
		if i not in string.digits:
			return 0
	return 1

def isip(ch):
	ch = clear_list(ch.split("."))
	if len(ch) != 4:
		return 0
	else:
		for i in ch:
			if not isan(i):
				return 0
			if int(i) >255:
				return 0
		return 1
def prime (ch):
	ch = ch.split(" ")
	if "not" in ch:
		return 0
	else:
		return 1

def gen_alea_prime():
	random.seed()
	i = random.randint(1000, 9999)
	cmd = "openssl prime "
	res = subprocess.check_output(cmd+str(i),shell=True)
	while not prime(res):
		i += 1
		res = subprocess.check_output(cmd+str(i),shell=True)
	return i



print "Initiation des mes clés "
mykeys = {}
mykeys["ppr"] = gen_alea_prime()
mykeys["qpr"] = gen_alea_prime()
mykeys["nme"]=mykeys["ppr"]*mykeys["qpr"]
mykeys["phi"]=(mykeys["ppr"]-1)*(mykeys["qpr"]-1)
mykeys["pub"]=65537
mykeys["sec"] = modinv(mykeys["pub"],mykeys["phi"])
while 1:
	host = raw_input("Donner l'adresse IP du destinataire avec le port séparé par ':' \n exemple 127.0.0.1:55555 :")
	host = clear_list(host.split(":"))
	if isip(host[0]):
		if isan(host[1]):
			port = int(host[1])
			host = host[0]
			break

"""host = ""
port = 15555"""
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	mySocket.bind((host, port))
except Exception, e:
	print e
	exit()

while 1:
	mySocket.listen(5)
	client, adresse = mySocket.accept()
	client.send("#"+str(mykeys["pub"])+"#"+str(mykeys["nme"])+"#")
	while 1:
		rep = client.recv(1024)
		if rep[0] == "#" and rep[-1] == "#":
			rep = clear_list(rep.split("#"))
			if len(rep) == 2:
				if DRSA(rep[0],mykeys["sec"],mykeys["nme"]) == "O":
					pseudo = rep[1]
					print "clé publique envoyé avec succes"
					break
				else:
					client.close()
					mySocket.close()
					print("Erreur d'envoi de clé publique")
					exit()
	client.send("#OK#")
	while 1:
		rep = client.recv(1024)
		if rep != "":
			rep = DRSA(rep,mykeys["sec"],mykeys["nme"])
			print now(),pseudo+">",rep
			if rep.upper() == "FIN":
				break
	break
print "conversation fini avec", pseudo

client.close()
mySocket.close()

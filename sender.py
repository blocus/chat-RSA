#!/usr/bin/env python
# coding: utf-8

import string, socket


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


hiskeys = {}

while 1:
	host = raw_input("Donner l'adresse IP du destinataire avec le port séparé par ':' \nexemple 127.0.0.1:55555 :")
	host = clear_list(host.split(":"))
	if isip(host[0]):
		if isan(host[1]):
			port = int(host[1])
			host = host[0]
			break


try:
	pass
except Exception, e:
	raise e
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	mySocket.connect((host, port))
except socket.error:
	print "La liaison du socket à l'adresse choisie a échoué."
	exit()

while 1:
	rep = mySocket.recv(1024)

	while 1:
		if rep[0] == "#" and rep[-1] == "#":
			rep = clear_list(rep.split("#"))
			if len(rep) == 2:
				hiskeys["pub"] = int(rep[0])
				hiskeys["nhe"] = int(rep[1])
				pseudo = raw_input("Votre pseudo :")
				mySocket.send("#"+RSA("O",hiskeys["pub"],hiskeys["nhe"])+"#"+pseudo+"#")
				print "envoi du test de son clé publique"
				break
			else:
				mySocket.close()
				exit()
	print "envoyer 'FIN' pour terminer la conversation"
	while 1:
		rep = mySocket.recv(1024)
		if rep[0] == "#" and rep[-1] == "#":
			rep = clear_list(rep.split("#"))
			if len(rep) == 1 and rep[0] == "OK":
				break
			else:
				mySocket.close()
				exit()

	while 1:
		msg = raw_input(pseudo+"> ")
		mySocket.send(RSA(msg,hiskeys["pub"],hiskeys["nhe"]))
		if msg.upper() == "FIN":
			break
	break
print "conversation terminé"
mySocket.close()

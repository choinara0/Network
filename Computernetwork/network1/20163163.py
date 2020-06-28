#-*- coding:utf-8 -*-

# Student ID: 20163163
# Name: Nara Choi

import sys

from socket import *

GETCMD = "dl"
QUITCMD = "quit"

print("Student ID : 20163163")
print("Name : Nara Choi")

while(1):
	while(1):
		try:	
			PROMPT = input("\n > ")
			argv = PROMPT.split(" ")
			argc = len(argv)

			cmd = argv[0]

			if(cmd == ""):
				continue
			elif((cmd == QUITCMD) or (cmd.lower() == QUITCMD)):
				exit()
			elif(cmd != GETCMD):
				print("Wrong command %s"%cmd)
				continue;
		
			hostname = argv[1]
			pnum = int(argv[2])
			filename = argv[3]

			# NEED TO IMPLEMENT HERE
			request_msg = "GET {0} HTTP/1.0\r\nHost: {1}\r\nUser-Agent: HW1/1.0\r\nID:20163163\r\nName:Nara Choi\r\nConnection: close\r\n\r\n".format(filename, hostname)
			#print(request_msg)
		
			dl_file_name = filename.split("/")[-1]
		
			client_sock = socket(AF_INET,SOCK_STREAM)
			client_sock.connect((hostname, pnum))
		
			client_sock.send(request_msg.encode())
			#response_msg = client_sock.recv(1024)
			#print("=============== response_msg ===============\n" + response_msg)
			#print(response_msg)

			header =""
		
			content_len = 0
			HeaderPackage = None
			pernum = 0
			download = 0
			status = ""
			presize = 0
			HeaderStatusPackage = None
			HeaderStatus = ""
			while(1):
				header += client_sock.recv(1).decode()
				if(header.find("\r\n\r\n")>0):
					break
			HeaderPackage = header.split("\r\n")
			
			for word in HeaderPackage:
				if("Content-Length" in word):
					content_len = int(word.split(" ")[-1])
				if("HTTP" in word):
					HeaderStatusPackage = word.split(" ")[1:]

			for i in HeaderStatusPackage:
				#print(i,end=" ")
				HeaderStatus +=i + " "
			
			if(HeaderStatus.find("200 OK")<0):
				print(HeaderStatus)
				break

			print("Total Size %d bytes" % content_len)
			f = open(dl_file_name, 'wb')
			while(1):
				data = client_sock.recv(1024)
				if(len(data)<=0):
		            		break
				f.write(data)
				download += len(data)
				pernum = download * 100 / content_len
				status = "Current Downloading %d/%d (bytes) %d" % (download, content_len, pernum) + '%'

				if(pernum >= presize):
					if(presize==int(pernum/10)):
						continue
					print(status)
				presize=int(pernum/10)

			f.close()
			
			print("Download Complete: %s, %d/%d"%(dl_file_name,content_len,content_len))
		except IndexError:
			print("Wrong command")
			continue
		except error:
			print("%s: unknown host"%hostname)
			print("cannot connect to server %s %d" %(hostname,pnum))
			break





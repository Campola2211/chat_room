#Nicholas Campola
#Chat.py connects to a chat server and can load list of rooms, join rooms, and chat with other users
#I pledge that I have neither given nor received unauthorized help on this assignment
import socket
import sys
import select

HOST = "34.73.23.1"
PORT = 5220

#Creating the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

#variable to stay within the main menu
menucheck = 0
while(menucheck == 0):
	prompt = input("1. See Rooms Available \n2. Join a Room\nChoose option: ")

	#Seeing list of rooms
	if(prompt == "1"):
		mesg = "/list"
		#Getting number of rooms for printing
		data = mesg.encode()
		sock.sendall(data)
		data = sock.recv(1024)
		mesg = data.decode()
		#Printing out list of rooms
		for x in range(0, int(mesg)):
			data = sock.recv(1024)
			mesg = data.decode()
			print(mesg)


	#Joining Room
	elif(prompt == "2"):
		room = input("What room would you like to join: ")
		mesg = "/join " + room
		data = mesg.encode()
		sock.sendall(data)
		data = sock.recv(1024)
		mesg = data.decode()
		
	#Error Checking
	else:
		print("Wrong input choose either a 1 or a 2")


			
		
	#Preparing to join room
	if(prompt == "2"):
		#Server returns a 0 to let you join room
		if(mesg == "0"):
			print("Successfully joined " + room + "\n")
			#Error checking for names
			namecheck = 0
			#Properly leaves the menu screen
			menucheck = 1
			#Stays in while loop till name is given
			while(namecheck == 0):
				name = input("Please supply a username: ")
				user = "/nick " + name
				data = user.encode()
				sock.sendall(data)
				data = sock.recv(1024)
				mesg = data.decode()
				#Server sends confirmation that name works
				if(mesg == "0"):
					print("Name is now: " + name + "\n")
					namecheck = 1
					chat = 1
					while(chat == 1):
						reads, writes, errors = select.select([sock, sys.stdin], [], [])
						for x in reads:
							#Incoming Message
							if(x == sock):
								sock_data = sock.recv(1024)
								sock_mesg = sock_data.decode()
								print(sock_mesg)
							#Message to send
							if(x == sys.stdin):
								prompt = input()
								data = prompt.encode()
								sock.sendall(data)
							#Exiting the server
							if(prompt == "/logout"):
								print("Goodbye\n")
								sock.close()
								chat = 0
				#Name is incorrect formatting	
				elif(mesg == "1"):
					print("Format was incorrect please use NAME as the format\n")
				#Name is taken
				else:
					print("Name is taken, please use a new name")	
		#Room is incorrect format				
		else:
			print("Format was incorrect please use ROOM as the format\n")
	
		


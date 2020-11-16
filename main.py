from functions import int_input, connection, exit, send_command, read_callback
from amt import amt
from user import user

print('Welcome to AMT!\n\n')

while(True): # Log in section
	print('1) Sign in')
	print('2) Create a new profile')

	choice = int_input()
	
	if (choice == 1):
		try:
			user = user(1)
			break
		except ValueError:
			print('\nCan\'t find a user with this nickname!\n')
	elif (choice == 2):
		user = user(2)
		break
	else:
		print('Incorrect input')
    
print(f"\nHello, {user.name} {user.last_name}!\n")

while(True):
	print('Please, log into your FINAM Transaq Connector account\n')
	
	login = input('Enter a login: ')
	password = input('Enter a password: ')
	address = input('Enter an address of a server: ')
	port = input('Enter a port of a server: ')
	
	success = connection(login, password, address, port)
	
	if success == 0:
		break

while(True): # User section
	

	print('\n1) Open list of your portfolios')
	print('2) Exit')
	
	choice = int_input()
	
	if (choice == 1):
		amt(user)
	elif (choice == 2):
		break
	else:
		print('Incorrect input\n')

exit()


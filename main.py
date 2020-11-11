import security as sc
from functions import sign_in, new_profile, int_input, connection, exit
from amt import amt

user = {'nickname':'', 'name':'', 'last_name':'', 'portfolios':{}, 'budget':0}

print('Welcome to AMT!\n\n')

while(True): # Log in section
    print('1) Sign in')
    print('2) Create a new profile')
	
    choice = int_input()
    
    if (choice == 1):
        if sign_in(user): # if logged in successfully, 
            break         # otherwise give user a chance to create a new profile again
    elif (choice == 2):
        new_profile(user)
        break
    else:
        print('Incorrect input')
    
print(f"\nHello, {user['name']} {user['last_name']}!\n")

while(True):
	print('Please, log into your FINAM Transaq Connector account\n')
	
	login = input('Enter a login: ')
	password = input('Enter a password: ')
	address = input('Enter an address of a server: ')
	port = input('Enter a port of a server: ')
	
	success = connection(login, password, address, port)
	
	if success == 1:
		break

while(True): # User section
	print('')
	print('1) Open list of your portfolios')
	print('2) Exit')
	
	choice = int_input()
	
	if (choice == 1):
		amt(user)
	elif (choice == 2):
		break
	else:
		print('Incorrect input\n')

exit()


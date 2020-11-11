from functions import int_input, update_user_info, send_command
from security import security

# first, list all current portfolios, created by user
# user can chose one of his current portfolios to see new info 
# about his securities: individual expected returns and risks.
# Also, in portfolio menu there is an info regarding the whole portfolio 
# expected return and risk, if weights are present. User can manually chose them, 
# or let program calculate weights, which will minimize risk with regard to
# fixed expected return.

def amt(user):
	#---------------------------------------------------------#
	# This function is a main menu of a programm - it shows   #
	# a list of your portfolios, allows to delete and create  #
	# new ones.                                               #
	# params: user - dict                                     #
	#---------------------------------------------------------#
	
    print('')

    while(True):
        am_portf = len(user['portfolios'])
        portfolio_names = list(user['portfolios'].keys())
    
        for i in range(am_portf):
            print(f'{i+1}) { portfolio_names[i] }') # keys are names of portfolios
            
        print(f'{am_portf+1}) Create new portfolio')
        print(f'{am_portf+2}) Log out')
        
        choice = int_input()
        
		# choice MINUS 1 due to python indexation
        if (choice-1) in range(am_portf):
			# user->portfolios->chosen portfolio, with user's current budget (probably should be a portfolio feature)
            portfolio_menu(user['portfolios'][portfolio_names[choice-1]], user['budget'], portfolio_names[choice-1])
        elif choice == am_portf+1:
            create_portfolio(user)
        elif choice == am_portf+2:
            break
        else:
            print('Incorrect input\n')

# portfolio - list with chosen tickers, budget - int, portf_name - str
def portfolio_menu(portfolio, budget, portf_name):
	#---------------------------------------------------------#
	# This function lists all assets of this portfolio, shows #
	# key info such as expected return and risk of each asset #
	# and the portfolio.                                      #
	# params: portfolio - list, budget - int. portf_name - str#
	#---------------------------------------------------------#

	while(True):
		print(f'\nPortfolio {portf_name}', end='')
		
		am_assets = len(portfolio)
		
		# show risk and return of a portfolio
		#if am_assets > 0:
		#	print(risk and return)
		
		print()
		
		print('1) Add assets')
		print('2) Delete assets')
		if am_assets > 0:
			print('3) Optimize portfolio weights')
			print('4) Assign weights manually')
		
		choice = int_input()
		
		if choice == 1:
			new_asset = input('Enter a ticker: ')
			asset = security(new_asset)
			
		elif choice == 2:
			to_delete = input('Enter the ticker you wish to delete: ')
		elif (choice == 3) and (am_assets > 0):
			print('optimize')
		elif (choice == 4) and (am_assets > 0):
			print('manual')
		else:
			print('Incorrect input')
    
def create_portfolio(user):
	print('\nCreating portfolio\n')

	name = input('Enter portfolio name: ')
	
	user['portfolios'][name] = []
	update_user_info(user)
	
	print('\nPortfolio successfully created!\n')
	
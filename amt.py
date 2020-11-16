from functions import int_input, optimize, mean, var
from security import security
from user import user

# first, list all current portfolios, created by user
# user can chose one of his current portfolios to see new info 
# about his securities: individual expected returns and risks.
# Also, in portfolio menu there is an info regarding the whole portfolio 
# expected return and risk, if weights are present. User can manually chose them, 
# or let program calculate weights, which will minimize risk with regard to
# fixed expected return.

def update(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		args[0].update_user_info()
	
	return inner

@update
def adding_asset(user, portfolio, asset_list):
	new_asset = input('Enter a ticker: ')
	asset = security(new_asset, period = portfolio['candle_period_id'], am_candles = portfolio['am_candles'])
	portfolio['assets'].append(new_asset)
	asset_list.append(asset)

@update
def deleting_asset(user, portfolio, asset_list):
	to_delete = input('Enter the ticker you wish to delete: ')
	
	if to_delete in portfolio['assets']:
		portfolio['assets'].remove(to_delete)
	else:
		raise ValueError
		
	for asset in asset_list:
		if asset.name == to_delete:
			del asset

def amt(user):
	#---------------------------------------------------------#
	# This function is a main menu of a programm - it shows   #
	# a list of your portfolios, allows to delete and create  #
	# new ones.                                               #
	# params: user - <class 'user'>                           #
	#---------------------------------------------------------#
	
    print('')

    while(True):
        for i in range(user.am_portf):
            print(f'{i+1}) { user.portfolio_names[i] }') 
            
        print(f'{user.am_portf+1}) Create new portfolio')
        print(f'{user.am_portf+2}) Log out')
        
        choice = int_input()
        
		# choice MINUS 1 due to python indexation
        if (choice-1) in range(user.am_portf):
			# user->portfolios->chosen portfolio
            portfolio_menu(user, user.portfolio_names[choice-1])
        elif choice == user.am_portf+1:
            create_portfolio(user)
        elif choice == user.am_portf+2:
            break
        else:
            print('Incorrect input\n')

def portfolio_menu(user, portf_name):
	#---------------------------------------------------------#
	# This function lists all assets of this portfolio, shows #
	# key info such as expected return and risk of each asset #
	# and the portfolio.                                      #
	# params: user - <class 'user'>, portf_name - str         #
	#---------------------------------------------------------#
	print('Loading portfolio...')
	portfolio = user.get_portfolio(portf_name)
	asset_list = [security(name, period = portfolio['candle_period_id'], am_candles = portfolio['am_candles']) for name in portfolio['assets']]

	while(True):
		print(f'\nPortfolio {portf_name}\n')
		
		am_assets = len(portfolio['assets'])
		
		if asset_list[0].weight is not None:
			print(f'Portfolio Exp. Ret.={mean(asset_list):.6f} Exp. Risk={var(asset_list):.6f}\n')
		
		for asset in asset_list:
			if asset.weight is None:
				print("n.w. ", end='')
			else:
				print(f'{asset.weight:.6f}', end=' ')
		
			print(f"{asset.name} Exp. Ret.={asset.exp_ret:.6f} Exp. Risk={asset.exp_risk:.6f}")
		
		print()
		
		print('1) Add assets')
		if am_assets > 0:
			print('2) Delete assets')
			print('3) Optimize portfolio weights')
			print('4) Return to portfolio menu')
		else:
			print('2) Return to portfolio menu')
		
		choice = int_input()
		
		if choice == 1:
			try:
				adding_asset(user, portfolio, asset_list)
			except ValueError:
				print('There is no such ticker!\n')		
				
		elif (choice == 2) and (am_assets == 0):
			break
			
		elif (choice == 2) and (am_assets > 0):
			try:
				deleting_asset(user, portfolio, asset_list)
			except ValueError:
				print("There is no such ticker in your portfolio!")	
				
		elif (choice == 3) and (am_assets > 0):
			ret = float(input("Type desired return: "))
		
			optimize(asset_list, ret)
		
		elif (choice == 4) and (am_assets > 0):
			break
				
		else:
			print('Incorrect input')
   
@update
def create_portfolio(user):
	print('\nCreating portfolio\n')

	name = input('Enter portfolio name: ')
	
	user.user_info['portfolios'][name] = {}
	
	portfolio = user.get_portfolio(name)
	
	print("Specify period for candles to cover\n")
	
	print("1) 1 minute")
	print("2) 5 minutes")
	print("3) 15 minutes")
	print("4) 1 hour")
	print("5) 1 day")
	print("6) 1 week")
	
	period_id = int_input()
	
	print("Specify how many candles should be used: ")
	am_candles = int_input()
	
	portfolio["candle_period_id"] = period_id
	portfolio["am_candles"] = am_candles
	portfolio["assets"] = []
	
	print('\nPortfolio successfully created!\n')
	
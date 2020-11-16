import ctypes
import os
import time
from bs4 import BeautifulSoup
from scipy.optimize import Bounds, LinearConstraint, minimize
import numpy as np
from numba import njit

path = os.getcwd()
lib = ctypes.WinDLL(path+"\\assets\\connect.dll")
lib.SendCommand.restype = ctypes.POINTER(ctypes.c_char)
lib.InitializeEx.restype = ctypes.POINTER(ctypes.c_char)

dll_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_char))

def var(asset_list):
	return risk(np.array([asset.weight for asset in asset_list]), np.array([[asset.cov(asset2) for asset2 in asset_list] for asset in asset_list]))
	
def mean(asset_list):
	return sum([asset.exp_ret*asset.weight for asset in asset_list])

@njit
def risk(x, A):
	return np.dot(x, np.dot(A, x))

def optimize(asset_list, ret):
	n = len(asset_list)

	#bounds = Bounds(*([0, 1] for i in range(n)))
	linear_constraint = LinearConstraint([[1 for i in range(n)], [asset.exp_ret for asset in asset_list]], [1-0.0000001, ret-0.0000001], [1+0.0000001, ret+0.0000001])

	x0 = np.array([1/n for i in range(n)])
	
	A = np.array([[asset.cov(asset2) for asset2 in asset_list] for asset in asset_list])
	
	res = minimize(risk, x0, A, options={'disp': 0},  constraints=linear_constraint, method='trust-constr')
	
	for i in range(n):
		asset_list[i].update_weights(res.x[i])

def historical_info(name, board, period, am_candles):
	#---------------------------------------------------------#
	# Function pulls historical info for specified security   #
	# params: name - str                                      #
	#---------------------------------------------------------#
	command = f"""
		<command id=\"gethistorydata\">
			<security>
				<board>{board}</board>
				<seccode>{name}</seccode>
			</security>
			<period>{period}</period>
			<count>{am_candles}</count>
			<reset>true</reset>
		</command>
	"""
	
	err = send_command(command)
	
	if err:
		raise SystemExit
	
	time_0 = time.time()
	while time.time() - 4 < time_0: # wait to listen to all callback from command
		pass
	
	xml = read_callback()
	candles = xml.candles.find_all('candle')
	
	data = [(float(candles[i]['open']), float(candles[i]['close']))  for i in range(len(candles))]
	
	return data
	
def list_of_tickers():
	#---------------------------------------------------------#
	# Function pulls a list of all tickers on exchange.       #
	# params: arr - list                                      #
	#---------------------------------------------------------#

	err = send_command(r'<command id="get_securities" />')
	
	if err:
		raise SystemExit
		
	xml = read_callback()
	seccodes = xml.securities.find_all('seccode')
	boards = xml.securities.find_all('board')
	
	return [(seccodes[i].string, boards[i].string) for i in range(len(seccodes))]
	
@dll_callback
def callback(msg):
	# --------- reading from callback ---------- #
	i = 0
	tmp = str()
	
	while True:
		try:
			tmp = tmp + msg[i].decode()
		except UnicodeDecodeError: # found the end of msg
			break
		i+=1
	
	while tmp[i-1] != '>': # strip this string of some strange symbols (no idea where they come from)
		i-=1
	
	tmp = tmp[:i]
	
	# -------------- freeing memory ------------ #
	free_memory(msg)
	
	# -------- parsing callback message -------- #
	with open('tmp\\callback.xml', mode='w', encoding='utf-8') as f:
		f.write(tmp)
	
	return 0

def read_callback():
	#parse callback here
	time_0 = time.time()
	
	while time.time() - 5 < time_0: # wait to listen to callback
		pass
	
	with open("tmp\\callback.xml", mode='r', encoding="utf-8") as f:
		xml = BeautifulSoup(f, 'xml')
		
	return xml

def send_command(command):
	#---------------------------------------------------------#
	# Function sends a command to the server                  #
	# params: command - str (xml)                             #
	# returns: 0 if everything OK; 1 if there is a mistake    #
	#---------------------------------------------------------#
	
	err_ptr = lib.SendCommand(command.encode())
	err = error_handling(err_ptr)
	
	free_memory(err_ptr)
	
	# for a while
	err = 0

	return err

def free_memory(ptr):
	#---------------------------------------------------------#
	# function simply clears memory from messages from server #
	# params: ptr - ctypes.POINTER(ctypes.c_char)             #
	#---------------------------------------------------------#

	err = lib.FreeMemory(ptr)
	
	if not err:
		raise SystemExit

def error_handling(msg):
	# some xml parsing methods
	
	return 0
    
def int_input():
	#---------------------------------------------------------#
	# Function helps prevent ValueError when int(input())     #
	# is called                                               #
	# returns: choice - int
	#---------------------------------------------------------#
    while(True):
        try:
            print('Choose an option: ', end='')
            choice = int(input())
            break
        except ValueError:
            print('Incorrect input')
            
    return choice

def connection(login, password, address, port):
	#---------------------------------------------------------#
	# Function establishes connection with transaq, sets a    #
	# callback function and connects to a server.             #
	# params: login, password, address, port - str;           #
	# returns: 0 if everything OK; 1 if there is a mistake    #
	#---------------------------------------------------------#

	# ------------------ Initializing transaq ----------------------- #
	log_path = '\"'+path+"\\logs\\"+'\"' # specifying the location of logs
	log = f"<init log_path={log_path} log_level=\"2\" />"

	status_init = lib.InitializeEx(log.encode()) # initialize the finam transaq

	if bool(status_init):
		print('Can\'t initialize library. Restart the application')
		free_memory(status_init)
		raise SystemExit
		
	free_memory(status_init)	
	
	# ----------- Setting callback function ------------------------- #
	err = lib.SetCallback(callback)
	
	if not err:
		print('Error! Restart the application')
		raise SystemExit
	
	# -------------- logging in ------------------------------------- #
	login = 'TCNN9930'
	password = 'SULYsu'
	address = 'tr1-demo5.finam.ru'
	port = '3939'
	
	#<rqdelay> - delay between addressing to the server
	connect = f"""
		<command id=\"connect\">
			<login>{login}</login>
			<password>{password}</password>
			<host>{address}</host>
			<port>{port}</port>
			<language>en</language>
			<rqdelay>10</rqdelay>
			<milliseconds>false</milliseconds>
			<utc_time>true</utc_time>
			
		</command>
	"""
	
	err = send_command(connect)	
	
	time_0 = time.time()
	print('Connecting...')
	while time.time() - 3 < time_0: # wait to listen to all callback from connect
		pass
	
	return error_handling(err)
	
def exit():
	#---------------------------------------------------------#
	# Function is called when the program is terminated       #
	#---------------------------------------------------------#
	err = send_command("<command id=\"disconnect\"/>")
	error_handling(err)
	
	err = lib.UnInitialize()
	
	if bool(err) == True:
		print('Failed to uninitialize. Forced to close the app')
		raise SystemExit
	
	with open('tmp\\callback.xml', mode='w', encoding='utf-8') as f: # make callback.xml empty
		pass
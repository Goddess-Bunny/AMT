import requests
import ctypes
import os
from bs4 import BeautifulSoup
from functions import send_command, free_memory

path = os.getcwd()
lib = ctypes.WinDLL(path+"\\assets\\connect.dll")
lib.SendCommand.restype = ctypes.c_wchar_p

dll_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_char))

xml = str()

@dll_callback
def callback(msg):
	# some xml parsing methods
	global xml
	
	# --------- reading from callback ---------- #
	i = 0
	tmp = str()
	
	while msg[i] != '\0':
		tmp = tmp + msg[i].decode()
	# -------------- stop reading -------------- #
	
	free_memory(msg)
	
	clbk_xml = BeautifulSoup(tmp, 'xml')
	print(clbk_xml)
	
	return 0
	
def set_callback():
	err = lib.SetCallback(callback)
	
	if not err:
		raise 'Error! Restart the application'
		

class security(object):
	name = str()

	def __init__(self, name):
		self.name = name
		
		
	
	
			
			
import requests
import ctypes
from bs4 import BeautifulSoup

path = os.getcwd()
lib = ctypes.WinDLL(path+"\\assets\\connect.dll")
lib.SendCommand.restype = ctypes.c_wchar_p

dll_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_char_p)

class security(object):
	def __init__(self, name):
		print('cre')
		
	@dll_callback
	def callback(self, msg):
		# some xml parsing methods
		xml = BeautifulSoup(msg)
		
		return 0
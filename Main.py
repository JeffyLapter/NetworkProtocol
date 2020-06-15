# This is the Main FILE OF client #
from tkinter import ttk
import tkinter as tk
import json

#-- global variables --#
Config_ini_path="./config.json"
FLUSH_FLAG=False


class Config_Loader:
    def __init__(self,path):#path requires a Config file which defined at the begining of this file
        self.config_dict={}
        with open(path,'r') as fread:
            self.config_dict=json.load(fread)
        self.number_of_server=len(self.config_dict['Server_List'])

    def get_server_list_from_config(self):#return a Two dimensions list from config.json
        server_list=[]
        for i in range(0,self.number_of_server):
            server_list.append([self.config_dict['Server_List'][i]['host'],self.config_dict['Server_List'][i]['port']])
        return server_list#[['xx.xx.xx.xx', 8808], ['xx.xx.xx.xx', 8777]]

    def modify_server_from_gui(self,host_input,port_input):
        pass
    
    def add_server_from_gui(self,host_input,port_input):
        pass
    
    def remove_server_from_gui(self,host_input):
        pass

            
            
E=Config_Loader(Config_ini_path)
print(E.get_server_list_from_config())
#--GUI INIT_WINDOW--#
#MainWindow=tk.Tk()
#MainWindow.title('Lapter&NothingH `s Network Client Alpha 0.0.1')
#MainWindow.iconbitmap("") #icon defines here

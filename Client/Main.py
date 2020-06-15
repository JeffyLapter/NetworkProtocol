# This is the Main FILE OF client #
from tkinter import ttk
import tkinter as tk
import json
from os import system

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
        print('modify_server_from_gui')
        pass

    def add_server_from_gui(self,host_input,port_input):
        print('add_server_from_gui')
        pass
    
    def remove_server_from_gui(self,host_input):
        print('remove_server_from_gui')
        pass

GLOBAL_Configuration=Config_Loader(Config_ini_path)

#--GUI INIT_WINDOW--#
MainWindow=tk.Tk()
MainWindow.title('Lapter&NothingH `s Network Client Alpha 0.0.1')
MainWindow.geometry('730x300')
#MainWindow.iconbitmap("") #icon defines here

#menu level 0
MenuBar=tk.Menu(MainWindow)

Filemenu=tk.Menu(MenuBar,tearoff=0)
Setting=tk.Menu(MenuBar,tearoff=0)
Proxymod=tk.Menu(Setting,tearoff=0)
ProxySetting=tk.Menu(Setting,tearoff=0)

MenuBar.add_cascade(label='文件',menu=Filemenu)
MenuBar.add_cascade(label='设置',menu=Setting)

#--文件菜单--#
def Open_Config_Directory():
    system("notepad.exe "+Config_ini_path)
Filemenu.add_cascade(label='打开配置文件',command=Open_Config_Directory)
Filemenu.add_cascade(label='退出',command=MainWindow.quit)

#--设置菜单--#

Setting.add_cascade(label='代理模式',menu=Proxymod)
Proxymod.add_radiobutton(label='自动选路')
Proxymod.add_radiobutton(label='手动模式')
Setting.add_cascade(label='代理设置',menu=ProxySetting)
ProxySetting.add_cascade(label='添加新服务器',command=GLOBAL_Configuration.add_server_from_gui)
ProxySetting.add_cascade(label='修改服务器配置',command=GLOBAL_Configuration.add_server_from_gui)
ProxySetting.add_cascade(label='添加新服务器',command=GLOBAL_Configuration.add_server_from_gui)

MainWindow.config(menu=MenuBar)
MainWindow.mainloop()


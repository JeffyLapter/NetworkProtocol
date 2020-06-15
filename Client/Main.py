# This is the Main FILE OF client #
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import json
from os import system

#-- global variables --#
Config_ini_path="./Client/config.json"
FLUSH_FLAG=False
auto_proxy=1

class Config_Loader:
    def __init__(self,path):#path requires a Config file which defined at the begining of this file
        self.config_dict={}
        self.auto_proxy=1
        with open(path,'r') as fread:
            self.config_dict=json.load(fread)
        self.number_of_server=len(self.config_dict['Server_List'])
    
    def Flush_all(self,path):
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

def USE_MANUAL_PROXY_CHANGE(config=GLOBAL_Configuration):
    config.auto_proxy=0
    tkinter.messagebox.showinfo(title='Success',message='切换为手动模式')

def USE_AUTO_PROXY_CHANGE(config=GLOBAL_Configuration):
    config.auto_proxy=1
    tkinter.messagebox.showinfo(title='Success',message='切换为自动模式')

Proxymod.add_radiobutton(label='自动选路',command=USE_AUTO_PROXY_CHANGE)
Proxymod.add_radiobutton(label='手动模式',command=USE_MANUAL_PROXY_CHANGE)

Setting.add_cascade(label='代理设置',menu=ProxySetting)

def Add_server():
    GLOBAL_Configuration.add_server_from_gui(1,1)

def Modify_server():
    GLOBAL_Configuration.modify_server_from_gui(1,1)
    
def Del_server():
    confirm=tkinter.messagebox.askyesno(title='警告!',message='你确定要移除所有存在的服务器么?')
    if confirm:
        try:
            GLOBAL_Configuration.remove_server_from_gui(1)
            GLOBAL_Configuration.Flush_all(Config_ini_path)            
            tkinter.messagebox.showinfo(title='Success',message='所有服务器已被清空')
        except:    
            tkinter.messagebox.showerror(title='Error!',message='操作失败')
    else:
        pass

ProxySetting.add_cascade(label='添加新服务器',command=Add_server)
ProxySetting.add_cascade(label='修改服务器配置',command=Modify_server)
ProxySetting.add_cascade(label='删除所有存在的服务器',command=Del_server)

MainWindow.config(menu=MenuBar)
MainWindow.mainloop()

'''
要解决的问题：
json写入，修改，自动化udp选路模块
'''
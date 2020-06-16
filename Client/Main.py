# This is the Main FILE OF client #
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

import tkinter.font as tkFont
import json
from os import system
import C_Delay_Test

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
MainWindow.geometry('390x400')
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



def Modify_server():
    Proxy_Manager_Window=tk.Toplevel(MainWindow)
    Proxy_Manager_Window.title('添加与修改服务器')
    Proxy_Manager_Window.geometry('280x320')
    Modify_Frame=tk.LabelFrame(Proxy_Manager_Window,text='代理服务器设置',fg='blue')
    Modify_Frame.grid(padx=5,pady=5,sticky=tk.W)
    Modify_introduce=tk.Label(Modify_Frame,text='添加或删除服务器')
    Modify_introduce.grid(padx=5,pady=5,sticky=tk.W)
    pass

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


ProxySetting.add_cascade(label='添加与修改服务器',command=Modify_server)
ProxySetting.add_cascade(label='删除所有存在的服务器',command=Del_server)

MainWindow.config(menu=MenuBar)
#----------------Menu bar ends--------------------#





#-----------------Connect-------------------#
Connection_Manager_Frame=tk.LabelFrame(MainWindow,text="连接管理",fg='blue',padx=5,pady=5)
Connection_Manager_Frame.grid(padx=10,pady=10,sticky='w')


ft = tkFont.Font(family='Fixdsys', size=13, weight=tkFont.NORMAL)

label_Server_chose=tk.Label(Connection_Manager_Frame,text="请选择代理服务器",padx=8,pady=8,font=ft)
label_Server_chose.grid(column=0,row=0,sticky='w')

Server_Chosen_Now=tk.StringVar()
Server_List_Select_combox=ttk.Combobox(Connection_Manager_Frame,textvariable=Server_Chosen_Now,)

Server_ip_List=[i[0] for i in GLOBAL_Configuration.get_server_list_from_config()]
Server_port_list=[i[1] for i in GLOBAL_Configuration.get_server_list_from_config()]
tupled_server_in_combox=[]

for i in range(0,GLOBAL_Configuration.number_of_server):
    tupled_server_in_combox.append(Server_ip_List[i]+':'+str(Server_port_list[i]))

Server_List_Select_combox['value']=tuple(tupled_server_in_combox)
Server_List_Select_combox.grid(column=0,row=1,padx=8,pady=4)

#延迟测试

def Delay_Test():
    print('Delay_Test')

Delay_Test_Button=tk.Button(Connection_Manager_Frame,text='延迟测试',font=ft,width=8,height=3,padx=4,pady=4,command=Delay_Test)
Delay_Test_Button.grid(column=1,row=0,rowspan=2)

#连接
def Connect():
    print('Try Connect')
Connection_Button=tk.Button(Connection_Manager_Frame,text='连接',font=ft,width=8,height=3,padx=4,pady=4,command=Connect)
Connection_Button.grid(column=2,row=0,rowspan=2)


#---------------Status---------------------#
status_ft=tkFont.Font(family='Airal',size=13,weight=tkFont.BOLD)

Connect_Status_Frame=tk.LabelFrame(MainWindow,text="连接状态",fg='blue',padx=5,pady=5)
Connect_Status_Frame.grid(padx=10,pady=3,columnspan=2,sticky='w')
Connect_Status_Lable=tk.Label(Connect_Status_Frame,text="当前服务器连接状态:",font=ft,padx=10,pady=8)
Connect_Status_Lable.grid(column=0,row=0)


Conn_status_var=tk.StringVar()
Conn_status_var.set('    连接成功   ')
#Conn_status_var.set('    连接错误   ')
#Conn_status_var.set('    未连接     ')
#Conn_status_var.set('   正在连接... ')
Conn_label=tk.Label(Connect_Status_Frame,textvariable=Conn_status_var,font=status_ft,fg='green',padx=10)
Conn_label.grid(column=1,row=0,sticky='w')


#--------------日志-------------------#

record_frame=tk.LabelFrame(MainWindow,text="日志",fg='blue',padx=5,pady=5)
record_frame.grid(column=0,padx=10,pady=3,columnspan=2,sticky='w')
#record_Lable=tk.Label(record_frame,text="当前服务器连接状态:",font=ft,padx=10,pady=8)
#record_Lable.grid(column=0,row=0)
#Recording_Var=tk.StringVar()
#Recording_String='sssssssssssssssssssssssss'
#Recording_Var.set(Recording_String)
record_Text=tk.Text(record_frame,width=48,height=12)


record_Text.grid(sticky='w')
record_Text.insert(tk.END,'test')
record_Text.configure(state='disabled')


scroll=tk.Scrollbar(record_frame)
scroll['command']=record_Text.yview
scroll.grid(column=1,row=0,sticky=tk.S + tk.W + tk.E + tk.N)



MainWindow.mainloop()

'''
要解决的问题：
json写入，修改，自动化udp选路模块
'''
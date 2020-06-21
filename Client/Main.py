# This is the Main FILE OF client #
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

import tkinter.font as tkFont
import json
from os import system
from C_Modules import Delay_Test_Module

#-- global variables --#
Config_ini_path="./Client/config.json"
FLUSH_FLAG=False
CONNECT_STATUS=0
auto_proxy=1

class Config_Loader:
    def __init__(self,path):#path requires a Config file which defined at the begining of this file
        self.config_dict={}
        self.auto_proxy=1
        with open(path,'r') as fread:
            self.config_dict=json.load(fread)
        self.number_of_server=len(self.config_dict['Server_List'])
    
    def get_server_list_from_config(self):#return a Two dimensions list from config.json
        server_list=[]
        for i in range(0,self.number_of_server):
            server_list.append([self.config_dict['Server_List'][i]['host'],self.config_dict['Server_List'][i]['port']])
        return server_list#[['xx.xx.xx.xx', 8808], ['xx.xx.xx.xx', 8777]]

    def get_server_list_fomatable(self):
        Server_ip_List=[i[0] for i in self.get_server_list_from_config()]
        Server_port_list=[i[1] for i in self.get_server_list_from_config()]
        tupled_server_in_combox=[]
        for i in range(0,self.number_of_server):
            tupled_server_in_combox.append(Server_ip_List[i]+':'+str(Server_port_list[i]))
        return tupled_server_in_combox

    def Flush_all(self,path):
        self.config_dict={}
        with open(path,'r') as fread:
            self.config_dict=json.load(fread)
        self.number_of_server=len(self.config_dict['Server_List'])

    def modify_server_from_gui(self,host_input,port_input):
        print('modify_server_from_gui')
        pass

    def add_server_from_gui(self,host_input,port_input):
        print('add_server_from_gui')
        temp_already=0
        global FLUSH_FLAG
        global Config_ini_path
        for i in self.config_dict['Server_List']:
            if i['host']==host_input and i['port']==eval(port_input):
                print('already added')
                temp_already=1
            else:
                pass
        if temp_already==0:
            self.config_dict['Server_List'].append({'host':host_input,'port':eval(port_input)})
            server_dict_to_json=json.dumps(self.config_dict)
            with open(Config_ini_path,'w') as fw:
                fw.write(server_dict_to_json)
                fw.close()
            FLUSH_FLAG=True
            #print(self.config_dict['Server_List'])
        
    
    def remove_server_from_gui(self,host_input,port_input):
        global FLUSH_FLAG
        global Config_ini_path
        for i in self.config_dict['Server_List']:
            if i['host']==host_input and i['port']==eval(port_input):
                #print(i)
                #print(self.config_dict['Server_List'])

                self.config_dict['Server_List'].remove(i)
                
                print('remove_server_from_gui')
                #print(self.config_dict['Server_List'])
                with open(Config_ini_path,'w') as fw:
                    fw.write(json.dumps(self.config_dict))
                    fw.close()
                FLUSH_FLAG=True
            else:
                pass

GLOBAL_Configuration=Config_Loader(Config_ini_path)


#print(GLOBAL_Configuration.get_server_list_from_config())


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
    global FLUSH_FLAG
    FLUSH_FLAG=True
    system("notepad.exe "+Config_ini_path)
    
Filemenu.add_cascade(label='打开配置文件',command=Open_Config_Directory)
Filemenu.add_cascade(label='退出',command=MainWindow.quit)

#--设置菜单--#

Setting.add_cascade(label='代理模式',menu=Proxymod)

def USE_MANUAL_PROXY_CHANGE():
    global auto_proxy
    auto_proxy=0
    tkinter.messagebox.showinfo(title='Success',message='切换为手动模式')

def USE_AUTO_PROXY_CHANGE():
    global auto_proxy
    auto_proxy=1
    tkinter.messagebox.showinfo(title='Success',message='切换为自动模式')

Proxymod.add_radiobutton(label='自动选路',command=USE_AUTO_PROXY_CHANGE)
Proxymod.add_radiobutton(label='手动模式',command=USE_MANUAL_PROXY_CHANGE)

Setting.add_cascade(label='代理设置',menu=ProxySetting)


#-----------------Connect-------------------#
Connection_Manager_Frame=tk.LabelFrame(MainWindow,text="连接管理",fg='blue',padx=5,pady=5)
Connection_Manager_Frame.grid(padx=10,pady=10,sticky='w')


ft = tkFont.Font(family='Fixdsys', size=13, weight=tkFont.NORMAL)

label_Server_chose=tk.Label(Connection_Manager_Frame,text="请选择代理服务器",padx=8,pady=8,font=ft)
label_Server_chose.grid(column=0,row=0,sticky='w')

Server_Chosen_Now=tk.StringVar()
Server_List_Select_combox=ttk.Combobox(Connection_Manager_Frame,textvariable=Server_Chosen_Now,)
Server_List_Select_combox['value']=tuple(GLOBAL_Configuration.get_server_list_fomatable())
Server_List_Select_combox.grid(column=0,row=1,padx=8,pady=4)

def Server_Chosen_Cobox():
    global FLUSH_FLAG
    global Server_List_Select_combox
    global GLOBAL_Configuration
    global Connection_Manager_Frame
    global Config_ini_path
    if FLUSH_FLAG==True:
        Server_List_Select_combox.destroy()
        GLOBAL_Configuration.Flush_all(Config_ini_path)
        Server_Chosen_Now=tk.StringVar()
        Server_List_Select_combox=ttk.Combobox(Connection_Manager_Frame,textvariable=Server_Chosen_Now,)
        Server_List_Select_combox['value']=tuple(GLOBAL_Configuration.get_server_list_fomatable())
        Server_List_Select_combox.grid(column=0,row=1,padx=8,pady=4)
        FLUSH_FLAG=False
    else:
        pass
    MainWindow.after(1000,Server_Chosen_Cobox)



def Modify_server():
    
    Proxy_Manager_Window=tk.Toplevel(MainWindow)
    Proxy_Manager_Window.title('添加与修改服务器')
    Proxy_Manager_Window.geometry('290x320')
    Modify_Frame=tk.LabelFrame(Proxy_Manager_Window,text='代理服务器设置',fg='blue')
    Modify_Frame.grid(padx=5,pady=5,sticky=tk.W)
    Modify_introduce=tk.Label(Modify_Frame,text='添加或删除服务器')
    Modify_introduce.grid(padx=5,pady=5,sticky=tk.W)
    
    temp_server_list=tk.StringVar()
    temp_server_list.set(tuple(GLOBAL_Configuration.get_server_list_fomatable()))

    Modify_List_Box=tk.Listbox(Modify_Frame,listvariable=temp_server_list)
    
    scroll_bar_proxy_setting=tk.Scrollbar(Modify_Frame)
    scroll_bar_proxy_setting['command']=Modify_List_Box.yview
    scroll_bar_proxy_setting.grid(column=1,sticky=tk.S+tk.W+tk.E+tk.N)

    Modify_List_Box.grid(padx=5,pady=5,ipadx=5,ipady=5,column=0,row=1,sticky=tk.W)

    Modify_Button_Frame=tk.LabelFrame(Proxy_Manager_Window,text='')
    Modify_Button_Frame.grid(padx=3,pady=15,column=1,row=0,sticky=tk.W+tk.N)

    #-----------------add
    def Server_add():
        ADD_SERVER_WINDOW=tk.Toplevel(Proxy_Manager_Window)
        ADD_SERVER_WINDOW.geometry('290x115')
        ADD_SERVER_WINDOW_ENTRY_Label=tk.Label(ADD_SERVER_WINDOW,text='服务器地址:',font=ft)
        ADD_SERVER_WINDOW_ENTRY_Label.grid(sticky=tk.W,column=0,row=0,padx=8,pady=8)
        ADD_SERVER_WINDOW_ENTRY_HOST=tk.Entry(ADD_SERVER_WINDOW,width=21)
        ADD_SERVER_WINDOW_ENTRY_HOST.grid(sticky=tk.W,column=1,row=0,padx=4,pady=8)

        ADD_SERVER_WINDOW_ENTRY_PORT_Label=tk.Label(ADD_SERVER_WINDOW,text='端口:',font=ft)
        ADD_SERVER_WINDOW_ENTRY_PORT_Label.grid(sticky=tk.W,column=0,row=1,padx=8,pady=4)
        ADD_SERVER_WINDOW_ENTRY_PORT=tk.Entry(ADD_SERVER_WINDOW,width=21)
        ADD_SERVER_WINDOW_ENTRY_PORT.grid(sticky=tk.W,column=1,row=1,padx=4,pady=4)
        def SERVER_ADD_CONFIRM():
            global FLUSH_FLAG
            host=ADD_SERVER_WINDOW_ENTRY_HOST.get()
            port=ADD_SERVER_WINDOW_ENTRY_PORT.get()
            GLOBAL_Configuration.add_server_from_gui(host,port)
            FLUSH_FLAG=True
            ADD_SERVER_WINDOW.destroy()

        ADD_SERVER_WINDOW_CONFIRM_BUTTON=tk.Button(ADD_SERVER_WINDOW,text='确定',width=25,command=SERVER_ADD_CONFIRM)
        ADD_SERVER_WINDOW_CONFIRM_BUTTON.grid(sticky=tk.W+tk.E,column=0,columnspan=2,row=2,padx=14,pady=4)
        pass

    add_button=tk.Button(Modify_Button_Frame,text='添加',width=8,height=1,command=Server_add)
    add_button.grid(padx=5,pady=5,column=0,row=0,sticky=tk.W)
    
    #-----------------edit
    def Server_edit():
        pass

    edit_button=tk.Button(Modify_Button_Frame,text='编辑',width=8,height=1,command=Server_edit)
    edit_button.grid(padx=5,pady=5,column=0,row=1,sticky=tk.W)

    #-----------------DEL
    def Server_del_single():
        global FLUSH_FLAG
        global GLOBAL_Configuration
        del_chosen_now=Modify_List_Box.get(tk.ACTIVE)
        SERVER_SELECTED=del_chosen_now.split(':')
        print(SERVER_SELECTED,'-Deleted')
        GLOBAL_Configuration.remove_server_from_gui(SERVER_SELECTED[0],SERVER_SELECTED[1])
        #print(del_chosen_now)
        Modify_List_Box.delete(tk.ACTIVE)

        

    del_button=tk.Button(Modify_Button_Frame,text='删除',width=8,height=1,command=Server_del_single)
    del_button.grid(padx=5,pady=5,column=0,row=2,sticky=tk.W)
    #----------------SAVE
    def Server_save():
        pass

    save_button=tk.Button(Modify_Button_Frame,text='保存',width=8,height=1,command=Proxy_Manager_Window.destroy)
    save_button.grid(padx=5,pady=5,column=0,row=3,sticky=tk.W)

    
    cancle_button=tk.Button(Modify_Button_Frame,text='取消',width=8,height=1,command=Proxy_Manager_Window.destroy)
    cancle_button.grid(padx=5,pady=5,column=0,row=4,sticky=tk.W)
    pass





def Del_server():
    confirm=tkinter.messagebox.askyesno(title='警告!',message='你确定要移除所有存在的服务器么?')
    if confirm:
        try:
            GLOBAL_Configuration.remove_server_from_gui(1,1)
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

#延迟测试



def Delay_Test():
    global auto_proxy
    global GLOBAL_Configuration
    
    if auto_proxy == 1:
        #自动化延迟测试
        ServerList=GLOBAL_Configuration.get_server_list_from_config()
        Recording_Insertion('[+] 使用自动化延迟测试...\n','normal')
        Recording_Insertion('[!] 测试开始..请勿关闭窗口...\n','warning')
        for i in ServerList:
            Auto_Delay_obj=Delay_Test_Module(i[0],i[1])
            auto_delay=Auto_Delay_obj.UDP_AVG_RTT()
            if auto_delay == -1:
                Recording_Insertion('[!] '+i[0]+':'+str(i[1])+' 无响应\n','error')
            else:
                Recording_Insertion('[+] '+i[0]+':'+str(i[1])+' '+str(auto_delay)+'ms \n','success')
    else:
        Recording_Insertion('[+] 使用单节点延迟测试...\n','normal')
        Recording_Insertion('[%] 正在测试: '+Server_List_Select_combox.get()+'\n','blue')
        temp=Server_List_Select_combox.get()
        tem_server=temp.split(':')
        Delay_obj=Delay_Test_Module(tem_server[0],eval(tem_server[1]))
        udp_delay=Delay_obj.UDP_AVG_RTT()
        if udp_delay == -1:
            Recording_Insertion('[!] '+temp+' 无响应\n','error')
            pass
        Recording_Insertion(udp_delay,'success')
        Recording_Insertion('\n','success')
        
        #手动延迟测试
    #print('Delay_Test:',Server_List_Select_combox.get())
    #Recording_Insertion('Delay_Test:'+Server_List_Select_combox.get(),'blue')

Delay_Test_Button=tk.Button(Connection_Manager_Frame,text='延迟测试',font=ft,width=8,height=3,padx=4,pady=4,command=Delay_Test)
Delay_Test_Button.grid(column=1,row=0,rowspan=2)

#连接


def Connect():
    global CONNECT_STATUS
    print('Try Connect:',Server_List_Select_combox.get())
    Recording_Insertion('Try Connect:'+Server_List_Select_combox.get()+'\n','blue')
    CONNECT_STATUS = 1



Connection_Button=tk.Button(Connection_Manager_Frame,text='连接',font=ft,width=8,height=3,padx=4,pady=4,command=Connect)
Connection_Button.grid(column=2,row=0,rowspan=2)



#---------------Status---------------------#
status_ft=tkFont.Font(family='Airal',size=13,weight=tkFont.BOLD)

Connect_Status_Frame=tk.LabelFrame(MainWindow,text="连接状态",fg='blue',padx=5,pady=5)
Connect_Status_Frame.grid(padx=10,pady=3,columnspan=2,sticky='w')
Connect_Status_Lable=tk.Label(Connect_Status_Frame,text="当前服务器连接状态:",font=ft,padx=10,pady=8)
Connect_Status_Lable.grid(column=0,row=0)


Conn_status_var=tk.StringVar()
#Conn_status_var.set('    连接成功   ')
#Conn_status_var.set('   正在连接... ')
#Conn_status_var.set('    连接错误   ')

Conn_status_var.set('    未连接     ')
Conn_label=tk.Label(Connect_Status_Frame,textvariable=Conn_status_var,font=status_ft,fg='orange',padx=10)
Conn_label.grid(column=1,row=0,sticky='w')

def Conn_Status_Grid():
    global Conn_label
    global Connect_Status_Frame
    global status_ft
    global CONNECT_STATUS
    Conn_label.destroy()
    if CONNECT_STATUS == 0:
        Conn_status_var.set('    未连接     ')
        Conn_label=tk.Label(Connect_Status_Frame,textvariable=Conn_status_var,font=status_ft,fg='orange',padx=10)
        Conn_label.grid(column=1,row=0,sticky='w')
    elif CONNECT_STATUS == 1:
        Conn_status_var.set('    已连接     ')
        Conn_label=tk.Label(Connect_Status_Frame,textvariable=Conn_status_var,font=status_ft,fg='green',padx=10)
        Conn_label.grid(column=1,row=0,sticky='w')


    MainWindow.after(1000,Conn_Status_Grid)

#--------------日志-------------------#

record_frame=tk.LabelFrame(MainWindow,text="日志",fg='blue',padx=5,pady=5)
record_frame.grid(column=0,padx=10,pady=3,columnspan=2,sticky='w')
#record_Lable=tk.Label(record_frame,text="当前服务器连接状态:",font=ft,padx=10,pady=8)
#record_Lable.grid(column=0,row=0)
#Recording_Var=tk.StringVar()
#Recording_String='sssssssssssssssssssssssss'
#Recording_Var.set(Recording_String)
record_Text=tk.Text(record_frame,width=48,height=12)

record_Text.tag_config('error',foreground='red')
record_Text.tag_config('warning',foreground='orange')
record_Text.tag_config('success',foreground='green')
record_Text.tag_config('normal',foreground='black')
record_Text.tag_config('blue',foreground='blue')
record_Text.grid(sticky='w')




#record_Text.insert(tk.END,'test','green')

#record_Text.configure(state='disabled')

def Recording_Insertion(text,_type):
    global record_Text
    record_Text.configure(state=tk.NORMAL)
    record_Text.insert(tk.END,text,_type)
    #record_Text.insert(tk.END,'\n',_type)
    record_Text.configure(state='disabled')
    

scroll=tk.Scrollbar(record_frame)
scroll['command']=record_Text.yview
scroll.grid(column=1,row=0,sticky=tk.S + tk.W + tk.E + tk.N)

#def Recording_Module(text,color):



MainWindow.after(1000,Server_Chosen_Cobox)
MainWindow.after(1000,Conn_Status_Grid)

MainWindow.mainloop()

'''
要解决的问题：
json写入，修改，自动化udp选路模块
'''

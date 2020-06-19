#import tkinter as tk
#from tkinter import ttk
#from tkinter import scrolledtext
#
import tkinter as tk
root=tk.Tk()
t=tk.Text(root)
# 创建一个TAG，其前景色为红色
t.tag_config('a',foreground='red')
# 使用TAG 'a'来指定文本属性
t.insert(1.0,'0123456789','a')
t.pack()
root.mainloop()

'''
window=tk.Tk()
window.title('a  window')
window.geometry('730x300')
'''
'''
def do_menu():
    print('selected a menu')

menubar=tk.Menu(window)

#level 1
filemenu=tk.Menu(menubar,tearoff=0)
edit=tk.Menu(menubar,tearoff=0)

#level 1 add
menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Edit', menu=edit)

#level 2 

filemenu.add_command(label='Open',command=do_menu)
filemenu.add_command(label='Find',command=do_menu)
edit.add_command(label='refresh',command=do_menu)
edit.add_command(label='help',command=do_menu)

submenu_file=tk.Menu(filemenu)
submenu_edit=tk.Menu(edit)
filemenu.add_cascade(label='Import', menu=submenu_file, underline=0)
edit.add_cascade(label='editsub', menu=submenu_edit, underline=0)
submenu_file.add_command(label='Sub1',command=do_menu)
#filemenu.add_cascade(label='subfile',menu=submenu_file)
#edit.add_cascade(label='subedit',menu=edit)

window.config(menu=menubar)
'''


'''
#tab1 write------------------
labelframe=ttk.LabelFrame(tab1,text='tab1')
labelframe.grid(column=0, row=0, padx=8, pady=4)
a_label = ttk.Label(labelframe, text=' Enter a number: ')
a_label.grid(column=0, row=0, sticky='W')
def click_me():
	action.configure(text='Hello ' + name.get() + ' ' + number_chosen.get())

# Adding a Textbox Entry widget
name = tk.StringVar()
name_entered = ttk.Entry(labelframe, width=12, textvariable=name)
name_entered.grid(column=0, row=1, sticky='W') # column 0

# Adding a Button
action = ttk.Button(labelframe, text="Click Me!", command=click_me)   
action.grid(column=2, row=1, sticky='W') # change column to 2

ttk.Label(labelframe, text='Choose a number:').grid(column=1, row=0, sticky='W')

number = tk.StringVar()
number_chosen = ttk.Combobox(labelframe, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=1, sticky='W') # Combobox in column 1
number_chosen.current(4)

# Using a scrlled text control
scrol_w = 30
scrol_h = 3
scr = scrolledtext.ScrolledText(labelframe, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scr.grid(column=0, sticky='WE', columnspan=3)
'''
#--------tab creat
'''
tabcontrol=ttk.Notebook(window)
tab1=ttk.Frame(tabcontrol)
tabcontrol.add(tab1,text='tab1')
tab2=ttk.Frame(tabcontrol)
tabcontrol.add(tab2,text='tab2')
tabcontrol.pack(expand=1,fill='both')

tab_label_A=ttk.LabelFrame(tab1,text='Primary Setting')
tab_label_A.grid(column=0, row=0, padx=8, pady=4)
a_label = ttk.Label(tab_label_A,text='hub')
a_label.grid(column=0,row=0,sticky='w')

#输入框
remote_server=tk.StringVar()
remote_server_input=ttk.Entry(tab_label_A,width=20,textvariable=remote_server)
remote_server_input.grid(column=0,row=1,sticky='w')

#按钮
SERVER_LIST=[]
FLUSH_FLAG=False

def Add_Server_into_List():
    SERVER_LIST.append(remote_server_input.get())


def UDP_Connection_Test():
    pass
Add_Server_into_List_Button=ttk.Button(tab_label_A,text="添加到服务器列表",command=Add_Server_into_List)
Add_Server_into_List_Button.grid(column=1,row=1,sticky='w')


'''
'''
but=tk.Button(window,text='延迟测试',command=pushd)
but.pack()
'''
'''
window.mainloop()
'''
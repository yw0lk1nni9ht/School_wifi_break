# -*- coding: UTF-8 -*-
import psutil
import os
import traceback
import time
from Tkinter import *           # 导入 Tkinter 库
import datetime
import win32api,win32con
import multiprocessing
import pyaudio  
import wave  
import threading
import ctypes
import inspect
import requests

global save
global li
global ga

def changemac():
    user = {'user':'20140390223','pass':'123'}
    r = requests.session()
    a = r.post('http://10.10.0.20/login.php',data = user)
    a = r.get('http://10.10.0.20/private.php')
    a = r.get('http://10.10.0.20/changeMACForm.php')
    a = r.get('http://10.10.0.20/changeMAC.php')
    if 'Unbind success' in a.text:
        win32api.MessageBox(0,u'解绑成功', u'提示框',win32con.MB_OK)

def play():
    #define stream chunk
    chunk = 1024

    #open a wav format music
    f = wave.open(r"C:\Users\Administrator\Desktop\school\4123.wav","rb")
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
				channels = f.getnchannels(),
				rate = f.getframerate(),
				output = True)
    #read data
    data = f.readframes(chunk)
    #paly stream
    while data != '':
       stream.write(data)
       data = f.readframes(chunk)
       #stop stream
    stream.stop_stream()
    stream.close()
    p.terminate()


   
def a():
    old = datetime.datetime.now()
    while ga :
        #os.system('cls')
        now = datetime.datetime.now()
        #print now - old
        text1.delete(0.0, END)
        text1.insert(INSERT, now-old )
        time.sleep(1)
        if str(now-old) > '0:18:00.000000':
            play()
            win32api.MessageBox(0,u'到点了', u'提示框',win32con.MB_OK)
            break
   

def Bsuspend():
    try:
        os.system('pssuspend64.exe '+str(save))
        li[1] = (time.strftime('%H:%M:%S',time.localtime(time.time()))+':进程状态：挂起')
        listb.delete(0,0)
        listb.insert(0,li[1])
        ga= 1
        t1 = threading.Thread(target=a)
        t1.start()
        #a()
    except:
        pass

          
def Bresume():
    try:
        os.system('pssuspend64.exe -r '+str(save))
        li[1] = (time.strftime('%H:%M:%S',time.localtime(time.time()))+':进程状态：运行')
        listb.delete(0,0)
        listb.insert(0,li[1])
        ga = 0
        text1.delete(0.0, END)
        del t1
        #text1.delete(0.0, END)
    except: 
        pass

ga = 1
root = Tk()                     # 创建窗口对象的背景色                            # 创建两个列表
root.title("挂起天翼")
root.iconbitmap('F:\\456.ico')
li     = ['1','2']
listb  = Listbox(root)          #  创建个列表组件
text1 = Text(root,width=18,height=2)
t1 = threading.Thread(target=a)

for id in psutil.pids():
    try:
        p = psutil.Process(id)
        if p.name() == 'ESurfingSvr.exe':
            li[0] = ('pid为：' + str(id))
            save = id
            break
    except:
        pass

B1 = Button(root, text ="挂起", command = Bsuspend)
#root.bind('<Double-Button-1>',work)
B2 = Button(root, text ="恢复", command = Bresume)
B3 = Button(root, text ="解绑", command = changemac)

for item in li:                 # 第一个小部件插入数据
    listb.insert(0,item)


listb.pack()                    # 将小部件放置到主窗口中 
text1.pack()
B1.pack()
B2.pack()
B3.pack()
root.mainloop()                 # 进入消息循环


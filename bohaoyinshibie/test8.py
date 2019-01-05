#创建GUI界面：Tkinter
import tkinter as tk
app=tk.Tk()             #生产根窗口
app.title("拨号音识别")   #窗口名称
theLabel=tk.Label(app,text="我的第一个窗口程序")   #显示在窗口上的文字
theLabel.pack() #自动调节GUI界面的尺寸

app.mainloop()   #建立主界面
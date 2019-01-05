import tkinter as tk
class APP:
    def __init__(self,master):
        frame=tk.Frame(master)
        frame.pack()

        self.hi_there=tk.Button(frame,text="打招呼",fg="blue",command=self.say_hi)
        self.hi_there.pack()

    def say_hi(self):
        print("大家好")
root=tk.Tk()
app=APP(root)

root.mainloop()
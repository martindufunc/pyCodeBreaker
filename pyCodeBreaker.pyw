#!/usr/bin/env python3

"""
-------------------------------
pyCodeBreaker v1.0, Jan2020
joselito.rapisora@gmail.com
-------------------------------
"""

import random
from tkinter import *

codeSelect = ("A", "B", "C", "D", "E", "F")


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()


    def init_window(self):
        self.master.title("pyCodeBreaker")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="New Code", command=self.new_code)
        file.add_command(label="Help", command=self.help_window)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        self.grid(row=0,column=0,padx=5,pady=5)

        Window.hiddenCode = [0 for x in range(4)]
        Window.hiddenCodebtn = [0 for x in range(4)]
        Window.code=[[0 for x in range(10)] for x in range(4)]
        Window.btn=[[0 for x in range(10)] for x in range(4)]
        Window.result=[[0 for x in range(10)] for x in range(2)]
        Window.evalbtn=[0 for x in range(10)]
        Window.trashTalker=[None]

        
        for x in range(4):
            self.hiddenCodebtn[x] = Button(self, height = 1, width = 3, text="--", bg="white")
            self.hiddenCodebtn[x].grid(column=x, row=11)
            self.hiddenCode[x] = random.randint(0,5)  #generates the secret code here.

        # For debugging, prints out the secret code...
        #for x in range(4):
        #    print(codeSelect[self.hiddenCode[x]], end=' ')
        #print()

        for x in range(4):
            for y in range(10):
                self.btn[x][y] = Button(self,command= lambda x1=x, y1=y: self.code_change(x1,y1), height = 1, width = 3, text="--", state="disabled")
                self.btn[x][y].grid(column=x, row=y)
                self.code[x][y] = 5 + 1
        for x in range(4):
            self.btn[x][0].config(state="active")

        for y in range(10):
            self.evalbtn[y] = Button(self, command= lambda y1=y: self.code_eval(y1), height = 1, width = 8, text="Evaluate", state="disabled")
            self.evalbtn[y].grid(column=4, row=y)
        self.evalbtn[0].config(state="active")

        for x in range(2):
            for y in range(10):
                self.result[x][y] = Label(self, height = 1, width = 3, text="  0  ", bg="white")
                self.result[x][y].grid(column=5+x, row=y)

        msg = (\
        "Show me your code breaking skills.",\
        "Do you accept the challenge?",\
        "You have 10 attempts to break the code.")
        self.trashTalker[0] = Label(self, height = 3, text=msg[random.randint(0,2)])
        self.trashTalker[0].grid(columnspan=10, row=12)


    def help_window(self):
        t = Toplevel(self)
        t.wm_title("Help")
        txt = "\npyCodeBreaker v1.0\nBased on the popular game Codebreaker/ Mastermind\n(c) Jan 2020, joselito.rapisora@gmail.com\nFeedback and bug reports are very much appreciated!\n"
        message = Message(t, text = txt)
        message.config(font=('Ariel', 12, 'italic'), width = 800)
        message.pack()                                
        image = PhotoImage(file="help.png")
        label = Label(t,image=image)
        label.image = image
        label.pack()      
        

    def code_change(self,x,y):  #cycles input code here
        if (self.code[x][y] + 1 > 5):
            self.code[x][y] = 0
        else:
            self.code[x][y] += 1
        self.btn[x][y].config(text=codeSelect[self.code[x][y]])


    def code_eval(self,y):
        res0 = 0
        res1 = 0
        valid = True
        tempHdnCode = [0 for x in range(4)]
        tempCode = [0 for x in range(4)]
        tempHdnCode = self.hiddenCode.copy()
        tempCode = self.code.copy()
        
        for x1 in range(4):
            if(tempCode[x1][y] > 5 ):
                valid = False
                break

        if(valid == True):
            #Comparison algorithm
            for x1 in range(4):  #checks for same code on same location
                if(tempCode[x1][y] == tempHdnCode[x1]):
                    tempCode[x1][y] = None
                    tempHdnCode[x1] = None
                    res1 += 1
            for x1 in range(4):  #checks for remaining same code that are not on same location
                for x2 in range(4):
                    if(tempCode[x1][y] != None and tempCode[x1][y] == tempHdnCode[x2]):
                        tempCode[x1][y] = None
                        tempHdnCode[x2] = None
                        res0 += 1
            self.result[0][y].config(text= "  "+str(res0)+"  ")
            self.result[1][y].config(text= "  "+str(res1)+"  ")

            #status logic here...     
            if(res1 == 4):
                self.evalbtn[y].config(state="disabled")
                for x in range(4):
                    self.btn[x][y].config(state="disabled", bg="white")
                Window.show_result(self, 1)
            elif(y+1 < 10):
                self.evalbtn[y+1].config(state="active")
                self.evalbtn[y].config(state="disabled")
                for x in range(4):
                    self.btn[x][y+1].config(state="active")
                    self.btn[x][y].config(state="disabled", bg="white")
            else:
                self.evalbtn[y].config(state="disabled")
                for x in range(4):
                    self.btn[x][y].config(state="disabled", bg="white")
                Window.show_result(self, 0)


    def show_result(self, pf):  #reveal code and remarks here
        if(pf == 1):
            bgcolor = "green"
            msg = (\
            "Code Broken. Well Done.",\
            "You should consider full time code breaking",\
            "You should try again to rule-out luck.")
        else:
            bgcolor = "red"
            msg = (\
            "You have failed. Now back to work!",\
            "You should refine your algorithm.",\
            "Try again?")
        self.trashTalker[0]['text']=msg[random.randint(0,2)]
        for x in range(4):
            self.hiddenCodebtn[x].config(text=codeSelect[self.hiddenCode[x]], bg=bgcolor)


    def new_code(self):
        self.trashTalker[0]['text']=""
        Window.init_window(self)


    def client_exit(self):
        exit()


    def key(event):
        kp = event.char
        #print ("pressed", kp)  #for debugging purposes
        if(kp == 'q'): #q
            x = 0
        elif(kp == 'w'): #w
            x = 1
        elif(kp == 'e'): #e
            x = 2
        elif(kp == 'r'): #r
            x = 3
        else:
            x = None
        if (x != None):
            for y in range(10):
                if(Window.evalbtn[y]['state'] == "active"):
                    Window.code_change(Window,x,y)
                    break
        if(kp == ' '): #space
            for y in range(10):
                if(Window.evalbtn[y]['state'] == "active"):
                    Window.code_eval(Window,y)
                    break                    


if __name__ == '__main__':
    root = Tk()
    root.geometry("255x350")
    root.resizable(False, False)
    app = Window(root)
    root.bind("<Key>", Window.key)
    root.mainloop()



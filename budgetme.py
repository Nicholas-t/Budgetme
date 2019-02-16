# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:54:33 2019

@author: yollp
"""

import tkinter as tk
from tkinter import Frame, END, OptionMenu, Button, messagebox, PhotoImage, Label, Entry, Listbox, Scrollbar, StringVar
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy import core
from decimal import Decimal

import os
import sys

DATA = {} #DATA = {date : [[title1, amount1],[title2, amount2]]}

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

def getdate():
    now = datetime.datetime.now()
    return str(now.day)+"."+str(now.month)+"."+str(now.year)


class expense:
    now = datetime.datetime.now()
    def __init__(self, title, amount, date=getdate()):
        self.title = title
        self.amount = amount
        self.date = date
        
    def add(self):
        out = [self.title, self.amount]
        if self.date in DATA.keys():
            if DATA[self.date] == [['0','0']]:
                DATA[self.date] = [out]
            else:
                DATA[self.date].append(out)
        else:
            DATA[self.date] = [out]
            
            
#------------------------- Objects done

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs, bg="white")
        
    def show(self):
        self.lift()
        
class bg_page(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        photo = PhotoImage(file=resource_path("white.gif"))
        photolab = Label(self,image=photo)
        photolab.image = photo
        photolab.grid(row=0 ,column=2,columnspan=2, rowspan=4, sticky = 'nwes')
        
class main_page(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       photo = PhotoImage(file=resource_path("home.gif"))
       photolab = Label(self,image=photo)
       photolab.image = photo
       photolab.grid(row=0 ,column=2,columnspan=2, sticky = 'nwes')
       self.listNodes = Listbox(self, width=35, height=15, font=("Courier", 10))
       self.listNodes.grid(row=1, column=1, columnspan=4, rowspan=2)
       scrollbar = Scrollbar(self, orient="vertical")
       scrollbar.config(command=self.listNodes.yview)
       scrollbar.grid(row=1, column=4, rowspan=2, sticky='ns')
       self.listNodes.config(yscrollcommand=scrollbar.set)
       self.lis = [k for k in DATA.keys()]
       self.variable = StringVar(self)
       self.variable.set(self.lis[0])
       self.variable2 = StringVar(self)
       self.variable2.set(self.lis[-1])
       self.opt1 = OptionMenu(self,self.variable, *self.lis)
       self.opt2 = OptionMenu(self,self.variable2, *self.lis)
       l1 = Label(self, text="From :", font=("Courier", 12))
       l2 = Label(self, text="To :", font=("Courier", 12))
       l1.grid(row=4, column=2)
       self.opt1.grid(row=4, column=3)
       l2.grid(row=5, column=2)
       self.opt2.grid(row=5, column=3)
       refb= Button(self, text="Refresh!", font =("Courier", 12), command=self.refresh)
       refb.grid(row=5, column=4)
       

   def refresh(self): 
        self.listNodes.delete(0,END)
        tot = 0
        day = 0
        self.lis = [k for k in DATA.keys()]
        self.opt2 = OptionMenu(self,self.variable2, *self.lis)
        global cur
        global target
        self.date1=self.variable.get()
        self.date2=self.variable2.get()
        self.lis = [k for k in DATA.keys()]
        if self.date1 == self.date2:
            self.listNodes.insert(END, self.date1+"  :")
            for eac in DATA[self.date1]:
                    if eac != ['0','0']:
                        out=""
                        out+=eac[0]
                        while len(out) != 18:
                            out += "."
                        out +=str(eac[1])+" {}".format(cur)
                        tot +=float (eac[1])
                        self.listNodes.insert(END, out)
        elif self.date2 not in self.lis[self.lis.index(self.date1):]:
            messagebox.showerror("Warning", "Your date is invalid!")
        else:
            l = self.lis[self.lis.index(self.date1):(self.lis.index(self.date2)+1)]
            for each in l:
                self.listNodes.insert(END, each+"  :")
                day += 1
                for eac in DATA[each]:
                    out=""
                    out+=eac[0]
                    while len(out) != 14:
                        out += "."
                    out +=str(eac[1])+" {}".format(cur)
                    tot +=float (eac[1])
                    self.listNodes.insert(END, out)
        self.listNodes.insert(END, "-------------------- +")
        tot = Decimal(float(tot))
        tot = round(tot,2)
        self.listNodes.insert(END, "Total   : {} {}".format(str(tot), cur))
        if day == 0:
            day = 1
        avg = Decimal(float(tot/day))
        avg = round(avg, 2)
        self.listNodes.insert(END, "Average : {} {}/day".format(str(avg), cur))
        self.listNodes.insert(END, "Target : {} {}/day".format(str(target), cur))
        surplus = float(target) - float(avg)
        if surplus < 0 :
            self.listNodes.insert(END, "You are spending more than your")
            self.listNodes.insert(END, "budget by : {} {}/day".format(str(surplus), cur))
        elif surplus == 0:
            self.listNodes.insert(END, "Be careful !")
            self.listNodes.insert(END, "You are in the border line of your budget")
        elif surplus > 0 :
            self.listNodes.insert(END, "Keep it up! You have an average")
            self.listNodes.insert(END, "surplus of : {} {}/day".format(str(surplus), cur))
        
        
    
       
                
       
   

class graph_page(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       photo = PhotoImage(file=resource_path("graph.gif"))
       photolab = Label(self,image=photo)
       photolab.image = photo
       photolab.grid(row=0 ,column=1, sticky = 'nwes')
       
       self.lis = [k for k in DATA.keys()]
       self.variable = StringVar(self)
       self.variable.set(self.lis[0])
       self.variable2 = StringVar(self)
       self.variable2.set(self.lis[-1])
       self.opt1 = OptionMenu(self,self.variable, *self.lis)
       self.opt2 = OptionMenu(self,self.variable2, *self.lis)
       l1 = Label(self, text="From :", font=("Courier", 12))
       l2 = Label(self, text="To :", font=("Courier", 12))
       l1.grid(row=3, column=0)
       self.opt1.grid(row=3, column=1)
       l2.grid(row=4, column=0)
       self.opt2.grid(row=4, column=1)
       refb= Button(self, text="Refresh!", font =("Courier", 12), command=self.refresh)
       refb.grid(row=5, column=1)
       
       self.fig = Figure(figsize=(3,2))
       self.a = self.fig.add_subplot(111)
       self.a.plot([],[], color = "green")
       self.a.set_title("Visualise your expenses !", fontsize=10)
       self.a.set_ylabel("Amount")
       self.a.set_xlabel("Day")
       
       self.canvas = FigureCanvasTkAgg(self.fig, master=self)
       self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=2, columnspan=2)
       self.canvas.draw()
       
   def refresh(self):
        global cur
        global target
        self.date1=self.variable.get()
        self.date2=self.variable2.get()
        self.lis = [k for k in DATA.keys()]
        if self.date1 == self.date2:
            messagebox.showerror("Warning", "Interval is invalid!")
        elif self.date2 not in self.lis[self.lis.index(self.date1):]:
            messagebox.showerror("Warning", "Your date is invalid!")
        else:
            self.lis = self.lis[self.lis.index(self.date1):(self.lis.index(self.date2)+1)]
            x= np.arange(len(self.lis))
            y= np.array([])
            for date in self.lis:
                tot = 0
                for expen in DATA[date]:
                    tot+=float(expen[1])
                y = np.append(y, [tot])
            self.a.clear()
            self.a.plot(x, y, color="green", marker="o")
            self.a.set_title("Expnses from {} to {}".format(self.date1, self.date2), fontsize=10)
            self.a.set_ylabel("Amount")
            self.a.set_xlabel("Day")
            
            t = [float(target) for _ in range (len(self.lis))]
            self.a.plot(x, t, color ="blue")
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=2, columnspan=2)
            self.canvas.draw()
       

class setting_page(Page):
   def __init__(self, *args, **kwargs):
       
       Page.__init__(self, *args, **kwargs)
       photo = PhotoImage(file=resource_path("setting.gif"))
       photolab = Label(self,image=photo)
       photolab.image = photo
       photolab.grid(row=0 ,column=0,columnspan=2, sticky = 'nwes')
       self.t_ent = Entry(self)
       self.t_lab = Label(self, text="Change target :", font = ("Courier", 15))
       self.t_but = Button(self, text="Change!", command = self.reset_target, font = ("Courier", 15))
       global cur
       global target
       self.lab = Label(self, text="Current Target : {} {} / day".format(str(target), cur), font = ("Courier", 15))
       self.lab.grid(row=1, column = 0, columnspan = 2)
       self.t_lab.grid(row = 2, column = 0)
       self.t_ent.grid(row = 2, column = 1)
       self.t_but.grid(row = 3, column = 1)
       
       self.c_ent = Entry(self)
       self.c_lab = Label(self, text="Change currency :", font = ("Courier", 15))
       self.c_but = Button(self, text="Change!", command = self.reset_cur, font = ("Courier", 15))
       self.c_lab.grid(row = 4, column = 0)
       self.c_ent.grid(row = 4, column = 1)
       self.c_but.grid(row = 9, column = 1)
       
       lab = Label(self, text="To help with conversion please specify \nthe conversion rate.", font = ("Courier", 15))
       self.ent_cur = Entry(self, font = ("Courier", 15))
       lab_cur = Label(self, text="{}".format(cur), font = ("Courier", 15))
       self.ent_feat_cur = Entry(self, font = ("Courier", 15))
       lab_trans = Label(self, text="<=====>", font = ("Courier", 15))
       lab_feat_cur = Label(self, text=" X (future currency)")
       lab.grid(row = 5, column = 0, columnspan=2)
       self.ent_cur.grid(row = 6, column = 0)
       lab_cur.grid(row = 6, column = 1)
       self.ent_feat_cur.grid(row = 8, column = 0)
       lab_trans.grid(row = 7, column = 1)
       lab_feat_cur.grid(row = 8, column = 1)
       
       
              
   def reset_target(self):
       global target
       global cur
       value = self.t_ent.get()
       target = value
       if value != "":
           self.lab = Label(self, text="Current Target : {} {} / day".format(str(target), cur), font = ("Courier", 15))
           self.lab.grid(row=1, column = 0, columnspan = 2)
           file = open("history.csv", 'w+')
           file.write("{}, {}\n".format(target, cur))
           for (k,v) in DATA.items():
               for each in v :
                   file.write("{}, {}, {}\n".format(k, each[0], each[1]))
           file.close()
           self.t_ent.delete(0, 'end')
           global main
           main.p1.refresh()
           main.p2.refresh()
       else:
           messagebox.showerror("Error", "Make sure all the required fields are not empty")
       
   def reset_cur(self):
       global target
       global cur

       value = self.c_ent.get()
       cur = value
       if value != "" and self.ent_cur.get() != "" and self.ent_feat_cur.get()!= "" and self.ent_cur.get() != "0" and self.ent_feat_cur.get()!= "0":
           try:
               rat = Decimal(float(self.ent_feat_cur.get())/float(self.ent_cur.get()))
               print(DATA)
               for k in DATA.keys():
                   out = []
                   for each in DATA[k]:
                       n = Decimal(float(float(each[1])*float(rat)))
                       n = round(n,2)
                       out+=[[each[0], str(n)]]
                   DATA[k]=out

               target = Decimal(float(target)*float(rat))
               target = round(target, 2)
               print(DATA, target, cur)
               self.lab = Label(self, text="Current Target : {} {} / day".format(str(target), cur), font = ("Courier", 15))
               self.lab.grid(row=1, column = 0, columnspan = 2)
               file = open("history.csv", 'w+')
               file.write("{}, {}\n".format(target, cur))
               for (k,v) in DATA.items():
                   for each in v :
                       file.write("{}, {}, {}\n".format(k, each[0], each[1]))
               file.close()
               self.c_ent.delete(0, 'end')
               self.ent_cur.delete(0, 'end')
               self.ent_feat_cur.delete(0, 'end')
               global main
               main.p1.refresh()
               main.p2.refresh()
           except ValueError:
               messagebox.showerror("Error", "Make sure your conversion amount is a number")
       else:
           messagebox.showerror("Error", "Make sure all the required fields are not empty and/or not 0")
               
       
class add_page(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       photo = PhotoImage(file=resource_path("add.gif"))
       photolab = Label(self,image=photo)
       photolab.image = photo
       photolab.grid(row=0 ,column=2,columnspan=2, sticky = 'nwes')
       Date = Label(self, text="Date : {}".format(getdate()))
       Date.config(font=("Courier", 20))
       Date.grid(row=1 ,column=2,columnspan=2, sticky = 'nwes')
       self.reason_label = Label(self, text="Reason :")
       self.reason_label.config(font=("Courier", 20))
       self.reason_label.grid(row=2 ,column=2, sticky = 'nwes')
       self.am_label = Label(self, text="Amount :")
       self.am_label.config(font=("Courier", 20))
       self.am_label.grid(row=3 ,column=2, sticky = 'nwes')
       self.reason_entry = Entry(self, font="Courier 20 bold")
       self.reason_entry.grid(row=2, column = 3)
       self.am_entry = Entry(self, font="Courier 20 bold")
       self.am_entry.grid(row=3, column = 3)
       self.okb = Button(self, text="Save",font = ("Courier", 20), command = self.save)
       self.okb.grid(row=4, column=3)
       
   def save(self):
       conf = messagebox.askquestion("Save", "Are you sure you want to save?", icon="warning")
       hist = open("history.csv", "a+")
       if conf == 'yes':
           if self.reason_entry.get() != "" and self.am_entry.get() != "": 
               try:
                   reason = self.reason_entry.get()
                   am = float(self.am_entry.get())
                   exp = expense(reason, am)
                   exp.add()
                   hist.write(getdate()+", "+reason+", "+str(am)+"\n")
                   
               except ValueError:
                   messagebox.showerror("Error", "Make sure your amount is a number")
           else:
                messagebox.showerror("Error", "Don't leave any space empty")
       else:
           messagebox.showerror("not saved", "Your consumption has not been saved")
       self.reason_entry.delete(0,'end')
       self.am_entry.delete(0,'end')
       hist.close()
       global main
       main.p1.refresh()
       main.p2.refresh()


       
       
       

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        if DATA == {}:
            DATA[getdate()] = [['0','0']]
        self.p1 = main_page(self)
        self.p2 = graph_page(self)
        p3 = setting_page(self)
        p4 = add_page(self)
        bg = bg_page(self)
        

        buttonframe = Frame(self, highlightbackground="green", highlightcolor="green", highlightthickness=1, bg="white")
        container = Frame(self, highlightbackground="green", highlightcolor="green", highlightthickness=1, bg="white")
        buttonframe.grid(row=0 ,column=0, rowspan = 5, sticky='nwes')
        container.grid(row=0 ,column=1, rowspan = 5, columnspan=2, sticky = 'nwes')
        
        self.p1.grid(row=0,column=1,in_=container)
        self.p2.grid(row=0,column=1,in_=container)
        p3.grid(row=0,column=1,in_=container)
        p4.grid(row=0,column=1,in_=container)
        bg.grid(row=0,column=1,in_=container)

        def combine_funcs(*funcs):
            def combined_func(*args, **kwargs):
                for f in funcs:
                    f(*args, **kwargs)
            return combined_func
        bg.lift()
        b1 = Button(buttonframe, text="Main Page", command= combine_funcs(bg.lift, self.p1.lift))
        b2 = Button(buttonframe, text="Graph Page", command=combine_funcs(bg.lift, self.p2.lift))
        b3 = Button(buttonframe, text="Setting Page", command=combine_funcs(bg.lift, p3.lift))
        b4 = Button(buttonframe, text="Add Page", command=combine_funcs(bg.lift, p4.lift))
        
        
        global target
        global cur
        t = Label(buttonframe , text="\"Putting a limit\n for the future\" -  some guy")
        t.config(font=("Courier", 15))
        t.grid(row=0 ,column=0, sticky = 'nwes')
        b1.config(font=("Courier", 15))
        b2.config(font=("Courier", 15))
        b3.config(font=("Courier", 15))
        b4.config(font=("Courier", 15))
        b1.grid(row=1 ,column=0, sticky = 'nwes', padx=10, pady=50)
        b2.grid(row=2 ,column=0, sticky = 'nwes', padx=10, pady=50)
        b3.grid(row=3 ,column=0, sticky = 'nwes', padx=10, pady=50)
        b4.grid(row=4 ,column=0, sticky = 'nwes', padx=10, pady=50)
        
        self.p1.show()

def get_next_day(origin):
    l = origin.split('.')
    date = int(l[0])
    month = int(l[1])
    year = int(l[2])
    month_a = [1,3,5,7,8,10,12] #month with 31
    month_b = [2,4,6,9,11]
    if month == 12 and date == 31:
        return "1.1.{}".format(str(year+1))
    elif month in month_a:
        if date == 31:
            return "{}.{}.{}".format(str(1),str(month+1),str(year))
        else:
            return "{}.{}.{}".format(str(date+1),str(month),str(year))
    elif month in month_b:
        if date == 30:
            return "{}.{}.{}".format(str(1),str(month+1),str(year))
        else:
            return "{}.{}.{}".format(str(date+1),str(month),str(year))
    

if __name__ == "__main__":
    if not (os.path.isfile('./history.csv')):
        init = tk.Tk()
        label = Label(init,text = "Let's get you started by setting a budget plan!")
        l1 = Label (init,text = "Daily target : ")
        l2 = Label (init,text = "Currency : ")
        e1 = Entry (init)
        e2 = Entry (init)
        label.grid(row = 1, column = 1, columnspan = 2,sticky ='nwes')
        l1.grid(row = 2, column = 1,sticky = 'nwes')
        l2.grid(row = 3, column = 1,sticky = 'nwes')
        e1.grid(row = 2, column = 2,sticky = 'nwes')
        e2.grid(row = 3, column = 2,sticky = 'nwes')
        photo = PhotoImage(file=resource_path("empty.gif"))
        photolab = Label(init,image=photo)
        photolab.image = photo
        photolab.grid(row=5 ,column=1, columnspan = 2, sticky = 'nwes')
        
        def end():
            try:
                global target
                global cur
                target = float(e1.get())
                cur = e2.get()
                init.destroy()
            except ValueError:
                messagebox.showerror("Error", "Make sure your target is an integer, and your currency is valid")
    
        b1 = Button (init, text = "I'm Ready !", command=end)
        b1.grid(row = 4, column = 1,columnspan=2, sticky='nwes')
        init.mainloop()
        hist = open("history.csv", "w+")
        hist.write(str(target)+", "+cur+"\n")
        hist.write(getdate()+", "+str(0)+", "+str(0)+"\n")
        hist.close()
        
    else :
        hist = open("history.csv", "r+")
        lines = hist.readlines()
        lines = [l.strip('\n') for l in lines]
        lines = [l.split(', ') for l in lines ]
        target = float(lines[0][0])
        cur = lines[0][1]
        if len(lines)!=1:
            for i in range (1, len(lines)):
                exp = expense(lines[i][1], lines[i][2], lines[i][0])
                exp.add()
        hist.close()
        
    #-------- initialised
    root = tk.Tk()
    main = MainView(root)
    main.grid()
    root.wm_geometry("852x660")
    root.mainloop()
        

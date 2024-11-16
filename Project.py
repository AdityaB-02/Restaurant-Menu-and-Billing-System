import tkinter as tk, tkinter.messagebox as msg
from tkinter import ttk
import mysql.connector as sql, time as xtime

#SQL CONNECTIVITY#
import mysql.connector as sql
mycon=sql.connect(host='localhost',user='root',passwd="aditya",database='ab02')#change
cursor=mycon.cursor()
cursor.execute('select *from menu2;')
menu=cursor.fetchall()

# comment
self=tk.Tk()
self.title('XX RESTAURANT')
self.config(bg='white')

code,ordr=[],[]
d={}
for i in menu:
        d[i[0]]=(i[1],i[2],i[3])
        code.append(str(i[0]))
rows=len(menu)
a=0
b_menu=rows

#-------------FRAME----------------#
frame=tk.Frame(self,bd=5,relief='ridge')
frame.pack(side=tk.TOP)
for i in ['Item Code','Item Name','Price','Time( in min)','Type']:
    e=tk.Entry(frame,width=14,font=('Arial',11,'bold'))
    e.grid(row=0,column=a)
    e.insert(tk.END,i)
    a+=1

if rows>17:
    b_menu=18
    a=7
    for i in ['Item Code','Item Name','Price','Time( in min)','Type']:
        e=tk.Entry(frame,width=14,font=('Arial',11,'bold'))
        e.grid(row=0,column=a)
        e.insert(tk.END,i)
        a+=1
    
def exist():
        cursor.execute('show tables')
        if ('customer_details',) in cursor.fetchall():
                return True
        else:
                return False


def Filter():
    a=0
    for w in frame.winfo_children():
        w.destroy()
    for i in ['Item Code','Item Name','Price','Time( in min)','Type']:
        e=tk.Entry(frame,width=14,font=('Arial',11,'bold'))
        e.grid(row=0,column=a)
        e.insert(tk.END,i)
        a+=1
    if ty.get()!='all':
        x,y=0,0
        for i in range(rows):
            if menu[i][4]==ty.get():
                x+=1
                y=0
                for j in range(5):#columns
                    e=tk.Entry(frame,width=14,font=('Arial',11))
                    e.grid(row=x,column=y)
                    e.insert(tk.END,menu[i][j])
                    y+=1
    else:
        for i in range(b_menu):
                for j in range(5):#columns
                        e=tk.Entry(frame,width=14,font=('Arial',11))
                        e.grid(row=i+1,column=j)
                        e.insert(tk.END,menu[i][j])
        ur=0
        if rows>17:
            for i in range(18,rows):
                for j in range(5):
                    e=tk.Entry(frame,width=14,font=('Arial',11))
                    e.grid(row=ur+1,column=j+6)
                    e.insert(tk.END,menu[i][j])
                ur+=1
            

#-------------TOP here----------------
def order():
    global top, oe, o, disp, total, time, v, c_name, p_n
    top=tk.Toplevel()
    top.geometry('400x450')
    top.title('ORDER')
    top.config(bg='lightgreen')
    top.attributes('-topmost',True)
    top.resizable(width=False, height=False)

    total,time=0,0
    v=[]

    fr=tk.Frame(top,relief='raised')
    fr.pack(side=tk.TOP)
    nm=tk.Label(fr,text='*Name: ')
    nm.grid(column=0,row=0)
    c_name=tk.Entry(fr,width=25)
    c_name.grid(column=1,row=0)
    ph=tk.Label(fr,text='*Phone No.(10-digit): ')
    ph.grid(column=0,row=1)
    p_n=tk.Entry(fr,width=25)
    p_n.grid(column=1,row=1)
    tk.Label(fr,text='*required').grid(column=1,row=4)

    disp=tk.Label(top,text='Start ordering')
    disp.pack(pady=(20,0))
    sec=tk.Button(top,text='Confirm Order',command=bill,bg='yellow')
    sec.pack(side=tk.BOTTOM,fill=tk.X)
    rmv=tk.Button(top,text='Remove',command=remove_c,bg='red')
    rmv.pack(side=tk.BOTTOM,pady=(0,30))
    odr=tk.Button(top,text='Add',command=item_c,bg='lightgray')
    odr.pack(side=tk.BOTTOM,pady=(10,5))
    top.bind('<Return>',item_c)
    o=tk.Label(top,text='Item Code:')
    o.pack(side=tk.LEFT,pady=(85,0),padx=(80,0))
    oe=tk.Entry(top,width=10)
    oe.pack(side=tk.LEFT,pady=(85,0))    

def item_c():
    global ordr, total, v, time
    if oe.get() in code:
        q=int(oe.get())
        ordr.append(q)
        v.append(d[q][0])
#        print(d[q][0],' added.')
        disp.config(text=str(v))
        total+=d[q][1]
        time+=d[q][2]
    else:
        msg.showerror('ERROR','Incorrect Item Code...!')

def remove_c():
    global ordr, total, time, v
    if oe.get() in code:
        q=int(oe.get())
        if q in ordr:
            ordr.remove(q)
            total-=d[q][1]
            time-=d[q][2]
            v.remove(d[q][0])
#            print(d[q][0],' removed.')
            disp.config(text=str(v))
            
        else:
            msg.showerror('ERROR','Item Not Found 404...!')
    else:
        msg.showerror('ERROR','Incorrect Item Code...!')
            
def bill():
    if c_name.get()!='' and len(p_n.get())==10:
        print()
        print('Name: ',c_name.get()) #Assume that name & phone no. are not empty
        print('Phone No.: ',p_n.get())
        print()
        print('-'*10+'BILL'+'-'*10)
        for i in ordr.copy():
            n=ordr.count(i)
            if n!=0:
                print(d[i][0]+' x'+str(n),end=' '*(24-len(d[i][0]+' x'+str(n))-len(str(d[i][1]*n))))
                print(d[i][1]*n)
            while i in ordr:
                ordr.remove(i)
        print('='*24)
        print('TOTAL'+' '*(19-len(str(total)))+str(total))
        print('-'*24)
        print()
        print('THANK YOU, HAVE A NICE DAY')
        print('-'*48)
        print('\n'*3)
        upload()
        top.after(2000,top.destroy)
        msg.showinfo('XX RESTAURANT','YOUR BILL HAS PRINTED \n THANK YOU, HAVE A NICE DAY')
    else:
        msg.showwarning('WTF','Custmor details Error!')

#----------CUSTOMER-DETAILS----------#
def upload():
        if not exist():
                cursor.execute('create table customer_details(name char(20),ph_no char(10),Total int,Date_time char(30));')
        if exist():
                cursor.execute('insert into customer_details values("{}",{},{},"{}");'.format(c_name.get(),p_n.get(),total,xtime.asctime()))
                mycon.commit()


#--------------TABLE---------------#

for i in range(b_menu):
    for j in range(5):#columns
        e=tk.Entry(frame,width=14,font=('Arial',11))
        e.grid(row=i+1,column=j)
        e.insert(tk.END,menu[i][j])
ur=0
if rows>17:
    for i in range(18,rows):
        for j in range(5):
            e=tk.Entry(frame,width=14,font=('Arial',11))
            e.grid(row=ur+1,column=j+7)
            e.insert(tk.END,menu[i][j])
        ur+=1
            

#----------BUTTONS---------------#
start=tk.Button(self,text='ORDER',command=order)
start.pack(side=tk.BOTTOM)

fltr=tk.Button(self,text='FILTER',command=Filter)
fltr.pack(side=tk.LEFT)

ext=tk.Button(self,text='EXIT',command=self.destroy,bg='red',width=15)
ext.pack(side=tk.RIGHT)
label=ttk.Label(self,text='TYPE')
label.pack(side=tk.LEFT,padx=(5,0))

n=tk.StringVar()
ty=ttk.Combobox(self,width=12,textvariable=n)
ty['values']=('all','veg','non-veg','drinks','dessert')
ty.pack(side=tk.LEFT,padx=(10,0))
ty.current(0)

self.mainloop()

mycon.close()

##input()

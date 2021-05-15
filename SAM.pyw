import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
from tkinter import simpledialog
from subprocess import check_call
import binascii
import os


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


root = tk.Tk()
root.iconbitmap(resource_path('SAM.ico'))
root.title('Social Account Management')
root.geometry("400x300+500+300")
root.resizable(0,0)
root.configure(bg='#856ff8')

conn = sq.connect(resource_path('AppData.db'))
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS "accounts" ("acc_username" TEXT NOT NULL, "acc_password" TEXT NOT NULL);')
conn.commit()
task = []

    #------------------------------- Functions--------------------------------

def addRow():
    acc_username = e1.get()
    acc_password = e2.get()
    if len(acc_username)==0 and len(acc_password)==0:
        messagebox.showinfo('Empty Entry', 'Enter Values in Both Fields.')
    elif len(acc_username)==0 :
        messagebox.showinfo('Empty Entry', 'Enter Values in Username Fields.')
    elif len(acc_password)==0 :
        messagebox.showinfo('Empty Entry', 'Enter Values in Password Fields.')
    else:
        listUpdate()
        acc_username =  bin(int(binascii.hexlify(acc_username.encode('utf-8')), 16))
        acc_password =  bin(int(binascii.hexlify(acc_password.encode('utf-8')), 16))
        cur.execute('INSERT INTO accounts VALUES(?,?)',(acc_username,acc_password))
        listUpdate()
        conn.commit()
        e1.delete(0,'end')
        e2.delete(0,'end')


def viewPass():       
    if(t.curselection()):   
        acc_username = t.get(t.curselection())  
        input_pass = simpledialog.askstring(title="Master Passcode", prompt="Verify Master Passcode:")
        if(input_pass=='3020'):
            for row in cur.execute('SELECT acc_password FROM accounts WHERE acc_username=?', (bin(int(binascii.hexlify((acc_username.decode('utf-8')).encode('utf-8')), 16)),)):
                cmd='echo '+binascii.unhexlify('%x' % int(row[0],2)).decode('utf-8').strip()+'|clip'
                if(check_call(cmd, shell=True)==0):
                    messagebox.showinfo('View Password','Your Password is Successfully Copied To ClipBoard Now You Can Paste it.')
    else:
        messagebox.showinfo('View Password','Please Select Username.')

def listUpdate():
    t.delete(0,'end')
    for row in cur.execute('SELECT acc_username FROM accounts'):
        t.insert('end',binascii.unhexlify('%x' % int(row[0],2)))


def delOne():
    try:
        if(t.curselection()): 
            mb = messagebox.askyesno('Delete','Are you sure?')
            if mb==True:
                acc_username = t.get(t.curselection())
                cur.execute('DELETE FROM accounts WHERE acc_username = ?', (bin(int(binascii.hexlify((acc_username.decode('utf-8')).encode('utf-8')), 16)),))
                conn.commit()
                listUpdate()
        else:
            messagebox.showinfo('View Password','Please Select Username.')
    except:
        messagebox.showinfo('Delete Error', 'Can\'t Delete')


def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        while(len(task)!=0):
            task.pop()
        cur.execute('DELETE FROM accounts')
        listUpdate()
    conn.commit()


def bye():
    root.destroy()


def retrieveDB():
    while(len(task)!=0):
        task.pop()
    for row in cur.execute('SELECT acc_username FROM accounts'):
        task.append(binascii.unhexlify('%x' % int(row[0],2)))
    conn.commit()


    #------------------------------- Functions--------------------------------

l2 = ttk.Label(root, background="#856ff8",foreground="black",text='Enter Username: ')
e1 = ttk.Entry(root, width=21)

l3 = ttk.Label(root, background="#856ff8",foreground="black",text='Enter Password: ')
e2 = ttk.Entry(root,show="*",width=21)

t = tk.Listbox(root, height=13,width=22,bg='#856ff9', selectmode='SINGLE')

b1 = ttk.Button(root, text='Add', width=20, command=addRow)
b5 = ttk.Button(root, text='Get Password', width=20, command=viewPass)
b2 = ttk.Button(root, text='Delete', width=20, command=delOne)
b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
b4 = ttk.Button(root, text='Exit', width=20, command=bye)

retrieveDB()
listUpdate()

#Place geometry
l2.place(x=50, y=25)
e1.place(x=50, y=45)

l3.place(x=50, y=68)
e2.place(x=50, y=85)

b1.place(x=50, y=110)
b5.place(x=50, y =140)
b2.place(x=50, y=170)
b3.place(x=50, y=200)
b4.place(x=50, y =230)


t.place(x=220, y = 45)
root.mainloop()

conn.commit()
cur.close()

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
root.geometry("400x325+500+300")
root.resizable(0,0)
root.configure(bg='#856ff8')

conn = sq.connect(resource_path('AppData.db'))
db = conn.cursor()
db.execute('CREATE TABLE IF NOT EXISTS "accounts" ("acc_username" TEXT NOT NULL, "acc_password" TEXT NOT NULL);')
conn.commit()
task = []

    #------------------------------- Functions--------------------------------

def addRow():
    if len(user_entry.get())==0 and len(pass_entry.get())==0 and len(media_entry.get())==0:
        messagebox.showinfo('Empty Entry', 'Enter Text in Both Fields.')
    elif len(user_entry.get())==0 :
        messagebox.showinfo('Empty Entry', 'Enter Text in Username Field.')
    elif len(pass_entry.get())==0 :
        messagebox.showinfo('Empty Entry', 'Enter Text in Password Field.')
    elif len(media_entry.get())==0 :
        messagebox.showinfo('Empty Entry', 'Enter Text in Social Media Field.')
    else:
        listUpdate()
                        #bytes->hex->decimal(ASCII)->binary
        acc_username =  bin(int(binascii.hexlify((user_entry.get()+"("+media_entry.get()+")").encode('utf-8')), 16))
        acc_password =  bin(int(binascii.hexlify(pass_entry.get().encode('utf-8')), 16))

        db.execute('SELECT * FROM accounts WHERE acc_username=?',(acc_username,))
        if(len(db.fetchall())>=1):
            messagebox.showinfo('Warning','Account Already Exist For Social Media.')
        else:
            #Addition Code To Check Repetation Of Same Crentials.
            """  db.execute('SELECT acc_username FROM accounts WHERE acc_password=?',(acc_password,))
            for uname in db.fetchall():
                if(str(binascii.unhexlify('%x' % int(uname[0],2))).partition('(')[0][2:]==str(binascii.unhexlify('%x' % int(acc_username,2))).partition('(')[0][2:]):
                    messagebox.showinfo('Warning','Credentials Already Exist.')
                else:
                    db.execute('INSERT INTO accounts VALUES(?,?)',(acc_username,acc_password))
                    listUpdate()
                    conn.commit()
                    """
            db.execute('INSERT INTO accounts VALUES(?,?)',(acc_username,acc_password))
            listUpdate()
            conn.commit()

        user_entry.delete(0,'end')
        pass_entry.delete(0,'end')
        media_entry.delete(0,'end')

def viewPass():
    if(table_view.curselection()):
        acc_username = table_view.get(table_view.curselection())
        input_pass = simpledialog.askstring(title="Master Passcode",show="*", prompt="Verify Master Passcode:")
        if(input_pass=='3020'):
            for row in db.execute('SELECT acc_password FROM accounts WHERE acc_username=?', (bin(int(binascii.hexlify((acc_username.decode('utf-8')).encode('utf-8')), 16)),)):
                cmd='echo '+binascii.unhexlify('%x' % int(row[0],2)).decode('utf-8').strip()+'|clip'
                if(check_call(cmd, shell=True)==0):
                    messagebox.showinfo('View Password','Your Password is Successfully Copied To ClipBoard Now You Can Paste it.')
    else:
        messagebox.showinfo('View Password','Please Select Username.')

def listUpdate():
    table_view.delete(0,'end')
    for row in db.execute('SELECT acc_username FROM accounts'):
        table_view.insert('end',binascii.unhexlify('%x' % int(row[0],2)))

def delOne():
    try:
        if(table_view.curselection()):
            mb = messagebox.askyesno('Delete','Are you sure?')
            if mb==True:
                acc_username = table_view.get(table_view.curselection())    #bytes->hex->decimal(ASCII)->binary
                db.execute('DELETE FROM accounts WHERE acc_username = ?', (bin(int(binascii.hexlify((acc_username.decode('utf-8')).encode('utf-8')), 16)),))
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
        db.execute('DELETE FROM accounts')
        listUpdate()
    conn.commit()


def bye():
    root.destroy()

    #------------------------------- Functions--------------------------------

user_label = ttk.Label(root, background="#856ff8",foreground="black",text='Enter Username: ')
user_entry = ttk.Entry(root, width=21)

pass_label = ttk.Label(root, background="#856ff8",foreground="black",text='Enter Password: ')
pass_entry = ttk.Entry(root,show="*",width=21)

media_label = ttk.Label(root, background="#856ff8",foreground="black",text='Social Media Name: ')
media_entry = ttk.Entry(root,width=21)

table_view = tk.Listbox(root, height=15,width=22,bg='#856ff9', selectmode='SINGLE')

add_button = ttk.Button(root, text='Add', width=20, command=addRow)
get_pass_button = ttk.Button(root, text='Get Password', width=20, command=viewPass)
delete_one_button = ttk.Button(root, text='Delete', width=20, command=delOne)
delete_all_button = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
exit_button = ttk.Button(root, text='Exit', width=20, command=bye)

listUpdate()

#Place geometry
user_label.place(x=50, y=25)
user_entry.place(x=50, y=45)

pass_label.place(x=50, y=68)
pass_entry.place(x=50, y=85)

media_label.place(x=50, y=110)
media_entry.place(x=50, y=130)

add_button.place(x=50, y=155)
get_pass_button.place(x=50, y =185)
delete_one_button.place(x=50, y=215)
delete_all_button.place(x=50, y=245)
exit_button.place(x=50, y =275)

table_view.place(x=220, y = 45)
root.mainloop()

conn.commit()
db.close()

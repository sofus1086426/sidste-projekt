import sqlite3, hashlib
from tkinter import *

#databasse
with sqlite3.connect("koder.db") as db:
    cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS hovedkode(id INTEGER PRIMARY KEY, password TEXT NOT NULL);")

#Hassing
def hasKodeordet(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

#vinduer
#theme=
window = Tk()

window.title("Password box")

def opratMasterKode():
    window.geometry("350x150")

    lbl = Label(window, text="Lav Et Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=18)
    txt.pack()

    lbl1 = Label(window, text="Gentag Master Password")
    lbl1.pack()

    txt2 = Entry(window, width=18)
    txt2.pack()

    lbl2 = Label(window,)
    lbl2.pack()

    def gemHovedKOde():

        if txt.get() == txt2.get():
            hasedpass = hasKodeordet(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO hovedkode(password) VALUES(?) """
            cursor.execute(insert_password, [(hasedpass)])
            db.commit()
            kodeskab()

        else:
            lbl2.config(text="Koder masher ikke")

    btn = Button(window, text="GEM", command=gemHovedKOde)
    btn.pack(pady=10)

def login():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("350x150")

    lbl = Label(window, text="login")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=18, show="¤")
    txt.pack()

    lbl1 = Label(window)
    lbl1.pack()

    def getkode():
        ceckhasedpass = hasKodeordet(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM hovedkode WHERE ID = 1 AND password = ?, [(ceckhasedpass)]")
        print(ceckhasedpass)
        return cursor.fetchall()

    def checkPassword():
        password = getkode()

        print(password)


        if password:
            kodeskab()
        else:
            txt.delete(0, "end")
            lbl1.config(text="worng")

    btn = Button(window, text="Lav", command=checkPassword)
    btn.pack(pady=10)

def kodeskab():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("500x130")

    lbl = Label(text="BOXEN")
    lbl.config(anchor=CENTER)
    lbl.pack()


cursor.execute("SELECT * FROM hovedkode")
if cursor.fetchall():
    login()
else:
    opratMasterKode()

window.mainloop()

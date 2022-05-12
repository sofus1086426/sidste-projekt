import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

#databasse
with sqlite3.connect("koder.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS hovedkode(id INTEGER PRIMARY KEY, password TEXT NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS box(id INTEGER PRIMARY KEY, 
hjemmeside TEXT NOT NULL,
brugernavn TEXT NOT NULL, kodeord TEXT NOT NULL);""")

#lav pop op
def popup(text):
    svar = simpledialog.askstring("input string", text)
    return (svar)


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
    txt.focus()

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
            kodeSkab()

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
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def getKode():
        ceckhasedpass = hasKodeordet(txt.get().encode('utf-8'))
        cursor.execute("""SELECT * FROM hovedkode WHERE ID = 1 AND password = ?""", [(ceckhasedpass)])
        return cursor.fetchall()

    def checkPassword():
        password = getKode()

        #print(password)

        if password:
            kodeSkab()
        else:
            txt.delete(0, "end")
            lbl1.config(text="worng")

    btn = Button(window, text="Lav", command=checkPassword)
    btn.pack(pady=10)

def kodeSkab():
    for widget in window.winfo_children():
        widget.destroy()


    def tilfoj():
        text1 = "hjemmedide"
        text2 = "brugernavn"
        text3 = "kodeord"

        hjemmeside = popup(text1)
        brugernavn = popup(text2)
        kodeord = popup(text3)

        insert_fields = """INSERT INTO box(hjemmeside, brugernavn, kodeord)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_fields, (hjemmeside, brugernavn, kodeord))
        db.commit()

        kodeSkab()

    def fjernkode(input):
        cursor.execute("DELETE FROM box WHERE id = ?", (input,))
        db.commit()
        kodeSkab()

    window.geometry("800x350")

    lbl = Label(text="BOXEN")
    lbl.config(anchor=CENTER)
    lbl.grid(column=1)

    btn = Button(window, text="+", command=tilfoj)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="hjemmeside")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="brugernavn")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="kodeord")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM box")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM box")
            array = cursor.fetchall()

            if(len(array) == 0):
                break

            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))#hjemmeside
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))#brugernavn
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))#kode
            lbl1.grid(column=2, row=i+3)

            btn1 = Button(window, text="Slet", command=partial(fjernkode, array[i][0]))
            btn1.grid(column=3, row=(i+3), pady=10)

            i = i+1

            cursor.execute('SELECT * FROM box')
            if(len(cursor.fetchall()) <= i):
                break

cursor.execute("""SELECT * FROM hovedkode""")
if cursor.fetchall():
    login()
else:
    opratMasterKode()

window.mainloop()

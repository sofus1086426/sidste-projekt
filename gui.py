import sqlite3, hashlib
import uuid
import pyperclip
import base64
import os
from tkinter import *
from tkinter import simpledialog
from functools import partial
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


#kryptering
backend = default_backend()
salt = b'1337'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)
cryptiosNøgle = 0


def krypter(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypter(message: bytes, token: bytes) -> bytes:
    return Fernet(token).decrypt(message)


#databasse
with sqlite3.connect("koder.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS hovedkode(id INTEGER PRIMARY KEY, password TEXT NOT NULL,
 recoveryKey TEXT NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS box(id INTEGER PRIMARY KEY, 
hjemmeside TEXT NOT NULL,
brugernavn TEXT NOT NULL,
kodeord TEXT NOT NULL);""")

#lav pop op
def popup(text):
    svar = simpledialog.askstring("input string", text)
    return (svar)

#Hassing til master passwordet
def hasKodeordet(input):
    hash = hashlib.sha256(input)
    hash = hash.hexdigest()
    return hash


#vinduer
#theme=
window = Tk()
window.title("Password Maneger")


def opratMasterKode():
    for widget in window.winfo_children():
        widget.destroy()
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
            sql = "DELETE FROM hovedkode WHERE id = 1"

            cursor.execute(sql)

            hasedpass = hasKodeordet(txt.get().encode('utf-8'))
            key = str(uuid.uuid4().hex)
            recoveryKey = hasKodeordet(key.encode('utf-8'))

            global cryptiosNøgle
            cryptiosNøgle = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))

            insert_password = """INSERT INTO hovedkode(password, recoveryKey) VALUES(?, ?) """
            cursor.execute(insert_password, ((hasedpass), (recoveryKey)))
            db.commit()
            recoveryVindu(key)

        else:
            lbl2.config(text="Koder masher ikke")

    btn = Button(window, text="GEM", command=gemHovedKOde)
    btn.pack(pady=10)


def recoveryVindu(key):
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("350x150")

    lbl = Label(window, text="gem nøglen for recovery")
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window, text=key)
    lbl1.pack()

    def kopirKey():
        pyperclip.copy(lbl1.cget("text"))

    btn = Button(window, text="Kopir nøglen til clipboard", command=kopirKey)
    btn.pack(pady=10)

    def næste():# uden denne funktion kommer der en den error beskeder, men programet virker stadigt
        kodeSkab()

    btn = Button(window, text="næste", command=næste)
    btn.pack(pady=10)


def resetvindu():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("350x150")

    lbl = Label(window, text="inset recovery nøgle")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    lbl1 = Label(window,)
    lbl1.pack()

    def hetntrecoverykey():
        recoveryKeyCheck = hasKodeordet(str(txt.get()).encode("utf-8"))
        cursor.execute('SELECT * FROM hovedkode WHERE id = 1 AND  recoveryKey = ?', [(recoveryKeyCheck)])
        return cursor.fetchall()

    def checkRecoveryKey():
        checked = hetntrecoverykey()

        if checked:
            opratMasterKode()
        else:
            txt.delete(0, 'end')
            lbl1.config(text='Forkert Nøgle')


    btn = Button(window, text="Check Nøgle", command=checkRecoveryKey)
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
        global cryptiosNøgle
        cryptiosNøgle = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))
        cursor.execute("""SELECT * FROM hovedkode WHERE ID = 1 AND password = ?""", [(ceckhasedpass)])
        return cursor.fetchall()

    def checkPassword():
        password = getKode()

        if password:
            kodeSkab()
        else:
            txt.delete(0, "end")
            lbl1.config(text="worng")


    def resetpass():
        resetvindu()

    btn = Button(window, text="Næste", command=checkPassword)
    btn.pack(pady=10)

    btn = Button(window, text="Reset password", command=resetpass)
    btn.pack(pady=10)


def kodeSkab():
    for widget in window.winfo_children():
        widget.destroy()

    def tilfoj():
        text1 = "hjemmedide"
        text2 = "brugernavn"
        text3 = "kodeord"

        hjemmeside = krypter(popup(text1).encode(), cryptiosNøgle)
        brugernavn = krypter(popup(text2).encode(), cryptiosNøgle)
        kodeord = krypter(popup(text3).encode(), cryptiosNøgle)

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
    if cursor.fetchall() is not None:
        i = 0
        while True:
            cursor.execute("SELECT * FROM box")
            array = cursor.fetchall()

            if len(array) == 0:
                break

            lbl1 = Label(window, text=(decrypter(array[i][1], cryptiosNøgle)), font=("Helvetica", 12))#hjemmeside
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(decrypter(array[i][2], cryptiosNøgle)), font=("Helvetica", 12))#brugernavn
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(decrypter(array[i][3], cryptiosNøgle)), font=("Helvetica", 12))#kode
            lbl1.grid(column=2, row=i+3)

            btn1 = Button(window, text="Slet", command=partial(fjernkode, array[i][0]))
            btn1.grid(column=3, row=(i+3), pady=10)

            i = i+1

            cursor.execute('SELECT * FROM box')
            if len(cursor.fetchall()) <= i:
                break


cursor.execute("""SELECT * FROM hovedkode""")
if cursor.fetchall():
    login()
else:
    opratMasterKode()
window.mainloop()

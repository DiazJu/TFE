from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import *
import sqlite3
from sqlite3 import Error


def connection(base):
    global cur, db  # attention global
    try:
        db = sqlite3.connect(base)
        cur = db.cursor()
    except Error as e:
        print(e)
    return None


def fenetre():
    global fen
    fen = Tk()
    fen.title("Page d'Accueil")
    fen.geometry("1000x600")
    fen.configure(bg='#F0F0F0')

    fen.image = PhotoImage(file='Image\hoteldelsol.png')

    fen.canvas = Canvas(fen, width=1000, height=500, background='#F0F0F0', borderwidth=None)
    fen.canvas.pack()
    fen.canvas.create_image(500, 200, image=fen.image)
    fen.canvas.grid(row=0, columnspan=3)

    Button(fen, text="Hotel", command=mainpagegestionhotel, font='Georgia', width=20, bg="lightgrey").grid(row=2, column=0)
    Button(fen, text="Villes",command=mainpageville, font='Georgia', width=20, bg="lightgrey").grid(row=2, column=1)
    Button(fen, text="Reservation",command=mainpagereserv, font='Georgia', width=20, bg="lightgrey").grid(row=2, column=2)

# --------------------------------------Hotel---------------------------------------------------------------------------


def mainpagegestionhotel():
    global win, tables, cur
    # création d'une fenêtre modal
    win = Toplevel(fen)
    win.title("Gestion des hôtels")


    tables = ttk.Treeview(win)
    tables.grid(row=0, columnspan=6, sticky=N + E + S + W, padx=10, pady=10)  # remplit toute la zone de root

    # Déclaration des colonnes
    tables["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")

    # taille des colonnes
    tables.column("#1", width=30, minwidth=30)
    tables.column("#2", width=100, minwidth=100)
    tables.column("#3", width=200, minwidth=200)
    tables.column("#4", width=100, minwidth=100)
    tables.column("#5", width=100, minwidth=100)
    tables.column("#6", width=30, minwidth=30)

    # entête ( titre ) de la colonne
    tables.heading("col1", text="id", anchor=W)
    tables.heading("col2", text="Nom hotel", anchor=W)
    tables.heading("col3", text="Adresse", anchor=W)
    tables.heading("col4", text="Code postal", anchor=W)
    tables.heading("col5", text="Prix", anchor=W)
    tables.heading("col6", text="Villes", anchor=W)

    # Paramètré la scrollbar
    ascenseurY = ttk.Scrollbar(win, orient=VERTICAL, command=tables.yview)
    # positionné la scrollbar
    ascenseurY.grid(row=0, column=6, sticky='nse')

    # configurer notre treeview
    tables.config(show="headings", height=10, selectmode="browse",
                  yscrollcommand=ascenseurY.set)  # height c'est le nombre de lignes a affiché
    remplisagehotel()
    # Boutons
    Button(win, text="Ajouter", command=ajoutehotel).grid(row=6, column=1, padx=5, sticky=E + W)
    Button(win, text="Modifier", command=modifh).grid(row=6, column=2, padx=5, sticky=E + W)
    Button(win, text="Supprimer", command=supprimehotel).grid(row=6, column=3, padx=5, sticky=E + W)
    Button(win, text="Annuler", command=win.destroy).grid(row=6, column=4, padx=5, sticky=E + W)


def ajoutehotel():
    global win,tables, cur
    # création d'une fenêtre modal
    win = Toplevel(fen)
    win.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    nomhotel = StringVar()
    adresse = StringVar()
    prixch = DoubleVar()
    codepostal = IntVar()
    idville = IntVar()

    # etiquettes
    Label(win, text="Nom Hotel").grid(row=1, column=0, pady=5, padx=5)
    Label(win, text="Adresse").grid(row=2, column=0, pady=5, padx=5)
    Label(win, text="Code posal").grid(row=3, column=0, pady=5, padx=5)
    Label(win, text="Prix").grid(row=4, column=0, pady=5, padx=5)
    Label(win, text="Villes").grid(row=5, column=0, pady=5, padx=5)

    # Les entrys
    Entry(win, textvariable=nomhotel, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=adresse, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=codepostal, width=30).grid(row=3, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=prixch, width=30).grid(row=4, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=idville, width=30).grid(row=5, column=1, columnspan=2, padx=5)

    # Boutons
    Button(win, text="Ajouter", command=lambda: ajoutdbhotel(nomhotel.get(), adresse.get(), codepostal.get(), prixch.get(),idville.get())).grid(row=7, column=1, padx=5, sticky=E + W)
    Button(win, text="Annuler", command=win.destroy).grid(row=7, column=2, padx=5, pady=10, sticky=E + W)


def ajoutdbhotel(nomhotel, adresse, codepostal, prixch, idville):  # sql autre fichier c'est mieux
    global win, tables
    win.destroy()
    if nomhotel != "" and adresse != "":
        query = '''
            INSERT INTO Hotels (nomhotel, adresse, codepostal,prixch)
                    VALUES (?, ?, ?, ?)'''

        cur.execute(query, (nomhotel, adresse, codepostal, prixch))  # re crée un cur avec la db
        db.commit()
        remplisagehotel()


def modifiehotel():
    global win,tables, cur,winmh
    # création d'une fenêtre modal
    winmh = Toplevel(fen)
    winmh.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    nomhotel=StringVar()
    adresse = StringVar()
    prixch = DoubleVar()
    codepostal = IntVar()
    idville = IntVar()

    # etiquettes
    Label(winmh, text="Nom hôtel").grid(row=1, column=0, pady=5, padx=5)
    Label(winmh, text="Adresse").grid(row=2, column=0, pady=5, padx=5)
    Label(winmh, text="Code posal").grid(row=3, column=0, pady=5, padx=5)
    Label(winmh, text="Prix").grid(row=4, column=0, pady=5, padx=5)
    Label(winmh, text="Villes").grid(row=5, column=0, pady=5, padx=5)

    # Les entrys
    Entry(winmh, textvariable=nomhotel, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(winmh, textvariable=adresse, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(winmh, textvariable=codepostal, width=30).grid(row=3, column=1, columnspan=2, padx=5)
    Entry(winmh, textvariable=prixch, width=30).grid(row=4, column=1, columnspan=2, padx=5)
    Entry(winmh, textvariable=idville, width=30).grid(row=5, column=1, columnspan=2, padx=5)

    # Boutons
    Button(winmh, text="Modifier", command=lambda: modifdbhotel(nomhotel.get(), adresse.get(), codepostal.get(), prixch.get())).grid(row=6, column=1, padx=5, sticky=E + W)
    Button(winmh, text="Annuler", command=winmh.destroy).grid(row=6, column=2, padx=5, pady=10, sticky=E + W)


def modifh():
    global winmh,idmodifierh,tables
    if tables.focus():
        nomhotel = tables.item(tables.focus())["values"][1]
        idmodifierh = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Modifier" + " " + nomhotel + " ?")
        if confirm:
            modifiehotel()
            db.commit()
            remplisagehotel()
    else :
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nmodifier")


def modifdbhotel(nomhotel, adresse, codepostal, prixch):
    query='''
    UPDATE Hotels SET nomhotel=?, adresse=?, codepostal=?, prixch=? WHERE idhotel=? '''
    cur.execute(query, (nomhotel, adresse, codepostal, prixch, idmodifierh))
    db.commit()
    winmh.destroy()
    remplisagehotel()


def supprimehotel():
    global tables
    if tables.focus():
        nomhotel = tables.item(tables.focus())["values"][1]
        adresse = tables.item(tables.focus())["values"][2]
        idAsupprimer = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Suppression de " + nomhotel + " " + adresse + " ?")
        if confirm:
            # supprimer le record
            cur.execute("DELETE FROM Hotels WHERE idhotel = ?", (idAsupprimer,))
            db.commit()
            remplisagehotel()
    else:
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nsupprimer")


def remplisagehotel():
    global tables, cur

    # vider la liste
    tables.delete(*tables.get_children())

    # récupérer la liste de la db
    cur.execute("SELECT * FROM Hotels ")
    Hotels= cur.fetchall()

    # Ajouter les etudiants dans le treeview
    for Hotel in Hotels:
        tables.insert('', 'end', values=(Hotel[0], Hotel[1], Hotel[2], Hotel[3], Hotel[4], Hotel[5]))

# --------------------------------------Villes--------------------------------------------------------------------------


def mainpageville():
    global win, tables, cur

    # création d'une fenêtre modal
    winV = Toplevel(fen)
    winV.title("Gestion des Villes")

    tables = ttk.Treeview(winV)
    tables.grid(row=0, columnspan=4, sticky=N + E + S + W, padx=10, pady=10)  # remplit toute la zone de root

    # Déclaration des colonnes
    tables["columns"] = ("col1", "col2", "col3")

    # taille des colonnes
    tables.column("#1", width=30, minwidth=30)
    tables.column("#2", width=200, minwidth=200)
    tables.column("#3", width=200, minwidth=200)

    # entête ( titre ) de la colonne
    tables.heading("col1", text="idVille", anchor=W)
    tables.heading("col2", text="Nom Ville", anchor=W)
    tables.heading("col3", text="Nom Province", anchor=W)

    # Paramètré la scrollbar
    ascenseurY = ttk.Scrollbar(winV, orient=VERTICAL, command=tables.yview)
    # positionné la scrollbar
    ascenseurY.grid(row=0, column=4, sticky='nse')

    # configurer notre treeview
    tables.config(show="headings", height=10, selectmode="browse", yscrollcommand=ascenseurY.set)  # height c'est le nombre de lignes a affiché
    remplisagevilles()
    # Boutons
    Button(winV, text="Ajouter", command=ajouteville, width=3).grid(row=6, column=1, padx=2, sticky=E + W)
    Button(winV, text="Modifier", command=modifv, width=3).grid(row=6, column=2, padx=2, sticky=E + W)
    Button(winV, text="Supprimer", command=supprimeville, width=3).grid(row=6, column=3, padx=2, sticky=E + W)
    Button(winV, text="Annuler", command=winV.destroy, width=15).grid(row=6, column=4, padx=2, sticky=E + W)


def ajouteville():
    global winA,tables, cur
    # création d'une fenêtre modal
    winA = Toplevel(fen)
    winA.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    idville = IntVar()
    nomville = StringVar()
    nomprovince = StringVar()

    # etiquettes
    Label(winA, text="Id Ville").grid(row=1, column=0, pady=5, padx=5)
    Label(winA, text="Ville").grid(row=2, column=0, pady=5, padx=5)
    Label(winA, text="Province").grid(row=3, column=0, pady=5, padx=5)

    # Les entrys
    Entry(winA, textvariable=idville, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(winA, textvariable=nomville, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(winA, textvariable=nomprovince, width=30).grid(row=3, column=1, columnspan=2, padx=5)

    # Boutons
    Button(winA, text="Ajouter", command=lambda: ajoutdbville(nomville.get(), nomprovince.get())).grid(row=4, column=1, padx=5, sticky=E + W)
    Button(winA, text="Annuler", command=winA.destroy).grid(row=4, column=2, padx=5, pady=10, sticky=E + W)


def ajoutdbville(nomville, nomprovince):  # sql autre fichier c'est mieux
    global winA, tables
    winA.destroy()
    if nomville != "" and nomprovince != "":
        query = '''
            INSERT INTO Villes (nomville, nomprovince)
                    VALUES (?, ?)'''

        cur.execute(query, (nomville, nomprovince))  # re crée un cur avec la db
        db.commit()
        remplisagevilles()


def modifieville():
    global winM,tables, cur
    # création d'une fenêtre modal
    winM = Toplevel(fen)
    winM.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    idville = IntVar()
    nomville = StringVar()
    nomprovince = StringVar()

    # etiquettes
    Label(winM, text="Id Ville").grid(row=1, column=0, pady=5, padx=5)
    Label(winM, text="Ville").grid(row=2, column=0, pady=5, padx=5)
    Label(winM, text="Province").grid(row=3, column=0, pady=5, padx=5)

    # Les entrys
    Entry(winM, textvariable=idville, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(winM, textvariable=nomville, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(winM, textvariable=nomprovince, width=30).grid(row=3, column=1, columnspan=2, padx=5)

    # Boutons
    Button(winM, text="Modifier", command=lambda: modifdbville(nomville.get(), nomprovince.get())).grid(row=4, column=1, padx=5, sticky=E + W)
    Button(winM, text="Annuler", command=winM.destroy).grid(row=4, column=2, padx=5, pady=10, sticky=E + W)


def modifv():
    global tables, fen, idAmodifierv
    if (tables.focus()) :
        nomville = tables.item(tables.focus())["values"][1]
        idAmodifierv = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Modifier" + " " + nomville + " ?")
        if confirm:
            modifieville()
            db.commit()
            remplisagevilles()
    else :
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nmodifier")


def modifdbville(nomville, nomprovince):
    global winM
    winM.destroy()
    if nomville != "" or nomprovince !="":
        query='''
        UPDATE Villes SET nomville=?, nomprovince=? WHERE idvillle=? '''
        cur.execute(query, (nomville, nomprovince, idAmodifierv))
        db.commit()
        remplisagevilles()


def supprimeville():
    global tables
    if tables.focus():
        nomville = tables.item(tables.focus())["values"][1]
        nomprovince = tables.item(tables.focus())["values"][2]
        idAsupprimer = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Suppression de " + nomville + " " + nomprovince + " ?")
        if confirm:
            # supprimer le record
            cur.execute("DELETE FROM Villes WHERE idvillle = ?", (idAsupprimer,))
            db.commit()
            remplisagevilles()
    else:
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nsupprimer")


def remplisagevilles():
    global tables, cur

    # vider la liste
    tables.delete(*tables.get_children())

    # récupérer la liste de la db
    cur.execute("SELECT * FROM Villes")
    Villes= cur.fetchall()

    # Ajouter les etudiants dans le treeview
    for Ville in Villes:
        tables.insert('', 'end', values=(Ville[0], Ville[1], Ville[2]))


# --------------------------------------Reservation--------------------------------------------------------------------------
def mainpagereserv():
    global winr, tables, cur

    # création d'une fenêtre modal
    winr = Toplevel(fen)
    winr.title("Gestion des reservations")

    tables = ttk.Treeview(winr)
    tables.grid(row=0, columnspan=6, sticky=N + E + S + W, padx=10, pady=10)  # remplit toute la zone de root

    # Déclaration des colonnes
    tables["columns"] = ("col1", "col2", "col3","col4", "col5", "col6")

    # taille des colonnes
    tables.column("#1", width=30, minwidth=30)
    tables.column("#2", width=100, minwidth=100)
    tables.column("#3", width=100, minwidth=100)
    tables.column("#4", width=150, minwidth=150)
    tables.column("#5", width=80, minwidth=80)
    tables.column("#6", width=80, minwidth=80)

    # entête ( titre ) de la colonne
    tables.heading("col1", text="Idreserv", anchor=W)
    tables.heading("col2", text="Nom ", anchor=W)
    tables.heading("col3", text="Prénom", anchor=W)
    tables.heading("col4", text="Mail", anchor=W)
    tables.heading("col5", text="Nombre de chambre ", anchor=W)
    tables.heading("col6", text="Id Hotel", anchor=W)

    # Paramètré la scrollbar
    ascenseurY = ttk.Scrollbar(winr, orient=VERTICAL, command=tables.yview)
    # positionné la scrollbar
    ascenseurY.grid(row=0, column=6, sticky='nse')

    # configurer notre treeview
    tables.config(show="headings", height=10, selectmode="browse", yscrollcommand=ascenseurY.set)  # height c'est le nombre de lignes a affiché
    remplisagereserv()
    # Boutons
    Button(winr, text="Ajouter",command=ajoutereserv, width=3).grid(row=6, column=1, padx=2, sticky=E + W)
    Button(winr, text="Modifier",command=modifr, width=3).grid(row=6, column=2, padx=2, sticky=E + W)
    Button(winr, text="Supprimer",command=supprimereserv, width=3).grid(row=6, column=3, padx=2, sticky=E + W)
    Button(winr, text="Annuler", command=winr.destroy, width=3).grid(row=6, column=4, padx=2, sticky=E + W)


def ajoutereserv():
    global winAr,tables, cur
    # création d'une fenêtre modal
    winAr = Toplevel(fen)
    winAr.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    idreserv = IntVar()
    nom = StringVar()
    prenom = StringVar()
    mail = StringVar()
    nbch = IntVar()
    idhotel = IntVar()

    # etiquettes
    Label(winAr, text="Id Reservation").grid(row=1, column=0, pady=5, padx=5)
    Label(winAr, text="Nom").grid(row=2, column=0, pady=5, padx=5)
    Label(winAr, text="Prénom").grid(row=3, column=0, pady=5, padx=5)
    Label(winAr, text="Mail").grid(row=4, column=0, pady=5, padx=5)
    Label(winAr, text="Nombre de chambre").grid(row=5, column=0, pady=5, padx=5)
    Label(winAr, text="Id hotel").grid(row=6, column=0, pady=5, padx=5)

    # Les entrys
    Entry(winAr, textvariable=idreserv, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(winAr, textvariable=nom, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(winAr, textvariable=prenom, width=30).grid(row=3, column=1, columnspan=2, padx=5)
    Entry(winAr, textvariable=mail, width=30).grid(row=4, column=1, columnspan=2, padx=5)
    Entry(winAr, textvariable=nbch, width=30).grid(row=5, column=1, columnspan=2, padx=5)
    Entry(winAr, textvariable=idhotel, width=30).grid(row=6, column=1, columnspan=2, padx=5)

    # Boutons
    Button(winAr, text="Ajouter", command=lambda: ajoutdbreserv(idreserv.get(),nom.get(), prenom.get(),mail.get(),nbch.get(),idhotel.get())).grid(row=7, column=1, padx=5, sticky=E + W)
    Button(winAr, text="Annuler", command=winAr.destroy).grid(row=7, column=2, padx=5, pady=10, sticky=E + W)


def ajoutdbreserv(idreserv, nom,prenom,mail,nbch,idhotel):  # sql autre fichier c'est mieux
    global winAr, tables
    winAr.destroy()
    if nom != "" and prenom != "":
        query = '''
            INSERT INTO Reservation (idreserv, nom,prenom,mail,nbch,idhotel)
                    VALUES (?, ?,?,?,?,?)'''

        cur.execute(query, (idreserv,nom, prenom,mail,nbch,idhotel))  # re crée un cur avec la db
        db.commit()
        remplisagereserv()


def modifreserv():
    global winMr,tables, cur
    # création d'une fenêtre modal
    winMr = Toplevel(fen)
    winMr.title("Gestion des hôtels")

    # Déclaration des variables du formulaire
    idreserv = IntVar()
    nom = StringVar()
    prenom = StringVar()
    mail = StringVar()
    nbch = IntVar()
    idhotel = IntVar()

    # etiquettes
    Label(winMr, text="Id Reservation").grid(row=1, column=0, pady=5, padx=5)
    Label(winMr, text="Nom").grid(row=2, column=0, pady=5, padx=5)
    Label(winMr, text="Prénom").grid(row=3, column=0, pady=5, padx=5)
    Label(winMr, text="Mail").grid(row=4, column=0, pady=5, padx=5)
    Label(winMr, text="Nombre de chambre").grid(row=5, column=0, pady=5, padx=5)
    Label(winMr, text="Id hotel").grid(row=6, column=0, pady=5, padx=5)

    # Les entrys
    Entry(winMr, textvariable=idreserv, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(winMr, textvariable=nom, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    Entry(winMr, textvariable=prenom, width=30).grid(row=3, column=1, columnspan=2, padx=5)
    Entry(winMr, textvariable=mail, width=30).grid(row=4, column=1, columnspan=2, padx=5)
    Entry(winMr, textvariable=nbch, width=30).grid(row=5, column=1, columnspan=2, padx=5)
    Entry(winMr, textvariable=idhotel, width=30).grid(row=6, column=1, columnspan=2, padx=5)

    # Boutons
    Button(winMr, text="Modifier", command=lambda: modifdbreserv(idreserv.get(),nom.get(), prenom.get(),mail.get(),nbch.get(),idhotel.get())).grid(row=7, column=1, padx=5, sticky=E + W)
    Button(winMr, text="Annuler", command=winMr.destroy).grid(row=7, column=2, padx=5, pady=10, sticky=E + W)


def modifr():
    global tables, fen, idAmodifierr
    if (tables.focus()) :
        nom = tables.item(tables.focus())["values"][1]
        idAmodifierr = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Modifier" + " " + nom + " ?")
        if confirm:
            modifreserv()
            db.commit()
            remplisagereserv()
    else :
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nmodifier")


def modifdbreserv(idreserv,nom, prenom,mail,nbch,idhotel):
    global winMr
    winMr.destroy()
    if nom != "" or prenom !="":
        query='''
        UPDATE Reservation SET idreserv=?, nom=?, prenom=?,mail=?,nbch=?,idhotel=? WHERE idreserv=? '''
        cur.execute(query, (idreserv, nom,prenom,mail,nbch,idhotel,idAmodifierr))
        db.commit()
        remplisagevilles()


def supprimereserv():
    global tables
    if tables.focus():
        nom = tables.item(tables.focus())["values"][1]
        prenom = tables.item(tables.focus())["values"][2]
        idAsupprimersr = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Suppression de " + nom + " " + prenom + " ?")
        if confirm:
            # supprimer le record
            cur.execute("DELETE FROM Reservation WHERE idreserv = ?", (idAsupprimersr,))
            db.commit()
            remplisagereserv()
    else:
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nsupprimer")



def remplisagereserv():
    global tables, cur

    # vider la liste
    tables.delete(*tables.get_children())

    # récupérer la liste de la db
    cur.execute("SELECT * FROM Reservation")
    Reservations= cur.fetchall()

    # Ajouter les etudiants dans le treeview
    for reservation in Reservations:
        tables.insert('', 'end', values=(reservation[0], reservation[1], reservation[2],reservation[3], reservation[4], reservation[5]))


if __name__ == '__main__':
    connection("database\Hotel.db")
    fenetre()
    mainloop()
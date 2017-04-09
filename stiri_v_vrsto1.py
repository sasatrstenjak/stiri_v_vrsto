import tkinter

from razred_igra import *
from razred_clovek import *

class Gui():
    TAG_ZETON = "zeton"
    TAG_OKVIR = "okvir"
    VELIKOST_POLJA = 80

    def __init__(self, master):

        self.rdeci = None
        self.modri = None
        self.igra = None
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        glavni_menu = tkinter.Menu(master)
        master.config(menu = glavni_menu)

        podmenu = tkinter.Menu(glavni_menu)
        glavni_menu.add_cascade(label = "Možnosti", menu = podmenu)
        podmenu.add_command(label = "Nova igra", command = self.nova_igra)
        

        self.plosca = tkinter.Canvas(master, width = 7*Gui.VELIKOST_POLJA, height = 7*Gui.VELIKOST_POLJA)
        self.plosca.grid(row = 1, column = 0)

         

        self.narisi_polje()
        
        self.plosca.bind("<Button-1>", self.plosca_klik)

        self.napis = tkinter.StringVar(master, value = "Igra 4 v vrsto se je pričela!")
        tkinter.Label(master, textvariable = self.napis).grid(row = 0, column = 0)

        self.nova_igra()

    def nova_igra(self):
        self.plosca.delete(Gui.TAG_ZETON)
            
        #prekinemo igralce
        self.prekini_igralce()
        # Nastavimo igralce
        self.rdeci = Clovek(self)
        self.modri = Clovek(self)
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_ZETON)
        # Ustvarimo novo igro
        self.igra = Igra()
        # Modri je prvi na potezi
        self.napis.set("Na potezi je MODRI.")
        self.modri.igraj()


    def koncaj_igro(self):
        self.napis.set("Konec igre!")

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.modri: self.modri.prekini()
        if self.rdeci: self.rdeci.prekini()

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()
    

    def narisi_polje(self):
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.plosca.create_line(0.02*d, d, 0.02*d, 7*d, tag = Gui.TAG_OKVIR)
        
        for i in range (1,9): #navpicne crte
            self.plosca.create_line(i*d, d, i*d, 7*d, tag = Gui.TAG_OKVIR)
        for j in range(1,8):#vodoravne crte
            self.plosca.create_line(0, j*d, 7*d, j*d, tag = Gui.TAG_OKVIR)

    def narisi_modri(self, p):
        #narise moder krogec v polje (i,j)
        x = p[0]*Gui.VELIKOST_POLJA
        sirina = 3
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1

        for i in range (1,7):
            if self.igra.stolpci[x//Gui.VELIKOST_POLJA][6-i]!= 0:
                self.y -= Gui.VELIKOST_POLJA
                self.stevec_polj += 1
            else:
                self.igra.stolpci[x//Gui.VELIKOST_POLJA][5 - self.stevec_polj] = "M"
                self.plosca.create_oval(x+d1, self.y+d1, x+d2, self.y+d2, width=sirina, tag=Gui.TAG_ZETON, fill = "blue")
                break
                
        print (self.igra.stolpci)
    
    def narisi_rdeci(self, p):
        #narise rdec krogec v polje (i,j)
        x = p[0]*Gui.VELIKOST_POLJA
        sirina = 3

        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        
        for i in range (1,7):
            if self.igra.stolpci[x//Gui.VELIKOST_POLJA][6-i]!= 0:
                self.y-= Gui.VELIKOST_POLJA
                self.stevec_polj +=1
            else:
                self.igra.stolpci[x//Gui.VELIKOST_POLJA][5 - self.stevec_polj] = "R"
                self.plosca.create_oval(x+d1, self.y+d1, x+d2, self.y+d2, width=sirina, tag=Gui.TAG_ZETON, fill = "red")
                break
                
        print (self.igra.stolpci)

        
    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // Gui.VELIKOST_POLJA
        j = event.y // Gui.VELIKOST_POLJA
        if self.igra.stolpci[i][0] == 0: #to zagotovi, da še so vsa polja v nekem stolpcu že polna, se ne zgodi nič
            print ("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
            if self.igra.na_potezi == MODRI:
                self.modri.klik((i,j))
            elif self.igra.na_potezi == RDECI:
                self.rdeci.klik((i,j))
            else:
                # Nihče ni na potezi, ne naredimo nič
                pass
        else:
            # klik izven plošče
            pass

    def povleci_potezo(self, p):
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        # Najprej povlečemo potezo v igri, še pred tem si zapomnimo, kdo jo je povlekel
        # (ker bo self.igra.povleci_potezo spremenil stanje igre).
        # GUI se *ne* ukvarja z logiko igre, zato ne preverja, ali je poteza veljavna.
        # Ta del bo kasneje za njega opravil self.igra.
        igralec = self.igra.na_potezi
        self.igra.povleci_potezo(p)
        self.stevec_polj = 0 #ta stevec šteje koliko polj v stolcpu je že zasedenih
        self.y = 6*Gui.VELIKOST_POLJA
        if igralec == MODRI:
            self.narisi_modri(p)
        elif igralec == RDECI:
            self.narisi_rdeci(p)
        # Popravimo napis, kdo je na potezi
        self.napis.set("Na potezi je {0}".format(
            'MODRI' if self.igra.na_potezi == MODRI else 'RDECI'))

    

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Štiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()





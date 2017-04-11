import tkinter

from razred_igra import *
from razred_clovek import *
from razred_racunalnik import *

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == RDECI:
        return MODRI
    elif igralec == MODRI:
        return RDECI
    else:

        assert False, "neveljaven nasprotnik"

class Gui():
    TAG_FIGURA = "figura"
    TAG_OKVIR = "okvir"
    VELIKOST_POLJA = 50
    ODMIK = 0.25

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
        

        self.plosca = tkinter.Canvas(master, width = 7.5*Gui.VELIKOST_POLJA, height = 7.5*Gui.VELIKOST_POLJA)
        self.plosca.grid(row = 1, column = 0)
         

        self.narisi_polje()
        
        self.plosca.bind("<Button-1>", self.plosca_klik)

        self.napis = tkinter.StringVar(master, value = "Igra 4 v vrsto se je pričela!")
        tkinter.Label(master, textvariable = self.napis).grid(row = 0, column = 0)

        self.nova_igra()

    def nova_igra(self):
        self.plosca.delete(Gui.TAG_FIGURA)
        #prekinemo igralce
        self.prekini_igralce()
        # Nastavimo igralce
        self.rdeci = Clovek(self)
        self.modri = Clovek(self)
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        # Ustvarimo novo igro
        self.igra = Igra()
        # Modri je prvi na potezi
        self.napis.set("Na potezi je MODRI.")
        self.modri.igraj()


    def koncaj_igro(self, zmagovalec, stirica):
        print(stirica)
        if zmagovalec == MODRI:
            self.napis.set("Zmagal je MODRI.")
            self.obkrozi_zmagovalno_stirico(zmagovalec, stirica)
            #self.narisi_zmagovalno_trojico(zmagovalec, trojka)
        elif zmagovalec == RDECI:
            self.napis.set("Zmagal je RDECI.")
            self.obkrozi_zmagovalno_stirico(zmagovalec, stirica)
            #self.narisi_zmagovalno_trojico(zmagovalec, trojka)
        else:
            self.napis.set("Neodločeno.")

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
        self.plosca.create_line(Gui.ODMIK * d, d, Gui.ODMIK*d, 7 * d, tag = Gui.TAG_OKVIR)

        for i in range(1, 9):  # navpicne crte
            self.plosca.create_line((i+Gui.ODMIK)*d, (d-(Gui.ODMIK)), (i+Gui.ODMIK) *d, 7 * (d-(Gui.ODMIK)), tag=Gui.TAG_OKVIR)
        for j in range(1, 8):  # vodoravne crte
            self.plosca.create_line(Gui.ODMIK*d, j * (d-(Gui.ODMIK)), 7*d+Gui.ODMIK * d, j * (d-Gui.ODMIK), tag=Gui.TAG_OKVIR)

    def narisi_modri(self, p):
        #narise moder krogec v polje (i,j)
        x = p[0] * Gui.VELIKOST_POLJA
        sirina = 3
        d1 = Gui.VELIKOST_POLJA / 10
        d2 = Gui.VELIKOST_POLJA - d1

        for i in range(1, 7):
            if self.igra.stolpci[x // Gui.VELIKOST_POLJA][6 - i] != 0:
                self.y -= Gui.VELIKOST_POLJA
                self.stevec_polj += 1
            else:
                self.igra.stolpci[x // Gui.VELIKOST_POLJA][5 - self.stevec_polj] = "M"
                self.plosca.create_oval(x + d1 + Gui.VELIKOST_POLJA * Gui.ODMIK, self.y + d1,
                                        x + d2 + Gui.VELIKOST_POLJA * Gui.ODMIK, self.y + d2, width=sirina,
                                        tag=Gui.TAG_FIGURA,
                                        fill="blue")
                break

        print (self.igra.stolpci)
    
    def narisi_rdeci(self, p):
        # narise rdec krogec v polje (i,j)
        x = p[0] * Gui.VELIKOST_POLJA
        sirina = 3
        d1 = Gui.VELIKOST_POLJA / 10
        d2 = Gui.VELIKOST_POLJA - d1


        for i in range(1, 7):
            if self.igra.stolpci[x // Gui.VELIKOST_POLJA][6 - i] != 0:
                self.y -= Gui.VELIKOST_POLJA
                self.stevec_polj += 1
            else:
                self.igra.stolpci[x // Gui.VELIKOST_POLJA][5 - self.stevec_polj] = "R"
                self.plosca.create_oval(x + d1 + Gui.VELIKOST_POLJA*Gui.ODMIK, self.y + d1, x + d2 +Gui.VELIKOST_POLJA*Gui.ODMIK, self.y + d2, width=sirina,
                                        tag=Gui.TAG_FIGURA,
                                        fill="red")
                break
                
        print (self.igra.stolpci)

    def obkrozi_zmagovalno_stirico(self, zmagovalec, stirica):
        d = Gui.VELIKOST_POLJA
        barva = "red"

        (i1, j1) = stirica[0]
        (i2, j2) = stirica[1]
        (i3, j3) = stirica[2]
        (i4, j4) = stirica[3]

        if zmagovalec == MODRI:
            barva = "blue"
        if j1==j2==j3==j4: #v primeru, da je zmagal s stolpcem
            self.plosca.create_rectangle(j1 * d + Gui.ODMIK, (i1+1) * d, (j1+1) * d + Gui.ODMIK, (i4 + 2) * d, width=5, outline = barva, tag = Gui.TAG_FIGURA) #Zakaj ne dela z drugim tagom?
        elif i1==i1==i3==i4:
            self.plosca.create_rectangle(j1 * d, (i1+2) * d, (j4+1) * d, (i1+1) * d, width=5, outline = barva, tag = Gui.TAG_FIGURA)
        else:
            self.plosca.create_rectangle(j1 * d, (i1 + 1) * d, (j1 + 1) * d, (i1 + 2) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle(j2 * d, (i2 + 1) * d, (j2 + 1) * d, (i2 + 2) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle(j3 * d, (i3 + 1) * d, (j3 + 1) * d, (i3 + 2) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle(j4 * d, (i4 + 1) * d, (j4 + 1) * d, (i4 + 2) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)


#
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

        igralec = self.igra.na_potezi

        r = self.igra.povleci_potezo(p)
        self.stevec_polj = 0 #ta stevec šteje koliko polj v stolcpu je že zasedenih
        self.y = 6*Gui.VELIKOST_POLJA


        if r is None:
            # Poteza ni bila veljavna, nič se ni spremenilo
            pass
        else:
            if igralec == MODRI:
                self.narisi_modri(p)
            elif igralec == RDECI:
                self.narisi_rdeci(p)

            (zmagovalec, stirica) = r

            if zmagovalec == NI_KONEC:
                if igralec == MODRI:
                    self.napis.set("Na potezi je RDECI.")
                    self.modri.igraj()


                elif igralec == RDECI:
                    self.napis.set("Na potezi je MODRI.")
                    self.rdeci.igraj()


            else:
                # Igre je konec, koncaj
                self.koncaj_igro(zmagovalec, stirica)



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Štiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()





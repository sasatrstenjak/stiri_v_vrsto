import tkinter

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

        #narediva matriko z "vrdnostmi" stolpcev
        self.stolpci = []
        i= 0
        while i < 7:
            self.stolpci.append([0, 0, 0, 0, 0, 0])
            i +=1

        self.nova_igra()

    def nova_igra(self):
        self.plosca.delete(Gui.TAG_ZETON)
        self.stolpci = []
        i= 0
        while i < 7:
            self.stolpci.append([0, 0, 0, 0, 0, 0])
            i +=1


    def koncaj_igro(self):
        self.napis.set("Konec igre!")

    def zapri_okno(self, master):
        master.destroy()
    

    def narisi_polje(self):
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.plosca.create_line(0.02*d, d, 0.02*d, 7*d, tag = Gui.TAG_OKVIR)
        
        for i in range (1,9): #navpicne crte
            self.plosca.create_line(i*d, d, i*d, 7*d, tag = Gui.TAG_OKVIR)
        for j in range(2,8):#vodoravne crte
            self.plosca.create_line(0, j*d, 7*d, j*d, tag = Gui.TAG_OKVIR)

    def narisi_modri(self, p):
        #narise krogec v polje (i,j)
        x = p[0]*Gui.VELIKOST_POLJA
        #y = p[1]*Gui.VELIKOST_POLJA
        #y = 6*Gui.VELIKOST_POLJA #- 0.5*Gui.VELIKOST_POLJA
        sirina = 3
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1

        
        for i in self.stolpci[x//Gui.VELIKOST_POLJA]:
            if i!= 0:
                self.y-= Gui.VELIKOST_POLJA
                self.stevec +=1
            else:
                self.stolpci[x//Gui.VELIKOST_POLJA][self.stevec] = "M"
                self.plosca.create_oval(x+d1, self.y+d1, x+d2, self.y+d2, width=sirina, tag=Gui.TAG_ZETON, fill = "blue")
                break
                
        print (self.stolpci)
    
    def narisi_rdeci(self, p):
        #narise krogec v polje (i,j)
        x = p[0]*Gui.VELIKOST_POLJA
        #y = p[1]*Gui.VELIKOST_POLJA
        sirina = 3
        d1 = 5
        d2 = Gui.VELIKOST_POLJA - d1
        
        for i in self.stolpci[x//Gui.VELIKOST_POLJA]:
            if i!= 0:
                self.y-= Gui.VELIKOST_POLJA
                self.stevec +=1
            else:
                self.stolpci[x//Gui.VELIKOST_POLJA][self.stevec] = "R"
                self.plosca.create_oval(x+d1, self.y+d1, x+d2, self.y+d2, width=sirina, tag=Gui.TAG_ZETON, fill = "red")
                break
                
        print (self.stolpci)

        
    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // Gui.VELIKOST_POLJA
        j = event.y // Gui.VELIKOST_POLJA
        print ("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
        self.povleci_potezo((i,j))

    def povleci_potezo(self, p):
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        (i, j) = p
        # Da vidimo, ali se prav riše, včasih narišemo X in včasih O
        
        
        if (i + j) % 2 == 0:
            self.stevec = 0
            self.y = 6*Gui.VELIKOST_POLJA
            self.narisi_modri(p)
        else:
            self.stevec = 0
            self.y = 6*Gui.VELIKOST_POLJA
            self.narisi_rdeci(p)

        


    

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Štiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()





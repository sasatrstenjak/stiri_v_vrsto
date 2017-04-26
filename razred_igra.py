MODRI = "M"
RDECI = "R"
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == RDECI:
        return MODRI
    elif igralec == MODRI:
        return RDECI
    else:

        assert False, "neveljaven nasprotnik"

class Igra():
    def __init__(self):


        #sestavi se matrika z vrednostmi stolpcev
        #0 pomeni, da je polje prazno
        #Prvi element v seznamu (seznama) predstavlja najvišje polje v stolpcu
        self.stolpci = []
        i = 0
        while i < 7:
            self.stolpci.append([0, 0, 0, 0, 0, 0])
            i +=1

        self.na_potezi = MODRI #začne modri igralec
        
        self.zgodovina = []
        
        self.stirice = []
        #doda vse možne zmage po vseh stolpcih
        for i in range(7):
            for j in range (3):
                self.stirice.append([(i, j), (i, j+1), (i, j+2), (i, j+3)])

        #doda vse možne zmage po vseh vrsticah
        for j in range(6):
            for i in range(4):
                self.stirice.append([(i, j), (i+1, j),(i+2, j),(i+3, j)])

        #doda vse možne zmage po vseh diagonalah
        for i in range(4):
            for j in range(3):
                self.stirice.append([(i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3)])
                self.stirice.append([(i,j+3),(i+1,j+2),(i+2,j+1),(i+3,j)])

        
    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.stolpci[i][:] for i in range(7)]
        self.zgodovina.append((p, self.na_potezi))

        #print (p)

    def kopija(self):
        k = Igra()
        k.stolpci = [self.stolpci[i][:] for i in range(7)]
        k.na_potezi = self.na_potezi
        return k

    
    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.stolpci, self.na_potezi) = self.zgodovina.pop()

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez."""
        veljavne_poteze = []
        for i in range(7):
            for j in range(5, -1, -1):
                if self.stolpci[i][j] == 0:
                    veljavne_poteze.append((i, j))
                    break
        # print (veljavne_poteze)
        # print("Veljavne poteze: {}".format(veljavne_poteze))
        return veljavne_poteze

    # def stirice_ki_vsebujejo_kako_veljavno_potezo(self):
    #     self.stirice2 = []  # v tem sezanmu so vse možne štirice, ki vsebujejo kako veljavno potezo
    #     for polje in self.veljavne_poteze():
    #         for stirica in self.stirice:
    #             if polje in stirica:
    #                 self.stirice2.append(stirica)
    #         print (self.stirice2)
    #     return self.stirice2

    def povleci_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""

        (i, j) = p
        if self.stolpci[i][0] != 0 or (self.na_potezi == None):
             #neveljavna poteza
             return None
        if i < 0 or i > 6 or j < 0: #to zagotovi, da je klik izven igralnega polja neveljaven
            return None
        else:
            # print(i, j)
            self.shrani_pozicijo()
            j = 5
            while j>=0:
                if self.stolpci[i][j] == 0:
                    self.stolpci[i][j] = self.na_potezi
                    break
                j-=1
            (zmagovalec, stirica) = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
                pass
            else:
                # Igre je konec
                self.na_potezi = None
            return (zmagovalec, stirica)

    def stanje_igre(self): #TO JE TREBA ŠE DODELATI!!!
        """Ugotovi, kakšno je trenutno stanje igre. Vrne:
           - (MODRI, stirica), če je igre konec in je zmagal MODRI z dano zmagovalno stirico
           - (RDECI, stirica), če je igre konec in je zmagal RDECI z dano zmagovalno stirico
           - (NEODLOCENO, None), če je igre konec in je neodločeno
           - (NI_KONEC, None), če igre še ni konec
        """
        for stirica in self.stirice:
            [(i1,j1),(i2,j2),(i3,j3),(i4,j4)] = stirica
            p = self.stolpci[i1][j1]
            if p != 0 and p == self.stolpci[i2][j2] == self.stolpci[i3][j3] == self.stolpci[i4][j4]:
                # Našli smo zmagovalno stirico
                #self.Gui.plosca.create_line(i1*100 + 0.5*self.Gui.VELIKOST_POLJA, j1*100 + 0.5*self.Gui.VELIKOST_POLJA, i4*100 + 0.5*self.Gui.VELIKOST_POLJA, j4*100 + 0.5*self.Gui.VELIKOST_POLJA)
                return (p, (stirica[0], stirica[1], stirica[2], stirica[3]))
    
        # Ni zmagovalca, ali je igre konec?
        for i in range(7):
            for j in range(6):
                if self.stolpci[i][j] == 0:
                    # Našli smo prazno polje, igre ni konec
                    return (NI_KONEC, None)
                        
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)
             

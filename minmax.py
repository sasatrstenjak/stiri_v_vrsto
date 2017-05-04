import logging

from razred_igra import MODRI, RDECI, NEODLOCENO, NI_KONEC, nasprotnik

VELIKOST = 6

class Minimax:
    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_potezi
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 1000000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        # Slovar, ki pove, koliko so vredne posamezne štirke, kjer "(x,y) : v" pomeni:
        # če imamo v stirici x znakov igralca in y znakov nasprotnika (in 4-x-y praznih polj),
        # potem je taka trojka za self.jaz vredna v.
        # Štirke, ki se ne pojavljajo v slovarju, so vredne 0.
        vrednost_stirice = {
            (4, 0): Minimax.ZMAGA,
            (0, 4): -Minimax.ZMAGA,
            (3, 0): Minimax.ZMAGA // 100,
            (0, 3): -Minimax.ZMAGA // 100,
            (2, 0): Minimax.ZMAGA // 10000,
            (0, 2): -Minimax.ZMAGA // 10000,
            (1, 0): Minimax.ZMAGA // 100000,
            (0, 1): -Minimax.ZMAGA// 100000}
        vrednost = 0
        for t in self.igra.stirice:
            x = 0  # koliko jih imam jaz v štirici t
            y = 0  # koliko jih ima nasprotnik v štirici t
            for (i, j) in t:
                if self.igra.stolpci[i][j] == self.jaz:
                    x += 1
                elif self.igra.stolpci[i][j] == nasprotnik(self.jaz):
                    y += 1
            vrednost += vrednost_stirice.get((x, y), 0)
            # print("Stirica: {0} ima vrednost {1}".format(t, vrednost_stirice.get((x, y), 0)))
            # print('Vrednost pozicije: {}'.format(vrednost))
        return vrednost

    def minimax(self, globina, maksimiziramo):
        if self.prekinitev:
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)

        (zmagovalec, stirica) = self.igra.stanje_igre()
        if zmagovalec in (MODRI, RDECI, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    # print("Veljavne: {}".format(self.igra.veljavne_poteze()))
                    for p in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina - 1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"

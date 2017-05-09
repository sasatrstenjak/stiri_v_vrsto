import logging
from random import shuffle
from igra import MODRI, RDECI, NEODLOCENO, NI_KONEC, nasprotnik

class Alfabeta:
    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False  # ali moramo končati?
        self.igra = None  # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None  # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_potezi
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo
        # Funkcijo alfabeta kličemo z začetnima argumentoma
        # alfa = -Alfabeta.NESKONCNO (spodnja meja)
        # in beta = Alfabeta.NESKONCNO (zgornja meja)
        (poteza, vrednost) = self.alfabeta(
            self.globina, -Alfabeta.NESKONCNO, Alfabeta.NESKONCNO, True)
        self.jaz = None
        self.igra = None

        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("alfabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            return poteza

    # Vrednosti igre
    ZMAGA = 1000000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh štiric na plošči."""
        # Slovar, ki pove, koliko so vredne posamezne štirke, kjer "(x,y) : v" pomeni:
        # če imamo v štirki x znakov igralca in y znakov nasprotnika (in 4-x-y praznih polj),
        # potem je taka štirka za self.jaz vredna v.
        # Štirke, ki se ne pojavljajo v slovarju, so vredne 0.
        vrednost_stirice = {
            (4, 0): Alfabeta.ZMAGA,
            (0, 4): -Alfabeta.ZMAGA,
            (3, 0): Alfabeta.ZMAGA // 100,
            (0, 3): -Alfabeta.ZMAGA // 100,
            (2, 0): Alfabeta.ZMAGA // 10000,
            (0, 2): -Alfabeta.ZMAGA // 10000,
            (1, 0): Alfabeta.ZMAGA // 100000,
            (0, 1): -Alfabeta.ZMAGA // 100000}
        vrednost = 0
        for t in self.igra.stirice:
            x = 0  # Koliko jih imam jaz v štirici t
            y = 0  # Koliko jih ima nasprotnik v štirici t
            for (i, j) in t:
                if self.igra.stolpci[i][j] == self.jaz:
                    x += 1
                elif self.igra.stolpci[i][j] == nasprotnik(self.jaz):
                    y += 1
            vrednost += vrednost_stirice.get((x, y), 0)
        return vrednost

    def alfabeta(self, globina, alfa, beta, maksimiziramo):
        if self.prekinitev:
            logging.debug("Alfabeta prekinja, globina = {0}".format(globina))
            return (None, 0)

        (zmagovalec, stirica) = self.igra.stanje_igre()
        if zmagovalec in (MODRI, RDECI, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Alfabeta.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Alfabeta.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo alfabeta
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    veljavne_poteze = self.igra.veljavne_poteze()
                    shuffle(veljavne_poteze)
                    for p in veljavne_poteze:
                        self.igra.povleci_potezo(p)
                        vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > alfa:
                            alfa = vrednost
                            najboljsa_poteza = p
                        if alfa >= beta:    
                            break
                    return (najboljsa_poteza, alfa)
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    veljavne_poteze = self.igra.veljavne_poteze()
                    shuffle(veljavne_poteze)
                    for p in veljavne_poteze:
                        self.igra.povleci_potezo(p)
                        vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < beta:
                            beta = vrednost
                            najboljsa_poteza = p
                        if alfa >= beta:
                            break
                    return (najboljsa_poteza, beta)

                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
        else:
            assert False, "alfabeta: nedefinirano stanje igre"

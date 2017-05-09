# Štiri v vrsto
Prvi projekt pri predmetu Programiranje 2 - igrica štiri v vrsto. 

# Datoteke
Igrica sestoji iz 6 datotek:

- stiri_v_vrsto.py

     - Ta datoteka izriše igralno ploščo in poskrbi, da lahko začenmo igrati igrico. Ko se nam odpre okno, lahko v meniju možnosti izberemo način igre, tj. človek proti človeku, računalnik proti človeku (lahko izbiramo, ali naj računalnik igra po algoritmu minimax ali alfabeta), človek proti računalniku (lahko izbiramo, ali naj računalnik igra po algoritmu minimax ali alfabeta) ali pa računalnik proti računalniku (tudi tukaj lahko izbiramo, ali naj računalnik igra po algoritmu minimax ali alfabeta). Če se ne odločimo posebej za katero od možnosti, se bo odigrala igra človek proti računalniku (minimax), kjer bo človek modri igralec in računalnik rdeči. 
      - Igralec odigra potezo tako, da klikne na stolpec v keterega želi narisati žeton, ki se bo narisal v prvo prosto vrstico v želenem stolpcu. Igra se zaključi, ko ima eden od igralcev v nekem stolpcu, vrstici ali diagonali štiri zaporedne enake žetone. Takrat se bo zmagovalna štirica obkrožila z okvirjem in igre bo konec. Za novo igro uporabik klikne možnosti (zgoraj levo) in izbere vrsto igre, ki jo želi odigrati. Če ne želi več igrati, zapre igralno okno.

- igra.py

     - Ta datoteka skrbi za logiko igre. Ko uporabnik klikne na ploščo, se v igra.py pokliče vrsta funkcij; povleče se dana poteza, v matriko self.stolpci se zapiše kam je bila odigrana poteza in kdo jo je odigral, pogleda se stanje igre (ali že imamo zmagovalca, je igre konec ali ne),... 
      - Poleg tega se v datoteki ustvari tudi seznam vseh možnih zmagovalnih štiric in definira se nasprotnik od igralca. 

- clovek.py

      - Ta datoteka je potrebna za igralca človeka. Ko kliknemo na ploščo, se povleče poteza p.

- racunalnik.py

      - Ta datoteka je potrebna, da imamo lahko računalniškega igralca. Pokliče se funkcija minimax oz alfabeta, ki izračuna najboljšo potezo za računalniškega igralca, le-ta pa jo potem odigra. Uporabi se kopija igre, ki smo jo ustvarili v razredu Igra v datoteki igra.py.

- minmax.py

      - V tej datoteki je algoritem, ki ga potrebuje računalnik, da izračuna, kam bo odigral potezo. Vse možne zmagovalne štirice se najprej ovrednotijo, nato pa se algoritem rekurzivno pokliče do določene globine, ki jo lahko nastavimo na vrhu datoteke stiri_v_vrsto.py.
      - Računalnik solidno igra do globine vključno 4 (tudi 5 se še da počakati).

- alfabeta.py

      - V tej daoteki je izboljšan algoritem minimax, imenovan alfabeta, ki nam omogoča hitrejše igranje igrice na višji globini. Algoritem deluje tako, da ne analizira poteze, za katero ve, da je slabša od potez, ki jih je že analiziral. 
      - Tukaj lahko brez problema igramo do globine vključno 6, za 7 in več pa moramo že malo počakati.  





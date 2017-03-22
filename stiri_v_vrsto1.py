import tkinter

class Gui():
    TAG_ZETON = "zeton"
    TAG_OKVIR = "okvir"
    VELIKOST_POLJA = 80

    def __init__(self, master):
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        glavni_menu = tkinter.Menu(master)
        master.config(menu = glavni_menu)

        podmenu = tkinter.Menu(glavni_menu)
        podmenu.add_cascade(label = "Možnosti", menu = podmenu)
        podmenu.add_command(label = "Nova igra", command = self.nova_igra)

        self.plosca = tkinter.Canvas(master, width = 7*Gui.VELIKOST_POLJA, height = 7*Gui.VELIKOST_POLJA)
        self.plosca.grid(row = 1, column = 0)

        self.narisi_polje()
        
        #self.plosca.bind("<Button-1>", self.plosca_klik)

        self.napis = tkinter.StringVar(master, value = "Igra 4 v vrsto se je pričela!")
        tkinter.Label(master, textvariable = self.napis).grid(row = 0, column = 0)

        self.nova_igra()

    def nova_igra(self):
        self.plosca.delete(Gui.TAG_ZETON)

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

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Štiri v vrsto")
    aplikacija = Gui(root)
    root.mainloop()

        

        

from tkinter import *

class Environment:
    def __init__(self, ime, coverBonus, destructable):
        self.ime=ime
        self.coverBonus=coverBonus
        self.destructable=destructable
        return

    def opis(self, extended=False):
        if extended:
            tekst="It is a {}.".format(self.ime)
            if self.coverBonus:
                tekst += " It provides +{}AC cover bonus.".format(self.coverBonus)
            if self.destructable:
                tekst += " It can be destroyed or penetrated by certain weapons."
        else:
            tekst =self.ime
        return tekst

    def endTurn(self):
        return

    def endCombat(self):
        return

    def showDetails(self, parent):
        cbtext="Cover bonus: {}".format(self.coverBonus)
        coverBonus=Label(parent, text=cbtext)
        coverBonus.grid(row=1, column=0, columnspan=2)
        if self.destructable:
            desttext="It can be destroyed or penetrated by certain weapons."
        else:
            desttext = "It can NOT be destroyed or penetrated by weapons."
        destructable = Label(parent, text=desttext)
        destructable.grid(row=1, column=0, columnspan=2)
        return

    def showCombatScreen(self, parent):
        desc = Label(parent, text=self.opis(extended=True))
        desc.grid(row=0, column=0, padx=5, pady=5)
        return

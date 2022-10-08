from tkinter import *

from EnemyMech import EnemyMech
from EnemyPilot import EnemyPilot
from PlayerMech import PlayerMech
from PlayerPilot import PlayerPilot


class Entitet:
    def __init__(self,actor, representation=None):
        self.actor=actor
        self.representation=representation
        # 0 - neutral, 1 - player, 2 - ally, 3 - enemy
        self.faction=0
        self.alive=False
        self.setDerived()
        return

    def setDerived(self):
        if isinstance(self.actor, EnemyMech):
            self.alive=True
            if self.actor.allyFlag:
                self.faction=2
                self.representation=r"res/mechBlue.png"
            else:
                self.faction=3
                self.representation = r"res/mechRed.png"
        elif isinstance(self.actor, EnemyPilot):
            self.alive=True
            if self.actor.allyFlag:
                self.faction=2
                self.representation=r"res/pilotBlue.png"
            else:
                self.faction=3
                self.representation = r"res/pilotRed.png"
        elif isinstance(self.actor, PlayerPilot):
            self.alive=True
            self.faction=1
            self.representation=r"res/pilotGreen.png"
        elif isinstance(self.actor, PlayerMech):
            self.alive = True
            self.faction=1
            self.representation = r"res/mechGreen.png"
        else:
            self.faction=0
            self.alive=False
        return

    def endTurn(self):
        if self.alive:
            self.actor.endTurn()
        else:
            pass
        return

    def endCombat(self):
        if self.alive:
            self.actor.endCombat()
        else:
            pass
        return

    def showDetails(self, parent):
        def del_func():
            delete['state']="disabled"
            self.actor.delete()

        tkimage = PhotoImage(file=self.representation)
        profilePic = Label(parent, image=tkimage)
        profilePic.image = tkimage
        profilePic.grid(row=0, column=0, padx=10, pady=10)
        opisLabel = Label(parent, text=self.actor.opis(extended=True), wraplength=500, justify=LEFT)
        opisLabel.grid(row=0, column=1, padx=10, pady=10)
        affiliationText="Affiliation: "
        if self.faction==0:
            affiliationText+="Neutral"
        elif self.faction==1:
            affiliationText+="Player Character"
        elif self.faction==2:
            affiliationText+="Allied Character"
        elif self.faction==3:
            affiliationText+="Enemy"
        affiliation=Label(parent, text=affiliationText)
        affiliation.grid(row=0, column=2)
        delete = Button(parent, text="DELETE THIS ENTITY", command=lambda: del_func())
        delete.grid(row=0, column=3, padx=5, pady=5)
        deleteWarning = Label(parent, text="Warning! This will permanently delete this entity!", wraplength=300, justify=LEFT,
                            font=("Arial", 10, "bold"))
        deleteWarning.grid(row=0, column=4, columnspan=2, padx=5, pady=5)
        actorFrame=Frame(parent)
        actorFrame.grid(row=1, column=0, columnspan=5)
        self.actor.showDetails(actorFrame)
        return

    def showCombatScreen(self, parent):
        frame=Frame(parent, width=1000, height=1000)
        frame.grid(row=0, column=0)
        self.actor.showCombatScreen(frame)
        return

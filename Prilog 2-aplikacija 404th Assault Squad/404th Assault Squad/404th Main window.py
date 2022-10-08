import copy
import pickle as pickle
from random import *
from tkinter.ttk import Notebook, Combobox

import podatci as podatci
from Entitet import *


class GlavniProzor(Frame):
    ikone = [r"res/deleteCell.png", r"res/mechGreen.png", r"res/mechBlue.png", r"res/mechRed.png",
             r"res/pilotGreen.png", r"res/pilotBlue.png", r"res/pilotRed.png", r"res/postTree.png", r"res/postMetal.png", r"res/wallStone.png"]
    savedEMs = "data/enemy_mechs.dat"
    savedEPs = "data/enemy_pilots.dat"
    savedPMs = "data/player_mechs.dat"
    savedPPs = "data/player_pilots.dat"
    savedDEPLOYED = "data/DEPLOYED.dat"

    def __init__(self, prozor):
        self.selectedEntitetIndex = None
        self.editorEntiteti = []
        self.tkImages = []
        self.aktivnaPolja = []
        self.aktivniEntiteti = []
        self.combatScreenWindows=[]
        self.coreSlot = None
        self.lLegSlot = None
        self.rLegSlot = None
        self.core2Slot = None
        self.core1Slot = None
        self.body4Slot = None
        self.body3Slot = None
        self.body2Slot = None
        self.body1Slot = None
        self.lShSlot = None
        self.rShSlot = None
        self.lHaSlot = None
        self.rHaSlot = None
        self.helmetSlot=None
        self.chestSlot=None
        self.backSlot=None
        self.suitlegsSlot=None
        self.omniSlot=None
        self.extraSlot=None
        self.weaponSlot=None
        self.prozor = prozor
        self.prozor.title("404th Assault Squad")
        super().__init__(self.prozor)
        self.grid(rows=5, columns=5)
        self.prozor.minsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.prozor.protocol('WM_DELETE_WINDOW', self.onDestroyCustom)
        self.loadDataOnStart()
        self.Kreirajsucelje()
        return

    def Kreirajsucelje(self):

        w = int(self.winfo_screenwidth() * 0.55)
        h = int(self.winfo_screenheight() * 0.85)

        self.playFrame = Frame(self)
        self.playFrame.grid(row=0, column=0, padx=10, pady=10)
        self.playCanvas = Canvas(self.playFrame, width=w, height=h)
        self.playCanvas.grid(column=0, row=0, sticky="nw")
        self.scrollableFrame = Frame(self.playCanvas)
        scrollbarNS = Scrollbar(self.playFrame, orient=VERTICAL, command=self.playCanvas.yview)
        scrollbarEW = Scrollbar(self.playFrame, orient=HORIZONTAL, command=self.playCanvas.xview)
        self.scrollableFrame.bind("<Configure>",
                                  lambda event: self.playCanvas.configure(scrollregion=self.playCanvas.bbox("all")))
        self.playCanvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        self.playCanvas.configure(yscrollcommand=scrollbarNS.set)
        self.playCanvas.configure(xscrollcommand=scrollbarEW.set)

        scrollbarNS.grid(row=0, column=1, sticky="nes")
        scrollbarEW.grid(row=1, column=0, sticky="wse")

        self.editorFrame = Frame(self)
        self.editorFrame.grid(row=0, column=1, padx=10, pady=10)
        self.createEditorUI()

        ##################    MENUS

        menuBar = Menu(self.prozor)
        playAreaMenu = Menu(menuBar, tearoff=0)
        generateMenu = Menu(playAreaMenu, tearoff=0)
        generateMenu.add_command(label="5 x 7", command=lambda: self.generatePlayArea(self.scrollableFrame, 5, 7))
        generateMenu.add_command(label="7 x 10", command=lambda: self.generatePlayArea(self.scrollableFrame, 7, 10))
        generateMenu.add_command(label="10 x 15", command=lambda: self.generatePlayArea(self.scrollableFrame, 10, 15))
        generateMenu.add_command(label="15 x 20", command=lambda: self.generatePlayArea(self.scrollableFrame, 15, 20))
        generateMenu.add_command(label="Custom size", command=lambda: self.customPlayAreaWindow(self.scrollableFrame))
        playAreaMenu.add_cascade(label="Generate new...", menu=generateMenu)
        playAreaMenu.add_command(label="Clear", command=self.clearPlayArea)
        createMenu = Menu(menuBar, tearoff=0)
        createPlayerMenu = Menu(createMenu, tearoff=0)
        createPlayerMenu.add_command(label="Create player pilot", command=lambda: self.createPilotWindow("pp"))
        createPlayerMenu.add_command(label="Create player mech", command=lambda: self.createMechWindow("pm"))
        createMenu.add_cascade(label="Create player...", menu=createPlayerMenu)
        createNPCMenu = Menu(createMenu, tearoff=0)
        createNPCMenu.add_command(label="Create NPC pilot", command=lambda: self.createPilotWindow("ep"))
        createNPCMenu.add_command(label="Create NPC mech", command=lambda: self.createMechWindow("em"))
        createMenu.add_cascade(label="Create NPC...", menu=createNPCMenu)
        createMenu.add_command(label="Show a list of all actors", command=self.createListWindow)
        extrasMenu=Menu(menuBar, tearoff=0)
        extrasMenu.add_command(label="Dice", command=self.createDiceWindow)
        extrasMenu.add_command(label="Credits", command=self.credits)
        menuBar.add_cascade(label="Play area", menu=playAreaMenu)
        menuBar.add_cascade(label="Actors", menu=createMenu)
        menuBar.add_cascade(label="Extras", menu=extrasMenu)
        self.prozor.config(menu=menuBar)

        return

    ################# GENERATE PLAY AREA

    def customPlayAreaWindow(self, parent):
        def create_f():
            self.generatePlayArea(parent, int(wEntry.get()), int(hEntry.get()))
            dialog.destroy()

        dialog=Toplevel(self)
        dialog.geometry("200x130")
        dialog.title("Generate custom Play area")
        width=Label(dialog, text="Width: ")
        width.grid(row=0, column=0, padx=10, pady=10)
        wEntry=Entry(dialog, exportselection=0, width=10)
        wEntry.grid(row=0, column=1, padx=10, pady=10)
        height=Label(dialog, text="Height: ")
        height.grid(row=1, column=0, padx=10, pady=10)
        hEntry = Entry(dialog, exportselection=0, width=10)
        hEntry.grid(row=1, column=1, padx=10, pady=10)
        create=Button(dialog, text="Generate", command=create_f)
        create.grid(row=2, column=0, padx=10, pady=10)
        cancel = Button(dialog, text="Cancel", command=dialog.destroy)
        cancel.grid(row=2, column=1, padx=10, pady=10)

    def generatePlayArea(self, parent, x, y):
        for i in range(y):
            for j in range(x):
                frame = Frame(parent, bd=2, relief=SOLID)
                frame.columnconfigure(0, minsize=5)
                frame.columnconfigure(1, minsize=5)
                frame.columnconfigure(2, minsize=5)
                frame.grid(row=i + 1, column=j + 1, sticky="EWNS")
                self.createPolje(frame)

        self.aktivnaPolja = self.izdvojiTipove(self.scrollableFrame, Label, lambda x: x.cget('image'))
        return

    def createPolje(self, parent):
        for i in range(3):
            for j in range(3):
                a = Label(parent, text=" ", width=5, height=2, borderwidth=2, relief="groove")
                a.grid(column=j, row=i)
        return

    def clearPlayArea(self):
        self.scrollableFrame.destroy()
        self.scrollableFrame = Frame(self.playCanvas)
        self.scrollableFrame.bind("<Configure>",
                                  lambda event: self.playCanvas.configure(scrollregion=self.playCanvas.bbox("all")))
        self.playCanvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        return

    ############### EXTRAS

    def createDiceWindow(self):
        def roll():
            rollres=[]
            rollres2=[]
            numberOfDie=int(dammount.get())

            dice=int(dtype.get())
            for i in range(numberOfDie):
                roll=randint(1,dice)
                rollres.append(roll)
                roll = randint(1, dice)
                rollres2.append(roll)

            result['text'] = "Roll: "
            result2['text'] = "Adv./Disadv. roll: "

            for i in range(numberOfDie):
                roll=rollres[i]
                result['text'] += "{} ".format(roll)
                roll = rollres2[i]
                result2['text'] += "{} ".format(roll)

            result['text'] += "= {}".format(sum(rollres))
            result2['text'] += "= {}".format(sum(rollres2))


        dw=Toplevel(self)
        dammount=Entry(dw, width=5)
        dammount.insert(0,1)
        dammount.grid(row=0, column=0, padx=5, pady=10)
        dlbl=Label(dw, text="d", justify=CENTER)
        dlbl.grid(row=0, column=1, padx=5, pady=10)
        dtype = Entry(dw, width=5)
        dtype.insert(0,20)
        dtype.grid(row=0, column=2, padx=5, pady=10)

        result=Label(dw, text="")
        result.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
        result2 = Label(dw, text="")
        result2.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        roll = Button(dw, text="ROLL", command=roll)
        roll.grid(row=0, column=3, padx=10, pady=10)
        return

    def credits(self):
        creds=Toplevel(self)
        creds.geometry("400x400")
        label=Label(creds, text="404th Assault Squad is a homebrew table-top role playing game developed by Antonio "
                                "Peršin.\nThis aplication was designed as a board/table replacement to accomodate "
                                "playing with players online and offline.\n\n\nVersion: 1.1.4 (26/8/2021)\nZagreb "
                                "University of Applied Sciences, Year 2021", justify=LEFT, wraplength=330,
                    font=("Arial",14))
        label.grid(row=0, column=0, padx=20, pady=20)
        return

    ############### EDITOR UI

    def izdvojiTipove(self, parent, tip, uvijet):
        # 2 deep child per type
        rez = []
        tmpDjeca = parent.winfo_children()
        if tmpDjeca:
            for item in tmpDjeca:
                if isinstance(item, tip) and uvijet(item):
                    rez.append(item)
                tmpUnuci = item.winfo_children()
                if tmpUnuci:
                    for item2 in tmpUnuci:
                        if isinstance(item2, tip) and uvijet(item2):
                            rez.append(item2)
        return rez

    def createEditorUI(self):
        def deleteFromDeployed(event):
            index = event.widget['text']
            podatci.DEPLOYED.pop(index)
            self.createEditorUI()

        def endCMBT():
            for entitet in self.editorEntiteti:
                entitet.actor.endCombat()
                print("Mech {} core status {}%".format(entitet.actor.opis(), entitet.actor.core.percent))

        def endTRN():
            for entitet in self.editorEntiteti:
                entitet.actor.endTurn()

        w = int(self.winfo_screenwidth() * 0.35)
        ws=int(self.winfo_screenwidth() * 0.34)
        h = int(self.winfo_screenheight() * 0.75)

        notebook=Notebook(self.editorFrame, height=h, width=w)
        notebook.grid(row=0,column=0, columnspan=5)
        # tabs=[("Player Pilots", podatci.PLAYER_PILOTS), ("Player Mechs", podatci.PLAYER_MECHS), ("Ally Pilots", podatci.ENEMY_PILOTS), ("Ally Mechs", podatci.ENEMY_MECHS), ("Enemy Pilots", podatci.ENEMY_PILOTS), ("Enemy Mechs", podatci.ENEMY_MECHS)]
        #
        # frames = [Frame(notebook) for _ in range(len(tabs))]
        # for i in range(len(tabs)):
        #     tab = tabs[i]
        #     for elem in tab[1]:
        #         entitet = Entitet(elem)
        #         tkimage = PhotoImage(file=entitet.representation)
        #         ind = (entitet.faction-1) * 2 + 1 - i % 2
        #         imageLabel = Label(frames[ind], image=tkimage)
        #         imageLabel.image = tkimage
        #         imageLabel.grid(row=i, column=0)
        #         imageLabel.bind("<Button-1>", self.selectUnitToPlace)
        #         textLabel = Label(frames[ind], text=elem.opis())
        #         textLabel.grid(row=i, column=1)
        #
        # for i in range(len(frames)):
        #     notebook.add(frames[i], text=tabs[i][0])

        tab=Frame(notebook)
        tabCanvas = Canvas(tab, width=ws, height=h)
        tab.grid(row=0, column=0, padx=10, pady=10)
        tabCanvas.grid(column=0, row=0, sticky="nw")
        tabFrame = Frame(tabCanvas)
        scrollbarNS = Scrollbar(tab, orient=VERTICAL, command=tabCanvas.yview)
        tabFrame.bind("<Configure>",
                      lambda event: tabCanvas.configure(scrollregion=tabCanvas.bbox("all")))
        tabCanvas.create_window((0, 0), window=tabFrame, anchor="nw")
        tabCanvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.PLAYER_PILOTS)):
            entitet = Entitet(podatci.PLAYER_PILOTS[i])
            tkimage = PhotoImage(file=entitet.representation)
            imageLabel = Label(tabFrame, image=tkimage, text=i)
            imageLabel.image = tkimage
            imageLabel.grid(row=i, column=0)
            imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.PLAYER_PILOTS))
            imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.PLAYER_PILOTS))
            textLabel = Label(tabFrame, text=entitet.actor.opis())
            textLabel.grid(row=i, column=1)
        notebook.add(tab, text="Player Pilots")

        tab1 = Frame(notebook)
        tab1Canvas = Canvas(tab1, width=ws, height=h)
        tab1.grid(row=0, column=0, padx=10, pady=10)
        tab1Canvas.grid(column=0, row=0, sticky="nw")
        tab1Frame = Frame(tab1Canvas)
        scrollbarNS = Scrollbar(tab1, orient=VERTICAL, command=tab1Canvas.yview)
        tab1Frame.bind("<Configure>",
                      lambda event: tab1Canvas.configure(scrollregion=tab1Canvas.bbox("all")))
        tab1Canvas.create_window((0, 0), window=tab1Frame, anchor="nw")
        tab1Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.PLAYER_MECHS)):
            entitet = Entitet(podatci.PLAYER_MECHS[i])
            tkimage = PhotoImage(file=entitet.representation)
            imageLabel = Label(tab1Frame, image=tkimage, text=i)
            imageLabel.image = tkimage
            imageLabel.grid(row=i, column=0)
            imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.PLAYER_MECHS))
            imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.PLAYER_MECHS))
            textLabel = Label(tab1Frame, text=entitet.actor.opis())
            textLabel.grid(row=i, column=1)
        notebook.add(tab1, text="Player Mechs")

        tab2 = Frame(notebook)
        tab2Canvas = Canvas(tab2, width=ws, height=h)
        tab2.grid(row=0, column=0, padx=10, pady=10)
        tab2Canvas.grid(column=0, row=0, sticky="nw")
        tab2Frame = Frame(tab2Canvas)
        scrollbarNS = Scrollbar(tab2, orient=VERTICAL, command=tab2Canvas.yview)
        tab2Frame.bind("<Configure>",
                      lambda event: tab2Canvas.configure(scrollregion=tab2Canvas.bbox("all")))
        tab2Canvas.create_window((0, 0), window=tab2Frame, anchor="nw")
        tab2Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        description=Label(tab2Frame, text="This tab contains Player Mechs currently used by the squad. If the squad "
                                         "finnishes an encounter with one of their Mechs still present, that Mech's "
                                         "statistics will be kept here. Placing a Mech from \"Player Mechs\" tab will "
                                         "place a freshly called one (with full HP and ammo).\nTo delete mechs from "
                                         "this tab, once they die, use RMB.", justify=LEFT, wraplength=600)
        description.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        for i in range(len(podatci.DEPLOYED)):
            entitet = podatci.DEPLOYED[i]
            tkimage = PhotoImage(file=entitet.representation)
            imageLabel = Label(tab2Frame, image=tkimage, text=i)
            imageLabel.image = tkimage
            imageLabel.grid(row=i+1, column=0)
            imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.DEPLOYED))
            imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.DEPLOYED))
            imageLabel.bind("<Button-3>", lambda e: deleteFromDeployed(e))
            textLabel = Label(tab2Frame, text=entitet.actor.opis())
            textLabel.grid(row=i+1, column=1)
        notebook.add(tab2, text="DEPLOYED Player Mechs")

        tab3 = Frame(notebook)
        tab3Canvas = Canvas(tab3, width=ws, height=h)
        tab3.grid(row=0, column=0, padx=10, pady=10)
        tab3Canvas.grid(column=0, row=0, sticky="nw")
        tab3Frame = Frame(tab3Canvas)
        scrollbarNS = Scrollbar(tab3, orient=VERTICAL, command=tab3Canvas.yview)
        tab3Frame.bind("<Configure>",
                      lambda event: tab3Canvas.configure(scrollregion=tab3Canvas.bbox("all")))
        tab3Canvas.create_window((0, 0), window=tab3Frame, anchor="nw")
        tab3Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.ENEMY_PILOTS)):
            entitet = Entitet(podatci.ENEMY_PILOTS[i])
            if entitet.faction == 2:
                tkimage = PhotoImage(file=entitet.representation)
                imageLabel = Label(tab3Frame, image=tkimage, text=i)
                imageLabel.image = tkimage
                imageLabel.grid(row=i, column=0)
                imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.ENEMY_PILOTS))
                imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENEMY_PILOTS))
                textLabel = Label(tab3Frame, text=entitet.actor.opis())
                textLabel.grid(row=i, column=1)
        notebook.add(tab3, text="Ally Pilots")

        tab4 = Frame(notebook)
        tab4Canvas = Canvas(tab4, width=ws, height=h)
        tab4.grid(row=0, column=0, padx=10, pady=10)
        tab4Canvas.grid(column=0, row=0, sticky="nw")
        tab4Frame = Frame(tab4Canvas)
        scrollbarNS = Scrollbar(tab4, orient=VERTICAL, command=tab4Canvas.yview)
        tab4Frame.bind("<Configure>",
                      lambda event: tab4Canvas.configure(scrollregion=tab4Canvas.bbox("all")))
        tab4Canvas.create_window((0, 0), window=tab4Frame, anchor="nw")
        tab4Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.ENEMY_MECHS)):
            entitet = Entitet(podatci.ENEMY_MECHS[i])
            if entitet.faction == 2:
                tkimage = PhotoImage(file=entitet.representation)
                imageLabel = Label(tab4Frame, image=tkimage, text=i)
                imageLabel.image = tkimage
                imageLabel.grid(row=i, column=0)
                imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.ENEMY_MECHS))
                imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENEMY_MECHS))
                textLabel = Label(tab4Frame, text=entitet.actor.opis())
                textLabel.grid(row=i, column=1)
        notebook.add(tab4, text="Ally Mechs")

        tab5 = Frame(notebook)
        tab5Canvas = Canvas(tab5, width=ws, height=h)
        tab5.grid(row=0, column=0, padx=10, pady=10)
        tab5Canvas.grid(column=0, row=0, sticky="nw")
        tab5Frame = Frame(tab5Canvas)
        scrollbarNS = Scrollbar(tab5, orient=VERTICAL, command=tab5Canvas.yview)
        tab5Frame.bind("<Configure>",
                      lambda event: tab5Canvas.configure(scrollregion=tab5Canvas.bbox("all")))
        tab5Canvas.create_window((0, 0), window=tab5Frame, anchor="nw")
        tab5Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.ENEMY_PILOTS)):
            entitet = Entitet(podatci.ENEMY_PILOTS[i])
            if entitet.faction == 3:
                tkimage = PhotoImage(file=entitet.representation)
                imageLabel = Label(tab5Frame, image=tkimage, text=i)
                imageLabel.image = tkimage
                imageLabel.grid(row=i, column=0)
                imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.ENEMY_PILOTS))
                imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENEMY_PILOTS))
                textLabel = Label(tab5Frame, text=entitet.actor.opis())
                textLabel.grid(row=i, column=1)
        notebook.add(tab5, text="Enemy Pilots")

        tab6 = Frame(notebook)
        tab6Canvas = Canvas(tab6, width=ws, height=h)
        tab6.grid(row=0, column=0, padx=10, pady=10)
        tab6Canvas.grid(column=0, row=0, sticky="nw")
        tab6Frame = Frame(tab6Canvas)
        scrollbarNS = Scrollbar(tab6, orient=VERTICAL, command=tab6Canvas.yview)
        tab6Frame.bind("<Configure>",
                      lambda event: tab6Canvas.configure(scrollregion=tab6Canvas.bbox("all")))
        tab6Canvas.create_window((0, 0), window=tab6Frame, anchor="nw")
        tab6Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.ENEMY_MECHS)):
            entitet = Entitet(podatci.ENEMY_MECHS[i])
            if entitet.faction == 3:
                tkimage = PhotoImage(file=entitet.representation)
                imageLabel = Label(tab6Frame, image=tkimage, text=i)
                imageLabel.image = tkimage
                imageLabel.grid(row=i, column=0)
                imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.ENEMY_MECHS))
                imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENEMY_MECHS))
                textLabel = Label(tab6Frame, text=entitet.actor.opis())
                textLabel.grid(row=i, column=1)
        notebook.add(tab6, text="Enemy Mechs")

        tab7 = Frame(notebook)
        tab7Canvas = Canvas(tab7, width=ws, height=h)
        tab7.grid(row=0, column=0, padx=10, pady=10)
        tab7Canvas.grid(column=0, row=0, sticky="nw")
        tab7Frame = Frame(tab7Canvas)
        scrollbarNS = Scrollbar(tab7, orient=VERTICAL, command=tab7Canvas.yview)
        tab7Frame.bind("<Configure>",
                      lambda event: tab7Canvas.configure(scrollregion=tab7Canvas.bbox("all")))
        tab7Canvas.create_window((0, 0), window=tab7Frame, anchor="nw")
        tab7Canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")
        for i in range(len(podatci.ENVIRONMENT)):
            entitet=podatci.ENVIRONMENT[i]
            tkimage = PhotoImage(file=entitet.representation)
            imageLabel = Label(tab7Frame, image=tkimage, text=i)
            imageLabel.image = tkimage
            imageLabel.grid(row=i, column=0)
            imageLabel.bind("<Button-1>", lambda e: self.selectUnitToPlace(e, podatci.ENVIRONMENT))
            imageLabel.bind("<Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENVIRONMENT))
            textLabel = Label(tab7Frame, text=entitet.actor.opis())
            textLabel.grid(row=i, column=1)
        notebook.add(tab7, text="Environment")

        endTrnBtn = Button(self.editorFrame, text="TURN END", command=endTRN, width=25, height=2, font=("Arial",15,"bold"))
        endTrnBtn.grid(row=1, column=0, padx=10, pady=10)

        endCmbtBtn = Button(self.editorFrame, text="COMBAT END", command=endCMBT, width=25, height=2, font=("Arial",15,"bold"))
        endCmbtBtn.grid(row=1, column=1, padx=10, pady=10)

        return

        ###################### BOARD FUNCTIONALITY

    def selectUnitToPlace(self, event, lista):
        index=event.widget['text']
        nesto=lista[index]
        if isinstance(nesto, Entitet):
            entitet=nesto
        elif isinstance(nesto, (EnemyPilot, EnemyMech)):
            nesto=copy.deepcopy(nesto)
            entitet=Entitet(nesto)
        elif isinstance(nesto, PlayerMech):
            nesto=copy.deepcopy(nesto)
            entitet = Entitet(nesto)
            podatci.DEPLOYED.append(entitet)
        else:
            entitet = Entitet(nesto)
        self.editorEntiteti.append(entitet)
        self.selectedEntitetIndex = self.editorEntiteti.index(entitet)
        print("placing {} on index {}".format(entitet.actor.opis(), self.selectedEntitetIndex))
        self.aktivnaPolja = self.izdvojiTipove(self.scrollableFrame, Label, lambda _: True)
        for label in self.aktivnaPolja:
            label.bind("<Button-1>", lambda e: self.placeUnit(e, entitet))
        return

    def placeUnit(self, event, entitet):
        if self.selectedEntitetIndex is not None:
            wid=event.widget
            tkimage = PhotoImage(file=entitet.representation)
            wid.configure(width=0)
            wid.configure(height=0)
            wid.configure(image=tkimage)
            wid.config(text=self.selectedEntitetIndex)
            wid.image = tkimage
            wid.bind("<Button-2>", lambda e: self.createCombatScreen(e))
            wid.bind("<Control-Button-2>", lambda e: self.createDetailsWindow(e, entitet))
            wid.bind("<Button-3>", self.moveUnit)

            self.createEditorUI()
        return

    def moveUnit(self, event):
        self.selectedEntitetIndex=int(event.widget['text'])
        print("Selected entity index {}".format(self.selectedEntitetIndex))
        entitet=self.editorEntiteti[self.selectedEntitetIndex]
        event.widget.config(image='')
        event.widget.config(text=' ')
        event.widget.configure(width=5)
        event.widget.configure(height=2)

        self.aktivnaPolja = self.izdvojiTipove(self.scrollableFrame, Label, lambda _: True)
        for label in self.aktivnaPolja:
            label.bind("<Button-1>", lambda e: self.placeUnit(e, entitet))
        return

    def createDetailsWindow(self, event, target):
        detailsWindow=Toplevel(self)
        if isinstance(target, list):
            index = event.widget['text']
            if isinstance(target[index], Entitet):
                entitet = target[index]
            else:
                entitet = Entitet(target[index])
        else:
            entitet=target
        detailsWindow.title(entitet.actor.opis())
        detailsWindow.protocol('WM_DELETE_WINDOW', lambda: self.onDestroyCustomChild(detailsWindow))
        entitet.showDetails(detailsWindow)
        return

    def createCombatScreen(self, event):
        self.selectedEntitetIndex = event.widget['text']
        entitet = self.editorEntiteti[self.selectedEntitetIndex]
        if entitet:
            print("selected entity {}".format(entitet.actor.opis()))
            combatWindow=Toplevel(self, width=1000, height=1000)
            combatWindow.title(entitet.actor.opis())
            combatWindow.protocol('WM_DELETE_WINDOW', lambda: self.onDestroyCustomChild(combatWindow))
            for old in self.combatScreenWindows:
                if old[1]==entitet:
                    old[0].destroy()
                    self.combatScreenWindows.remove(old)
            self.combatScreenWindows.append((combatWindow,entitet))
            entitet.showCombatScreen(combatWindow)
        else:
            print("No entity to show combat screen for.")
        return

    ################# ACTOR CREATION WINDOWS

    def createMechWindow(self, flag):
        emw = Toplevel(self)
        emw.protocol('WM_DELETE_WINDOW', lambda: self.onDestroyCustomChild(emw))
        if flag == "em":
            emw.title("Create NPC mech preset")
        elif flag == "pm":
            emw.title("Create player mech preset")
        ws = emw.winfo_screenwidth()
        hs = emw.winfo_screenheight()

        emw.update()
        canvas = Canvas(emw, width=ws, height=hs)
        canvas.grid(row=0, column=0)

        armList = [x for x in podatci.MECH_WEAPONS if "arm weapon" in x.slot]
        shoulderList = [x for x in podatci.MECH_WEAPONS if "shoulder" in x.slot]
        shoulderList.extend([x for x in podatci.MODULES if "shoulder" in x.slot])
        bodyList = [x for x in podatci.MODULES if "body" in x.slot]
        coreModList = [x for x in podatci.MODULES if "core" in x.slot]
        coreList = podatci.CORES
        legList = [x for x in podatci.MODULES if "leg" in x.slot]

        if flag == "em":
            saveBtn = Button(canvas, text="Save NPC Mech preset", height=3, state="disabled",
                             command=lambda: self.saveNPCM(tier.get(), archetype.get(), action.get(),
                                                           self.rHaSlot, self.lHaSlot, self.rShSlot,
                                                           self.lShSlot, self.body1Slot, self.body2Slot, self.body3Slot,
                                                           self.body4Slot,
                                                           self.core1Slot, self.core2Slot, self.coreSlot, self.rLegSlot,
                                                           self.lLegSlot, allyFlag.get()))
            saveBtn.grid(row=11, column=3, columnspan=2, padx=10, pady=10)

            allyFlag=IntVar(canvas)
            ally=Checkbutton(canvas, text="Create this NPC as an ally", variable=allyFlag)
            ally.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

            tierTxt = Label(canvas, text="Enemy Tier:", width=25, height=3)
            tierTxt.grid(row=0, column=1, padx=10, pady=10)
            tier = Entry(canvas, exportselection=0, width=25)
            tier.insert(0,int(1))
            tier.grid(row=1, column=1, padx=10, pady=10)

            archetypeTxt = Label(canvas, text="Enemy Archetype:", width=25, height=3)
            archetypeTxt.grid(row=0, column=2, padx=10, pady=10)
            archetype = Entry(canvas, exportselection=0, width=25)
            archetype.bind("<KeyRelease>", lambda e: self.enableWidget(e.widget.get(), saveBtn))
            archetype.grid(row=1, column=2, padx=10, pady=10)

            actionTxt = Label(canvas, text="Enemy actions per turn:\n(format as: XMove XAtt XAct)", width=25, height=3)
            actionTxt.grid(row=0, column=3, padx=10, pady=10)
            action = Entry(canvas, exportselection=0, width=25)
            action.insert(0, "0Move 0Att 0Act")
            action.grid(row=1, column=3, padx=10, pady=10)

        elif flag == "pm":
            saveBtn = Button(canvas, text="Save player Mech preset", height=3, state="disabled",
                             command=lambda: self.savePCM(ime.get(), self.rHaSlot, self.lHaSlot, self.rShSlot,
                                                          self.lShSlot,
                                                          self.body1Slot, self.body2Slot, self.body3Slot,
                                                          self.body4Slot,
                                                          self.core1Slot, self.core2Slot, self.coreSlot, self.rLegSlot,
                                                          self.lLegSlot))
            saveBtn.grid(row=11, column=3, columnspan=2, padx=10, pady=10)

            imeTxt = Label(canvas, text="Mech name:", width=25, height=3)
            imeTxt.grid(row=0, column=1, padx=10, pady=10)
            ime = Entry(canvas, exportselection=0, width=25)
            ime.bind("<KeyRelease>", lambda e: self.enableWidget(e.widget.get(), saveBtn))
            ime.grid(row=1, column=1, padx=10, pady=10)

        rHaTxt = Label(canvas, text="Right Hand slot:", width=25, height=3)
        rHaTxt.grid(row=5, column=0, padx=10, pady=10)
        rHaPH = StringVar(canvas)
        rHa = Combobox(canvas, textvariable=rHaPH, state="readonly", width=25)
        tmpVals = [x.ime for x in armList]+[""]
        rHa['values'] = tmpVals
        rHa.grid(row=6, column=0, padx=10, pady=10)
        rHa.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rHaPH, armList, "rHa"))

        lHaTxt = Label(canvas, text="Left Hand slot:", width=25, height=3)
        lHaTxt.grid(row=5, column=4, padx=10, pady=10)
        lHaPH = StringVar(canvas)
        lHa = Combobox(canvas, textvariable=lHaPH, state="readonly", width=25)
        lHa['values'] = tmpVals
        lHa.grid(row=6, column=4, padx=10, pady=10)
        lHa.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lHaPH, armList, "lHa"))

        rShTxt = Label(canvas, text="Right Shoulder slot:", width=25, height=3)
        rShTxt.grid(row=2, column=0, padx=10, pady=10)
        rShPH = StringVar(canvas)
        rSh = Combobox(canvas, textvariable=rShPH, state="readonly", width=25)
        tmpVals = [x.ime for x in shoulderList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        rSh['values'] = tmpVals
        rSh.grid(row=3, column=0, padx=10, pady=10)
        rSh.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rShPH, shoulderList, "rSh"))

        lShTxt = Label(canvas, text="Left Shoulder slot:", width=25, height=3)
        lShTxt.grid(row=2, column=4, padx=10, pady=10)
        lShPH = StringVar(canvas)
        lSh = Combobox(canvas, textvariable=lShPH, state="readonly", width=25)
        lSh['values'] = tmpVals
        lSh.grid(row=3, column=4, padx=10, pady=10)
        lSh.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lShPH, shoulderList, "lSh"))

        body1Txt = Label(canvas, text="First Chasis slot:", width=25, height=3)
        body1Txt.grid(row=3, column=1, padx=10, pady=10)
        body1PH = StringVar(canvas)
        body1 = Combobox(canvas, textvariable=body1PH, state="readonly", width=25)
        tmpVals = [x.ime for x in bodyList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        body1['values'] = tmpVals
        body1.grid(row=4, column=1, padx=10, pady=10)
        body1.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body1PH, bodyList, "body1"))

        body2Txt = Label(canvas, text="Second Chasis slot:", width=25, height=3)
        body2Txt.grid(row=3, column=3, padx=10, pady=10)
        body2PH = StringVar(canvas)
        body2 = Combobox(canvas, textvariable=body2PH, state="readonly", width=25)
        body2['values'] = tmpVals
        body2.grid(row=4, column=3, padx=10, pady=10)
        body2.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body2PH, bodyList, "body2"))

        body3Txt = Label(canvas, text="Third Chasis slot:", width=25, height=3)
        body3Txt.grid(row=7, column=1, padx=10, pady=10)
        body3PH = StringVar(canvas)
        body3 = Combobox(canvas, textvariable=body3PH, state="readonly", width=25)
        body3['values'] = tmpVals
        body3.grid(row=8, column=1, padx=10, pady=10)
        body3.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body3PH, bodyList, "body3"))

        body4Txt = Label(canvas, text="Fourth Chasis slot:", width=25, height=3)
        body4Txt.grid(row=7, column=3, padx=10, pady=10)
        body4PH = StringVar(canvas)
        body4 = Combobox(canvas, textvariable=body4PH, state="readonly", width=25)
        body4['values'] = tmpVals
        body4.grid(row=8, column=3, padx=10, pady=10)
        body4.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body4PH, bodyList, "body4"))

        core1Txt = Label(canvas, text="First Core slot:", width=25, height=3)
        core1Txt.grid(row=5, column=1, padx=10, pady=10)
        core1PH = StringVar(canvas)
        core1 = Combobox(canvas, textvariable=core1PH, state="readonly", width=25)
        tmpVals = [x.ime for x in coreModList]+[""]
        core1['values'] = tmpVals
        core1.grid(row=6, column=1, padx=10, pady=10)
        core1.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(core1PH, coreModList, "core1"))

        core2Txt = Label(canvas, text="Second Core slot:", width=25, height=3)
        core2Txt.grid(row=5, column=3, padx=10, pady=10)
        core2PH = StringVar(canvas)
        core2 = Combobox(canvas, textvariable=core2PH, state="readonly", width=25)
        core2['values'] = tmpVals
        core2.grid(row=6, column=3, padx=10, pady=10)
        core2.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(core2PH, coreModList, "core2"))

        rLegTxt = Label(canvas, text="Right Leg slot:", width=25, height=3)
        rLegTxt.grid(row=9, column=1, padx=10, pady=10)
        rLegPH = StringVar(canvas)
        rLeg = Combobox(canvas, textvariable=rLegPH, state="readonly", width=25)
        tmpVals = [x.ime for x in legList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        rLeg['values'] = tmpVals
        rLeg.grid(row=10, column=1, padx=10, pady=10)
        rLeg.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rLegPH, legList, "rLeg"))

        lLegTxt = Label(canvas, text="Left Leg slot:", width=25, height=3)
        lLegTxt.grid(row=9, column=3, padx=10, pady=10)
        lLegPH = StringVar(canvas)
        lLeg = Combobox(canvas, textvariable=lLegPH, state="readonly", width=25)
        lLeg['values'] = tmpVals
        lLeg.grid(row=10, column=3, padx=10, pady=10)
        lLeg.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lLegPH, legList, "lLeg"))

        coreTxt = Label(canvas, text="Core:", width=25, height=3)
        coreTxt.grid(row=5, column=2, padx=10, pady=10)
        coreTypePH = StringVar(canvas)
        core = Combobox(canvas, textvariable=coreTypePH, state="readonly", width=25)
        tmpVals = [x.ime for x in coreList]
        core['values'] = tmpVals
        core.grid(row=6, column=2, padx=10, pady=10)
        core.bind("<<ComboboxSelected>>",
                  lambda e: self.comboBoxReturnObject(coreTypePH, coreList, "core"))

        return

    def createPilotWindow(self, flag):
        pw = Toplevel(self)
        pw.protocol('WM_DELETE_WINDOW', lambda: self.onDestroyCustomChild(pw))
        if flag == "ep":
            pw.title("Create NPC pilot preset")
        elif flag == "pp":
            pw.title("Create player pilot preset")
        ws = pw.winfo_screenwidth()
        hs = pw.winfo_screenheight()

        pw.update()
        canvas = Canvas(pw, width=ws, height=hs)
        canvas.grid(row=0, column=0)

        helmetList = [x for x in podatci.MODULES if "helmet" in x.slot]
        chestList = [x for x in podatci.MODULES if "chest" in x.slot]
        backList = [x for x in podatci.MODULES if "back" in x.slot]
        omniList = [x for x in podatci.MODULES if "omni-tool" in x.slot]
        legsList = [x for x in podatci.MODULES if "legs" in x.slot and "suit" in x.mount]
        weaponList = [x for x in podatci.PILOT_WEAPONS]
        extraList=helmetList+chestList+backList+legsList+omniList

        if flag == "ep":
            statPoints=IntVar(pw, 9)

            saveBtn = Button(canvas, text="Save NPC pilot preset", height=3, state="disabled",
                             command=lambda: self.saveNPCP(tier.get(), archetype.get(), hp.get(), ac.get(), lckVal.get(), action.get(), self.helmetSlot, self.chestSlot, self.backSlot, self.suitlegsSlot, self.omniSlot, self.weaponSlot, allyFlag.get()))
            saveBtn.grid(row=11, column=3, columnspan=2, padx=10, pady=10)

            allyFlag = IntVar(canvas)
            ally = Checkbutton(canvas, text="Create this NPC as an ally", variable=allyFlag)
            ally.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

            tierTxt = Label(canvas, text="Enemy Tier:", width=25, height=3)
            tierTxt.grid(row=0, column=0, padx=10, pady=10)
            tier = Entry(canvas, exportselection=0, width=25)
            tier.insert(0, int(1))
            tier.grid(row=1, column=0, padx=10, pady=10)

            archetypeTxt = Label(canvas, text="Enemy Archetype:", width=25, height=3)
            archetypeTxt.grid(row=0, column=1, padx=10, pady=10)
            archetype = Entry(canvas, exportselection=0, width=25)
            archetype.bind("<KeyRelease>", lambda e: self.enableWidget(e.widget.get(), saveBtn))
            archetype.grid(row=1, column=1, padx=10, pady=10)

            actionTxt = Label(canvas, text="Enemy actions per turn:\n(format as: XMove XAtt XAct)", width=25, height=3)
            actionTxt.grid(row=0, column=2, padx=10, pady=10)
            action = Entry(canvas, exportselection=0, width=25)
            action.insert(0, "0Move 0Att 0Act")
            action.grid(row=1, column=2, padx=10, pady=10)

            hpTxt = Label(canvas, text="Enemy maximum Hit Points:", width=25, height=3)
            hpTxt.grid(row=0, column=3, padx=10, pady=10)
            hp = Entry(canvas, exportselection=0, width=25)
            hp.insert(0, int(1))
            hp.grid(row=1, column=3, padx=10, pady=10)

            acTxt = Label(canvas, text="Enemy Armor Class (6-19):", width=25, height=3)
            acTxt.grid(row=0, column=4, padx=10, pady=10)
            ac = Entry(canvas, exportselection=0, width=25)
            ac.insert(0, int(6))
            ac.grid(row=1, column=4, padx=10, pady=10)

            statPointsTxt = Label(canvas, text="Maximum Points to allocate:", width=25, height=3)
            statPointsTxt.grid(row=2, column=5, padx=10, pady=10, columnspan=3)
            statPointslabel = Label(canvas, text=statPoints.get())
            statPointslabel.grid(row=3, column=5, padx=10, pady=10, columnspan=3)

            lckTxt = Label(canvas, text="Enemy Luck statistic:", width=25, height=3)
            lckTxt.grid(row=0, column=5, padx=10, pady=10, columnspan=3)
            lckVal=IntVar(canvas, 1)
            lckValLabel=Label(canvas, text=lckVal.get())
            lckValLabel.grid(row=1, column=6)
            lckUp=Button(canvas, text="-", command=lambda: self.statDown(lckVal, lckValLabel, statPoints, statPointslabel))
            lckUp.grid(row=1, column=5)
            lckDwn=Button(canvas, text="+", command=lambda: self.statUp(lckVal, lckValLabel, statPoints, statPointslabel))
            lckDwn.grid(row=1, column=7)

            weaponTxt = Label(canvas, text="Enemy Weapon:", width=25, height=3)
            weaponTxt.grid(row=3, column=3, padx=10, pady=10)
            weaponPH = StringVar(canvas)
            weapon = Combobox(canvas, textvariable=weaponPH, state="readonly", width=25)
            tmpVals = [x.ime for x in weaponList]+[""]
            weapon['values'] = tmpVals
            weapon.grid(row=4, column=3, padx=10, pady=10)
            weapon.bind("<<ComboboxSelected>>",
                       lambda e: self.comboBoxReturnObject(weaponPH, weaponList, "weapon"))

        elif flag == "pp":
            statPoints=IntVar(pw, 18)

            saveBtn = Button(canvas, text="Save player pilot preset", height=3, state="disabled",
                             command=lambda: self.savePCP(ime.get(),strVal.get(),perVal.get(),endVal.get(),intVal.get(),aglVal.get(),lckVal.get(),self.helmetSlot,self.chestSlot,self.backSlot,self.suitlegsSlot,self.omniSlot,self.extraSlot))
            saveBtn.grid(row=11, column=3, columnspan=2, padx=10, pady=10)

            imeTxt = Label(canvas, text="Pilot Name:", width=25, height=3)
            imeTxt.grid(row=0, column=1, padx=10, pady=10)
            ime = Entry(canvas, exportselection=0, width=25)
            ime.bind("<KeyRelease>", lambda e: self.enableWidget(e.widget.get(), saveBtn))
            ime.grid(row=1, column=1, padx=10, pady=10)

            statPointsTxt=Label(canvas, text="Points to spend:", width=25, height=3)
            statPointsTxt.grid(row=0, column=5, padx=10, pady=10, columnspan=3)
            statPointslabel=Label(canvas, text=statPoints.get())
            statPointslabel.grid(row=0, column=8, padx=10, pady=10, columnspan=3)

            strTxt = Label(canvas, text="Pilot Strength statistic:", width=25, height=3)
            strTxt.grid(row=1, column=5, padx=10, pady=10, columnspan=3)
            strVal = IntVar(canvas, 1)
            strValLabel = Label(canvas, text=strVal.get())
            strValLabel.grid(row=2, column=6)
            strUp = Button(canvas, text="-", command=lambda: self.statDown(strVal, strValLabel, statPoints, statPointslabel))
            strUp.grid(row=2, column=5)
            strDwn = Button(canvas, text="+", command=lambda: self.statUp(strVal, strValLabel, statPoints, statPointslabel))
            strDwn.grid(row=2, column=7)

            perTxt = Label(canvas, text="Pilot Perception statistic:", width=25, height=3)
            perTxt.grid(row=3, column=5, padx=10, pady=10, columnspan=3)
            perVal = IntVar(canvas, 1)
            perValLabel = Label(canvas, text=perVal.get())
            perValLabel.grid(row=4, column=6)
            perUp = Button(canvas, text="-", command=lambda: self.statDown(perVal, perValLabel, statPoints, statPointslabel))
            perUp.grid(row=4, column=5)
            perDwn = Button(canvas, text="+", command=lambda: self.statUp(perVal, perValLabel, statPoints, statPointslabel))
            perDwn.grid(row=4, column=7)

            endTxt = Label(canvas, text="Pilot Endurance statistic:", width=25, height=3)
            endTxt.grid(row=5, column=5, padx=10, pady=10, columnspan=3)
            endVal = IntVar(canvas, 1)
            endValLabel = Label(canvas, text=endVal.get())
            endValLabel.grid(row=6, column=6)
            endUp = Button(canvas, text="-", command=lambda: self.statDown(endVal, endValLabel, statPoints, statPointslabel))
            endUp.grid(row=6, column=5)
            endDwn = Button(canvas, text="+", command=lambda: self.statUp(endVal, endValLabel, statPoints, statPointslabel))
            endDwn.grid(row=6, column=7)

            intTxt = Label(canvas, text="Pilot Inteligence statistic:", width=25, height=3)
            intTxt.grid(row=1, column=8, padx=10, pady=10, columnspan=3)
            intVal = IntVar(canvas, 1)
            intValLabel = Label(canvas, text=intVal.get())
            intValLabel.grid(row=2, column=9)
            intUp = Button(canvas, text="-", command=lambda: self.statDown(intVal, intValLabel, statPoints, statPointslabel))
            intUp.grid(row=2, column=8)
            intUp.bind("<Button-1>", lambda e: self.enableWidget(intVal.get()-1>9, extra))
            intDwn = Button(canvas, text="+", command=lambda: self.statUp(intVal, intValLabel, statPoints, statPointslabel))
            intDwn.grid(row=2, column=10)
            intDwn.bind("<Button-1>", lambda e: self.enableWidget(intVal.get()+1>9, extra))

            aglTxt = Label(canvas, text="Pilot Agility statistic:", width=25, height=3)
            aglTxt.grid(row=3, column=8, padx=10, pady=10, columnspan=3)
            aglVal = IntVar(canvas, 1)
            aglValLabel = Label(canvas, text=aglVal.get())
            aglValLabel.grid(row=4, column=9)
            aglUp = Button(canvas, text="-", command=lambda: self.statDown(aglVal, aglValLabel, statPoints, statPointslabel))
            aglUp.grid(row=4, column=8)
            aglDwn = Button(canvas, text="+", command=lambda: self.statUp(aglVal, aglValLabel, statPoints, statPointslabel))
            aglDwn.grid(row=4, column=10)

            lckTxt = Label(canvas, text="Pilot Luck statistic:", width=25, height=3)
            lckTxt.grid(row=5, column=8, padx=10, pady=10, columnspan=3)
            lckVal = IntVar(canvas, 1)
            lckValLabel = Label(canvas, text=lckVal.get())
            lckValLabel.grid(row=6, column=9)
            lckUp = Button(canvas, text="-", command=lambda: self.statDown(lckVal, lckValLabel, statPoints, statPointslabel))
            lckUp.grid(row=6, column=8)
            lckDwn = Button(canvas, text="+", command=lambda: self.statUp(lckVal, lckValLabel, statPoints, statPointslabel))
            lckDwn.grid(row=6, column=10)

            extraTxt = Label(canvas, text="Extra Suit Module slot:", width=25, height=3)
            extraTxt.grid(row=7, column=3, padx=10, pady=10)
            extraPH = StringVar(canvas)
            extra = Combobox(canvas, textvariable=extraPH, state="readonly", width=25)
            tmpVals = [x.ime for x in extraList]+[""]
            extra['values'] = tmpVals
            extra['state'] = "disabled"
            extra.grid(row=8, column=3, padx=10, pady=10)
            extra.bind("<<ComboboxSelected>>",
                       lambda e: self.comboBoxReturnObject(extraPH, extraList, "extra"))

        helmetTxt = Label(canvas, text="Helmet slot:", width=25, height=3)
        helmetTxt.grid(row=3, column=1, padx=10, pady=10)
        helmetPH = StringVar(canvas)
        helmet = Combobox(canvas, textvariable=helmetPH, state="readonly", width=25)
        tmpVals = [x.ime for x in helmetList]+[""]
        helmet['values'] = tmpVals
        helmet.grid(row=4, column=1, padx=10, pady=10)
        helmet.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(helmetPH, helmetList, "helmet"))

        chestTxt = Label(canvas, text="Chest slot:", width=25, height=3)
        chestTxt.grid(row=5, column=1, padx=10, pady=10)
        chestPH = StringVar(canvas)
        chest = Combobox(canvas, textvariable=chestPH, state="readonly", width=25)
        tmpVals = [x.ime for x in chestList]+[""]
        chest['values'] = tmpVals
        chest.grid(row=6, column=1, padx=10, pady=10)
        chest.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(chestPH, chestList, "chest"))

        backTxt = Label(canvas, text="Back slot:", width=25, height=3)
        backTxt.grid(row=5, column=2, padx=10, pady=10)
        backPH = StringVar(canvas)
        back = Combobox(canvas, textvariable=backPH, state="readonly", width=25)
        tmpVals = [x.ime for x in backList]+[""]
        back['values'] = tmpVals
        back.grid(row=6, column=2, padx=10, pady=10)
        back.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(backPH, backList, "back"))

        legsTxt = Label(canvas, text="Legs slot:", width=25, height=3)
        legsTxt.grid(row=7, column=1, padx=10, pady=10)
        legsPH = StringVar(canvas)
        legs = Combobox(canvas, textvariable=legsPH, state="readonly", width=25)
        tmpVals = [x.ime for x in legsList]+[""]
        legs['values'] = tmpVals
        legs.grid(row=8, column=1, padx=10, pady=10)
        legs.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(legsPH, legsList, "suitlegs"))

        omniTxt = Label(canvas, text="Omni-tool slot:", width=25, height=3)
        omniTxt.grid(row=5, column=3, padx=10, pady=10)
        omniPH = StringVar(canvas)
        omni = Combobox(canvas, textvariable=omniPH, state="readonly", width=25)
        tmpVals = [x.ime for x in omniList]+[""]
        omni['values'] = tmpVals
        omni.grid(row=6, column=3, padx=10, pady=10)
        omni.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(omniPH, omniList, "omni"))

        return

    def comboBoxReturnObject(self, stoTrazim, vadimObjekt, flag, enableBtn=None):
        spremam=None
        for elem in vadimObjekt:
            if elem.ime == stoTrazim.get():
                spremam = copy.deepcopy(elem)
        if not spremam:
            spremam = stoTrazim.get()
        if stoTrazim.get()=="":
            spremam=None


        if flag == "rHa":
            self.rHaSlot = spremam
        elif flag == "lHa":
            self.lHaSlot = spremam
        elif flag == "rSh":
            self.rShSlot = spremam
        elif flag == "lSh":
            self.lShSlot = spremam
        elif flag == "body1":
            self.body1Slot = spremam
        elif flag == "body2":
            self.body2Slot = spremam
        elif flag == "body3":
            self.body3Slot = spremam
        elif flag == "body4":
            self.body4Slot = spremam
        elif flag == "core1":
            self.core1Slot = spremam
        elif flag == "core2":
            self.core2Slot = spremam
        elif flag == "lLeg":
            self.lLegSlot = spremam
        elif flag == "rLeg":
            self.rLegSlot = spremam
        elif flag == "core":
            self.coreSlot = spremam
        elif flag=="helmet":
            self.helmetSlot=spremam
        elif flag=="chest":
            self.chestSlot=spremam
        elif flag=="back":
            self.backSlot=spremam
        elif flag=="suitlegs":
            self.suitlegsSlot=spremam
        elif flag=="omni":
            self.omniSlot=spremam
        elif flag=="extra":
            self.extraSlot=spremam
        elif flag=="weapon":
            self.weaponSlot=spremam

        if enableBtn:
            enableBtn['state']="normal"

        print(spremam)
        return

    def enableWidget(self, check, widget):
        if check:
            widget['state'] = "normal"
        else:
            widget['state']="disabled"
            try:
                widget.set("")
            except AttributeError:
                pass
        return

    def statUp(self, statRef, labelRef, spRef, spLabelRef):
        br=statRef.get()
        sp=spRef.get()
        if br<10 and sp>0:
            statRef.set(br+1)
            sp-=1
            spRef.set(sp)
        labelRef['text']=statRef.get()
        spLabelRef['text']=spRef.get()
        print("stat points {}".format(spRef.get()))
        return

    def statDown(self, statRef, labelRef, spRef, spLabelRef):
        br = statRef.get()
        sp=spRef.get()
        if br >1:
            statRef.set(br - 1)
            sp += 1
            spRef.set(sp)
        labelRef['text'] = statRef.get()
        spLabelRef['text']=spRef.get()
        print("stat points {}".format(spRef.get()))
        return

    def saveNPCM(self, tier, archetype, action, rHa, lHa, rSh, lSh, body1, body2, body3, body4, core1, core2, core,
                 rLeg, lLeg, allyFlag):
        if not core: core = podatci.CORES[0]
        tier=int(tier)
        toSave = EnemyMech(tier, archetype, action, core, lSh, rSh, lHa, rHa, core1, core2, body1, body2, body3, body4,
                           lLeg, rLeg, allyFlag)
        replaced = False
        for i in range(len(podatci.ENEMY_MECHS)):
            if podatci.ENEMY_MECHS[i].tier == tier and podatci.ENEMY_MECHS[i].archetype == archetype:
                podatci.ENEMY_MECHS[i] = toSave
                replaced = True
        if not replaced:
            podatci.ENEMY_MECHS.append(toSave)
        return

    def savePCM(self, ime, rHa, lHa, rSh, lSh, body1, body2, body3, body4, core1, core2, core,
                 rLeg, lLeg):
        if not core: core=podatci.CORES[0]
        toSave = PlayerMech(ime, core, lSh, rSh, lHa, rHa, core1, core2, body1, body2, body3, body4,
                           lLeg, rLeg)
        replaced = False
        for i in range(len(podatci.PLAYER_MECHS)):
            if podatci.PLAYER_MECHS[i].ime == ime:
                podatci.PLAYER_MECHS[i] = toSave
                replaced = True
        if not replaced:
            podatci.PLAYER_MECHS.append(toSave)
        return

    def saveNPCP(self, tier, archetype, maxHP, ac, lck, actions, helm, chest, back, legs, omni, weapon, allyFlag):

        tier=int(tier)
        maxHP=int(maxHP)
        ac=int(ac)
        lck=int(lck)
        toSave = EnemyPilot(tier,archetype,maxHP,ac,lck,actions,helm,chest,back,legs,omni,weapon, allyFlag)
        replaced = False
        for i in range(len(podatci.ENEMY_PILOTS)):
            if podatci.ENEMY_PILOTS[i].tier == tier and podatci.ENEMY_PILOTS[i].archetype == archetype:
                podatci.ENEMY_PILOTS[i] = toSave
                replaced = True
        if not replaced:
            podatci.ENEMY_PILOTS.append(toSave)
        return

    def savePCP(self, ime,str_,per,end,int_,agl,lck,helm,chest,back,legs,omni,extra):

        str_=int(str_)
        per = int(per)
        end = int(end)
        int_ = int(int_)
        agl = int(agl)
        lck = int(lck)
        toSave = PlayerPilot(ime,str_,per,end,int_,agl,lck,helm,chest,back,legs,omni,extra, podatci.PILOT_WEAPONS[0])
        replaced = False
        for i in range(len(podatci.PLAYER_PILOTS)):
            if podatci.PLAYER_PILOTS[i].ime==ime:
                podatci.PLAYER_PILOTS[i] = toSave
                replaced = True
        if not replaced:
            podatci.PLAYER_PILOTS.append(toSave)
        return

    def createListWindow(self):
        lw = Toplevel(self)
        lw.title("List of all actors")
        ws = lw.winfo_screenwidth()
        hs = lw.winfo_screenheight()
        w = 1000
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        lw.geometry('%dx%d+%d+%d' % (w, h, x, y))
        lw.update()
        canvas = Canvas(lw, width=lw.winfo_width(), height=lw.winfo_height())
        canvas.grid(row=0, column=0)

        y = 0

        title=Label(canvas, text="PLAYER PILOTS", font=("Courier", 24), compound=RIGHT)
        canvas.create_window(10, y, window=title, anchor=NW)
        y += 60
        if len(podatci.PLAYER_PILOTS)==0:
            label=Label(canvas, text="No Data to display", compound=RIGHT)
            canvas.create_window(0, y, window=label, anchor=NW)
            y += 60
        else:
            for i in range(len(podatci.PLAYER_PILOTS)):
                objekt=podatci.PLAYER_PILOTS[i]
                label = Label(canvas, text=objekt.opis(extended=True), compound=RIGHT)
                canvas.create_window(0, y, window=label, anchor=NW)
                y += 60


        title = Label(canvas, text="PLAYER MECHS", font=("Courier", 24), compound=RIGHT)
        canvas.create_window(10, y, window=title, anchor=NW)
        y += 60
        if len(podatci.PLAYER_MECHS)==0:
            label=Label(canvas, text="No Data to display", compound=RIGHT)
            canvas.create_window(0, y, window=label, anchor=NW)
            y += 60
        else:
            for i in range(len(podatci.PLAYER_MECHS)):
                objekt=podatci.PLAYER_MECHS[i]
                label = Label(canvas, text=objekt.opis(extended=True), compound=RIGHT)
                canvas.create_window(0, y, window=label, anchor=NW)
                y += 60


        title = Label(canvas, text="NPC PILOTS", font=("Courier", 24), compound=RIGHT)
        canvas.create_window(10, y, window=title, anchor=NW)
        y += 60
        if len(podatci.ENEMY_PILOTS)==0:
            label=Label(canvas, text="No Data to display", compound=RIGHT)
            canvas.create_window(0, y, window=label, anchor=NW)
            y += 60
        else:
            for i in range(len(podatci.ENEMY_PILOTS)):
                objekt=podatci.ENEMY_PILOTS[i]
                label = Label(canvas, text=objekt.opis(extended=True), compound=RIGHT)
                canvas.create_window(0, y, window=label, anchor=NW)
                y += 60


        title = Label(canvas, text="NPC MECHS", font=("Courier", 24), compound=RIGHT)
        canvas.create_window(10, y, window=title, anchor=NW)
        y += 60
        if len(podatci.ENEMY_MECHS)==0:
            label=Label(canvas, text="No Data to display", compound=RIGHT)
            canvas.create_window(0, y, window=label, anchor=NW)
            y += 60
        else:
            for i in range(len(podatci.ENEMY_MECHS)):
                objekt=podatci.ENEMY_MECHS[i]
                label = Label(canvas, text=objekt.opis(extended=True), compound=RIGHT)
                #label.bind("<Control-Button-2>", lambda e: self.createDetailsWindow(e, podatci.ENEMY_MECHS))
                canvas.create_window(0, y, window=label, anchor=NW)
                y += 60

        scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))
        return

    ################ INTERCEPT on_destroy

    def loadDataOnStart(self):
        try:
            with open(self.savedEMs, "rb") as f:
                podatci.ENEMY_MECHS = pickle.load(f)
        except:
            pass
        try:
            with open(self.savedEPs, "rb") as f:
                podatci.ENEMY_PILOTS = pickle.load(f)
        except:
            pass
        try:
            with open(self.savedPPs, "rb") as f:
                podatci.PLAYER_PILOTS = pickle.load(f)
        except:
            pass
        try:
            with open(self.savedPMs, "rb") as f:
                podatci.PLAYER_MECHS = pickle.load(f)
        except:
            pass
        try:
            with open(self.savedDEPLOYED, "rb") as f:
                podatci.DEPLOYED = pickle.load(f)
        except:
            pass

        print("loaded {} player pilot objects".format(len(podatci.PLAYER_PILOTS)))
        print("loaded {} player mech objects".format(len(podatci.PLAYER_MECHS)))
        print("loaded {} enemy pilot objects".format(len(podatci.ENEMY_PILOTS)))
        print("loaded {} enemy mech objects".format(len(podatci.ENEMY_MECHS)))
        print("loaded {} deployed mech objects".format(len(podatci.DEPLOYED)))
        return

    def onDestroyCustom(self):

        with open(self.savedEMs, "wb") as f:
            pickle.dump(podatci.ENEMY_MECHS, f)
        with open(self.savedEPs, "wb") as f:
            pickle.dump(podatci.ENEMY_PILOTS, f)
        with open(self.savedPPs, "wb") as f:
            pickle.dump(podatci.PLAYER_PILOTS, f)
        with open(self.savedPMs, "wb") as f:
            pickle.dump(podatci.PLAYER_MECHS, f)
        with open(self.savedDEPLOYED, "wb") as f:
            pickle.dump(podatci.DEPLOYED, f)

        self.prozor.destroy()
        return

    def onDestroyCustomChild(self, window):

        with open(self.savedEMs, "wb") as f:
            pickle.dump(podatci.ENEMY_MECHS, f)
        with open(self.savedEPs, "wb") as f:
            pickle.dump(podatci.ENEMY_PILOTS, f)
        with open(self.savedPPs, "wb") as f:
            pickle.dump(podatci.PLAYER_PILOTS, f)
        with open(self.savedPMs, "wb") as f:
            pickle.dump(podatci.PLAYER_MECHS, f)

        window.destroy()
        self.createEditorUI()
        return


def main():
    p = GlavniProzor(Tk())
    p.mainloop()

    return


main()

import copy
from tkinter.ttk import Combobox

from PilotWeapon import *
from Module import *

class PlayerPilot:
    def __init__(self,ime,str,per,end,int,agl,lck,helm,chest,back,legs,omni,extra, weapon):
        self.ime=ime
        self.str=str
        self.per=per
        self.end=end
        self.int=int
        self.agl=agl
        self.lck=lck
        self.helm=helm
        self.chest=chest
        self.back=back
        self.legs=legs
        self.omni=omni
        self.extra=extra
        self.weapon=weapon
        self.slots = [
            self.helm,
            self.chest,
            self.back,
            self.legs,
            self.omni,
            self.extra,
            self.weapon
        ]
        self.newTmpStats=[]
        self.newTmpSlots=[None] *7
        self.setDerivedStats()
        return

    def setDerivedStats(self):
        self.level=1
        self.currXP=0
        self.maxHP=20+self.end*5
        self.actions={"action":0,"movement":0,"attack":0}
        self.evalAction()
        self.suppressed=False
        self.coverBonus=0
        self.statChangeCheck()
        return

    def statChangeCheck(self):
        self.reqXP = 260 - self.int * 10
        self.lvlupHP = self.end
        self.currHP=self.maxHP
        self.ac=5+int((self.agl+self.end)/2)
        if self.agl>=7: self.ac+=1
        if self.agl>=10: self.ac+=1
        self.evalAction()
        self.throwRange = int((self.str + self.agl) / 2)
        self.acTotal = self.ac
        self.evalAC()
        self.evalReserves()
        return

    def evalAC(self):
        if self.suppressed: self.coverBonus = 5

        if self.ac > 17: self.ac = 17
        if self.ac < 6: self.ac = 6

        self.acTotal = self.ac + self.coverBonus

        if self.acTotal > 19: self.acTotal = 19
        if self.acTotal < 6: self.acTotal = 6

        return

    def evalAction(self):
        if self.agl>=1: self.actions["action"]=1
        if self.agl>=3: self.actions["movement"]=1
        if self.agl>=5: self.actions["attack"]=1
        if self.agl>=9: self.actions["action"]=2
        return

    def evalReserves(self):
        if self.chest and self.chest.ime=="Extended ammo rig":
            if self.weapon:
                self.weapon.reserves+=5
        if self.legs and self.legs.ime=="Ammo rig":
            if self.weapon and self.weapon.weaponClass!="melee":
                self.weapon.reserves+=2
        return

    def addXP(self, ammount):
        self.currXP+=ammount
        while self.currXP>=self.reqXP:
            razlika=self.currXP-self.reqXP
            self.level+=1
            self.maxHP+=self.lvlupHP
            self.currXP=razlika
        return

    def changeHealth(self, ammount):
        self.currHP+=ammount
        if self.currHP>self.maxHP:
            self.currHP=self.maxHP
        elif self.currHP<0:
            self.currHP=0
        return

    def opis(self, extended=False):
        tekst="Codename: {}, Level: {}".format(self.ime, self.level)
        if extended:
            tekst+=", HP: {}/{}, AC (base): {}".format(self.currHP, self.maxHP, self.ac)
        return tekst

    def endTurn(self):
        for e in self.slots:
            try:
                e.endTurn()
            except:
                pass

        return

    def endCombat(self):
        for e in self.slots:
            try:
                e.endCombat()
            except:
                pass

        return

    def showDetails(self, parent):
        for child in parent.winfo_children():
            child.destroy()

        lvlText="level: {}".format(self.level)
        level=Label(parent, text=lvlText, justify=LEFT, anchor="w", wraplength=300)
        level.grid(row=1, column=0, padx=5, pady=5)

        progtxt="XP to next Level: {}/{}".format(self.currXP, self.reqXP)
        lvlProg=Label(parent, text=progtxt, justify=LEFT, anchor="w", wraplength=300)
        lvlProg.grid(row=1, column=1, padx=5, pady=5)

        postotak=int(round(self.currXP/self.reqXP*30))
        lista=['[']+['-']*30+[']']
        for i in range(postotak):
            lista[i+1]='X'
        lvlProgSketchTxt=''.join(lista)
        lvlProgSketch=Label(parent, text=lvlProgSketchTxt, justify=LEFT, anchor="w", wraplength=600, font=('TkFixedFont'))
        lvlProgSketch.grid(row=2, column=0, columnspan=2, padx=5)

        hptxt="Hit Points: {}/{}\nHit Point increase per Level-Up: {}".format(self.currHP, self.maxHP, self.lvlupHP)
        hp=Label(parent, text=hptxt, justify=LEFT, anchor="w", wraplength=300)
        hp.grid(row=1, column=2, padx=5, pady=5)

        actxt = "Base Armor Class (Total Armor Class): {} ({})".format(self.ac, self.acTotal)
        ac=Label(parent, text=actxt, justify=LEFT, anchor="w", wraplength=300)
        ac.grid(row=2, column=2, padx=5, pady=5)

        actionFrame=LabelFrame(parent, text="Actions per Turn")
        move=Label(actionFrame, text="Movement (2 squares = 1 movement action): ", justify=LEFT, anchor="w", wraplength=300)
        move.grid(row=0, column=0)
        attack=Label(actionFrame, text="Attack (1 attack = 1 attack action): ", justify=LEFT, anchor="w", wraplength=300)
        attack.grid(row=1, column=0)
        action=Label(actionFrame, text="Action (any other action or prolonged gesture): ", justify=LEFT, anchor="w", wraplength=300)
        action.grid(row=2, column=0)
        moveVal=Label(actionFrame, text=self.actions["movement"])
        moveVal.grid(row=0, column=1)
        attackVal = Label(actionFrame, text=self.actions["attack"])
        attackVal.grid(row=1, column=1)
        actionVal = Label(actionFrame, text=self.actions["action"])
        actionVal.grid(row=2, column=1)
        actionFrame.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

        throwtxt="Throw range: {}\n(PER roll determines accuracy of the throw)".format(self.throwRange)
        throw=Label(parent, text=throwtxt, justify=LEFT, anchor="w", wraplength=300)
        throw.grid(row=1, column=4, padx=5, pady=5)

        covertxt="Current cover bonus: {}\n".format(self.coverBonus)
        if self.suppressed:
            covertxt+="Character is currently suppressed and cannot take action towards suppressing enemy."
        else:
            covertxt+="Character is not under suppressing fire and can act normally."
        cover=Label(parent, text=covertxt, justify=LEFT, anchor="w", wraplength=300)
        cover.grid(row=2, column=4, padx=5, pady=5)

        statistics = LabelFrame(parent, text="Character's main statistics")
        self.showStats(statistics,parent)
        statistics.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

        suit=LabelFrame(parent, text="PILOT SUIT setup")
        show=Button(suit, text="Show suit modules' details", command=lambda: self.showSuitDetails(suit, parent))
        show.grid(row=0, column=0, padx=10, pady=10)
        edit=Button(suit, text="Edit suit modules", command=lambda: self.editSuit(suit, parent))
        edit.grid(row=0, column=1, padx=10, pady=10)
        suit.grid(row=4, column=0, rowspan=4, columnspan=5, padx=5, pady=5)

        return

    def showStats(self, parent, mainWin):

        self.newTmpStats = [self.str, self.per, self.end, self.int, self.agl, self.lck]
        strtxt = "Strength (STR): {}".format(self.newTmpStats[0])
        str_ = Label(parent, text=strtxt)
        str_.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        pertxt = "Perception (PER): {}".format(self.newTmpStats[1])
        per = Label(parent, text=pertxt)
        per.grid(row=0, column=3, padx=10, pady=10, columnspan=3)
        endtxt = "Endurance (END): {}".format(self.newTmpStats[2])
        end = Label(parent, text=endtxt)
        end.grid(row=0, column=6, padx=10, pady=10, columnspan=3)
        inttxt = "Inteligence (INT): {}".format(self.newTmpStats[3])
        int_ = Label(parent, text=inttxt)
        int_.grid(row=0, column=9, padx=10, pady=10, columnspan=3)
        agltxt = "Agility (AGL): {}".format(self.newTmpStats[4])
        agl = Label(parent, text=agltxt)
        agl.grid(row=0, column=12, padx=10, pady=10, columnspan=3)
        lcktxt = "Luck (LCK): {}".format(self.newTmpStats[5])
        lck = Label(parent, text=lcktxt)
        lck.grid(row=0, column=15, padx=10, pady=10, columnspan=3)
        upgrade = Button(parent, text="Upgrade Stats", command=lambda: self.showStatUpgrade(parent, mainWin))
        upgrade.grid(row=0, column=18, padx=10, pady=10, columnspan=3)

        return

    def showStatUpgrade(self, parent, mainWin):
        def save_f(p):
            self.saveStatUpgrade()
            cancel_f(p)

        def cancel_f(p):
            for child in p.winfo_children():
                child.destroy()
            self.showDetails(mainWin)


        downer=Button(parent, text="-", width=3, command=lambda: self.changeStat(self.str,0,-1,differences))
        downer.grid(row=1, column=0, padx=5, pady=5)
        differences=Label(parent, text="%+d"%0)
        differences.grid(row=1, column=1)
        uper=Button(parent, text="+", width=3, command=lambda: self.changeStat(self.str,0,1,differences))
        uper.grid(row=1, column=2, padx=5, pady=5)
        downer = Button(parent, text="-", width=3, command=lambda: self.changeStat(self.per,1,-1,differencep))
        downer.grid(row=1, column=3, padx=5, pady=5)
        differencep = Label(parent, text="%+d"%0)
        differencep.grid(row=1, column=4)
        uper = Button(parent, text="+", width=3, command=lambda: self.changeStat(self.per,1,1,differencep))
        uper.grid(row=1, column=5, padx=5, pady=5)
        downer = Button(parent, text="-", width=3, command=lambda: self.changeStat(self.end,2,-1,differencee))
        downer.grid(row=1, column=6, padx=5, pady=5)
        differencee = Label(parent, text="%+d"%0)
        differencee.grid(row=1, column=7)
        uper = Button(parent, text="+", width=3, command=lambda: self.changeStat(self.end,2,1,differencee))
        uper.grid(row=1, column=8, padx=5, pady=5)
        downer = Button(parent, text="-", width=3, command=lambda: self.changeStat(self.int,3,-1,differencei))
        downer.grid(row=1, column=9, padx=5, pady=5)
        differencei = Label(parent, text="%+d"%0)
        differencei.grid(row=1, column=10)
        uper = Button(parent, text="+", width=3, command=lambda: self.changeStat(self.int,3,1,differencei))
        uper.grid(row=1, column=11, padx=5, pady=5)
        downer = Button(parent, text="-", width=3, command=lambda: self.changeStat(self.agl,4,-1,differencea))
        downer.grid(row=1, column=12, padx=5, pady=5)
        differencea = Label(parent, text="%+d"%0)
        differencea.grid(row=1, column=13)
        uper = Button(parent, text="+", width=3, command=lambda: self.changeStat(self.agl,4,1,differencea))
        uper.grid(row=1, column=14, padx=5, pady=5)
        downer = Button(parent, text="-", width=3, command=lambda: self.changeStat(self.lck,5,-1,differencel))
        downer.grid(row=1, column=15, padx=5, pady=5)
        differencel = Label(parent, text="%+d"%0)
        differencel.grid(row=1, column=16)
        uper = Button(parent, text="+", width=3, command=lambda: self.changeStat(self.lck,5,1,differencel))
        uper.grid(row=1, column=17, padx=5, pady=5)
        save = Button(parent, text="Confirm", command=lambda: save_f(parent))
        save.grid(row=1, column=18, padx=5, pady=5)
        cancel = Button(parent, text="Cancel", command=lambda: cancel_f(parent))
        cancel.grid(row=1, column=19, padx=5, pady=5)
        return

    def changeStat(self, stat, index, ammount, difflbl):
        self.newTmpStats[index]+=ammount
        if self.newTmpStats[index]<stat:
            self.newTmpStats[index]=stat
        elif self.newTmpStats[index]>10:
            self.newTmpStats[index]=10
        diff=self.newTmpStats[index]-stat
        difflbl['text']="%+d"%diff
        return

    def saveStatUpgrade(self):
        self.str=self.newTmpStats[0]
        self.per=self.newTmpStats[1]
        self.end=self.newTmpStats[2]
        self.int=self.newTmpStats[3]
        self.agl=self.newTmpStats[4]
        self.lck=self.newTmpStats[5]
        self.statChangeCheck()
        return

    def showSuitDetails(self, parent, grandParent):
        for child in parent.winfo_children():
            child.destroy()
        helmTitle = Label(parent, text="Helmet module:", justify=LEFT, wraplength=100)
        helmTitle.grid(row=0, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=1, column=0, sticky="ew", columnspan=5)
        chestTitle = Label(parent, text="Chest module:", justify=LEFT, wraplength=100)
        chestTitle.grid(row=2, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=3, column=0, sticky="ew", columnspan=5)
        backTitle = Label(parent, text="Back module:", justify=LEFT, wraplength=100)
        backTitle.grid(row=4, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=5, column=0, sticky="ew", columnspan=5)
        legsTitle = Label(parent, text="Suit Legs module:", justify=LEFT, wraplength=100)
        legsTitle.grid(row=6, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=7, column=0, sticky="ew", columnspan=5)
        omniTitle = Label(parent, text="Omni-Tool module:", justify=LEFT, wraplength=100)
        omniTitle.grid(row=8, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=9, column=0, sticky="ew", columnspan=5)
        extraTitle = Label(parent, text="Suit extension module:", justify=LEFT, wraplength=100)
        extraTitle.grid(row=10, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=11, column=0, sticky="ew", columnspan=5)
        weaponTitle = Label(parent, text="Currently equipped Weapon:", justify=LEFT, wraplength=100)
        weaponTitle.grid(row=12, column=0, padx=5, pady=5)
        for i in range(len(self.slots)):
            frame = Frame(parent)
            if self.slots[i]:
                self.slots[i].showDetails(frame)
            else:
                label = Label(frame, text="There is no module on this slot.")
                label.grid(row=0, column=0)
            frame.grid(row=i * 2, column=1, columnspan=4)
        hide = Button(parent, text="Hide suit modules' details", command=lambda: self.showDetails(grandParent))
        hide.grid(row=13, column=0, padx=10, pady=10)
        edit = Button(parent, text="Edit suit modules", command=lambda: self.editSuit(parent, grandParent))
        edit.grid(row=13, column=1, padx=10, pady=10)
        return

    def editSuit(self, parent, grandParent):
        for child in parent.winfo_children():
            child.destroy()

        helmetList = [x for x in podatci.MODULES if "helmet" in x.slot]
        chestList = [x for x in podatci.MODULES if "chest" in x.slot]
        backList = [x for x in podatci.MODULES if "back" in x.slot]
        omniList = [x for x in podatci.MODULES if "omni-tool" in x.slot]
        legsList = [x for x in podatci.MODULES if "legs" in x.slot and "suit" in x.mount]
        extraList = helmetList + chestList + backList + omniList + legsList
        weaponList = [x for x in podatci.PILOT_WEAPONS]

        helmetTxt = Label(parent, text="Helmet slot:", width=25, height=3)
        helmetTxt.grid(row=0, column=0, padx=5, pady=5)
        helmetPH = StringVar(parent, self.helm.ime if self.helm else None)
        helmet = Combobox(parent, textvariable=helmetPH, state="readonly", width=25)
        tmpVals = [x.ime for x in helmetList]+[""]
        helmet['values'] = tmpVals
        helmet.grid(row=1, column=0, padx=5, pady=5)
        helmet.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(helmetPH, helmetList, "helmet"))

        chestTxt = Label(parent, text="Chest slot:", width=25, height=3)
        chestTxt.grid(row=2, column=0, padx=5, pady=5)
        chestPH = StringVar(parent, self.chest.ime if self.chest else None)
        chest = Combobox(parent, textvariable=chestPH, state="readonly", width=25)
        tmpVals = [x.ime for x in chestList]+[""]
        chest['values'] = tmpVals
        chest.grid(row=3, column=0, padx=5, pady=5)
        chest.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(chestPH, chestList, "chest"))

        backTxt = Label(parent, text="Back slot:", width=25, height=3)
        backTxt.grid(row=2, column=1, padx=5, pady=5)
        backPH = StringVar(parent, self.back.ime if self.back else None)
        back = Combobox(parent, textvariable=backPH, state="readonly", width=25)
        tmpVals = [x.ime for x in backList]+[""]
        back['values'] = tmpVals
        back.grid(row=3, column=1, padx=5, pady=5)
        back.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(backPH, backList, "back"))

        legsTxt = Label(parent, text="Legs slot:", width=25, height=3)
        legsTxt.grid(row=4, column=0, padx=5, pady=5)
        legsPH = StringVar(parent, self.legs.ime if self.legs else None)
        legs = Combobox(parent, textvariable=legsPH, state="readonly", width=25)
        tmpVals = [x.ime for x in legsList]+[""]
        legs['values'] = tmpVals
        legs.grid(row=5, column=0, padx=5, pady=5)
        legs.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(legsPH, legsList, "suitlegs"))

        omniTxt = Label(parent, text="Omni-tool slot:", width=25, height=3)
        omniTxt.grid(row=2, column=2, padx=5, pady=5)
        omniPH = StringVar(parent, self.omni.ime if self.omni else None)
        omni = Combobox(parent, textvariable=omniPH, state="readonly", width=25)
        tmpVals = [x.ime for x in omniList]+[""]
        omni['values'] = tmpVals
        omni.grid(row=3, column=2, padx=5, pady=5)
        omni.bind("<<ComboboxSelected>>",
                  lambda e: self.comboBoxReturnObject(omniPH, omniList, "omni"))

        extraTxt = Label(parent, text="Extra Suit Module slot:", width=25, height=3)
        extraTxt.grid(row=4, column=2, padx=5, pady=5)
        extraPH = StringVar(parent, self.extra.ime if self.extra else None)
        extra = Combobox(parent, textvariable=extraPH, state="readonly", width=25)
        tmpVals = [x.ime for x in extraList]+[""]
        extra['values'] = tmpVals
        extra['state'] = "disabled" if self.int<10 else "normal"
        extra.grid(row=5, column=2, padx=5, pady=5)
        extra.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(extraPH, extraList, "extra"))

        weaponTxt = Label(parent, text="Enemy Weapon:", width=25, height=3)
        weaponTxt.grid(row=3, column=3, padx=10, pady=10)
        weaponPH = StringVar(parent, self.weapon.ime if self.weapon else None)
        weapon = Combobox(parent, textvariable=weaponPH, state="readonly", width=25)
        tmpVals = [x.ime for x in weaponList] + [""]
        weapon['values'] = tmpVals
        weapon.grid(row=4, column=3, padx=10, pady=10)
        weapon.bind("<<ComboboxSelected>>",
                    lambda e: self.comboBoxReturnObject(weaponPH, weaponList, "weapon"))

        def btn_func():
            self.comboBoxReturnObject(helmetPH, helmetList, "helmet")
            self.comboBoxReturnObject(chestPH, chestList, "chest")
            self.comboBoxReturnObject(backPH, backList, "back")
            self.comboBoxReturnObject(legsPH, legsList, "suitlegs")
            self.comboBoxReturnObject(omniPH, omniList, "omni")
            self.comboBoxReturnObject(extraPH, extraList, "extra")
            self.saveEdit(parent, grandParent)

        save=Button(parent, text="Save preset", command=btn_func)
        save.grid(row=6, column=0, padx=5, pady=5)
        saveWarning=Label(parent, text="Warning! This will overwrite your current setup!", wraplength=150, font=("Arial",10,"bold"))
        saveWarning.grid(row=7, column=0, padx=5, pady=5)
        cancel = Button(parent, text="cancel editing", command=lambda: self.showDetails(grandParent))
        cancel.grid(row=6, column=1, padx=5, pady=5)
        return

    def comboBoxReturnObject(self, stoTrazim, vadimObjekt, flag):
        spremam=None
        for elem in vadimObjekt:
            if elem.ime == stoTrazim.get():
                spremam = copy.deepcopy(elem)
        if not spremam:
            spremam = stoTrazim.get()
        if stoTrazim.get()=="":
            spremam=None

        if flag=="helmet":
            self.newTmpSlots[0]=spremam
        elif flag=="chest":
            self.newTmpSlots[1]=spremam
        elif flag=="back":
            self.newTmpSlots[2]=spremam
        elif flag=="suitlegs":
            self.newTmpSlots[3]=spremam
        elif flag=="omni":
            self.newTmpSlots[4]=spremam
        elif flag=="extra":
            self.newTmpSlots[5]=spremam
        elif flag == "weapon":
            self.newTmpSlots[6] = spremam

        return

    def saveEdit(self, parent, grandParent):
        self.helm=self.newTmpSlots[0]
        self.chest = self.newTmpSlots[1]
        self.back = self.newTmpSlots[2]
        self.legs = self.newTmpSlots[3]
        self.omni = self.newTmpSlots[4]
        self.extra = self.newTmpSlots[5]
        self.weapon = self.newTmpSlots[6]
        for i in range(len(self.slots)):
             self.slots[i]=self.newTmpSlots[i]
        self.showSuitDetails(parent, grandParent)
        return

    def showCombatScreen(self, parent):
        def hp_f(ammount, coef, label):
            self.changeHealth(ammount * coef)
            label['text']="Hit Points: {}/{}".format(self.currHP, self.maxHP)

        def ac_f(acLbl, coverLbl, val):
            self.coverBonus=val
            self.evalAC()
            acLbl['text']="Armor Class (Total): {}".format(self.ac+self.coverBonus)
            coverLbl['text']="Cover Bonus: {}".format(self.coverBonus)

        def xp_f(ammount, lvlLabel, xpLabel):
            self.addXP(ammount)
            lvlLabel['text'] ="Level: {}".format(self.level)
            xpLabel['text']="Experience: {}/{}".format(self.currXP, self.reqXP)


        stattit=Label(parent, text="Statistics", font=("Arial",13,"bold"))
        stattit.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        healthFrame=LabelFrame(parent)
        hptxt="Hit Points: {}/{}".format(self.currHP, self.maxHP)
        hp=Label(healthFrame, text=hptxt)
        hp.grid(row=0, column=0, padx=5, pady=5)
        changeEntry=Entry(healthFrame, exportselection=0, width=5)
        changeEntry.insert(0, int(0))
        changeEntry.grid(row=0, column=1, padx=5, pady=5)
        damage=Button(healthFrame, text="Damage", command=lambda: hp_f(int(changeEntry.get()), -1, hp))
        damage.grid(row=0, column=2, padx=5, pady=5)
        repair = Button(healthFrame, text="Heal", command=lambda: hp_f(int(changeEntry.get()), 1, hp))
        repair.grid(row=0, column=3, padx=5, pady=5)
        healthFrame.grid(row=1, column=0, padx=20)

        acFrame = LabelFrame(parent)
        actxt = "Armor Class (Total): {}".format(self.ac+self.coverBonus)
        ac = Label(acFrame, text=actxt)
        ac.grid(row=0, column=0, padx=5, pady=5)
        covertxt = "Cover Bonus: {}".format(self.coverBonus)
        cover = Label(acFrame, text=covertxt)
        cover.grid(row=1, column=0, padx=5, pady=5)
        coverbuttons=LabelFrame(acFrame, text="Unit cover")
        val=IntVar()
        nocover=Radiobutton(coverbuttons, text="Not in Cover", padx=20, variable=val, value=0, command=lambda: ac_f(ac, cover, int(val.get())))
        nocover.grid(row=0, column=0, pady=5)
        halfcover = Radiobutton(coverbuttons, text="in Waist high Cover", padx=20, variable=val, value=1, command=lambda: ac_f(ac, cover, int(val.get())))
        halfcover.grid(row=1, column=0, pady=5)
        threeqcover = Radiobutton(coverbuttons, text="in Chest high Cover", padx=20, variable=val, value=2, command=lambda: ac_f(ac, cover, int(val.get())))
        threeqcover.grid(row=2, column=0, pady=5)
        coverbuttons.grid(row=0, column=1, rowspan=2, padx=5, pady=5)
        acFrame.grid(row=1, column=1, padx=20)
        if self.coverBonus==0:
            nocover.select()
        elif self.coverBonus==1:
            halfcover.select()
        elif self.coverBonus==2:
            threeqcover.select()

        xpFrame = LabelFrame(parent)
        lvltxt = "Level: {}".format(self.level)
        lvl = Label(xpFrame, text=lvltxt)
        lvl.grid(row=0, column=0, padx=5, pady=5)
        xptxt = "Experience: {}/{}".format(self.currXP, self.reqXP)
        xp = Label(xpFrame, text=xptxt)
        xp.grid(row=1, column=0, padx=5, pady=5)
        xpEntry = Entry(xpFrame, exportselection=0, width=5)
        xpEntry.insert(0, int(0))
        xpEntry.grid(row=1, column=1, padx=5, pady=5)
        add = Button(xpFrame, text="Add XP", command=lambda: xp_f(int(xpEntry.get()), lvl, xp))
        add.grid(row=1, column=2, padx=5, pady=5)
        xpFrame.grid(row=1, column=2, padx=20)

        modstit=Label(parent, text="Modules and Weapons", font=("Arial",13,"bold"))
        modstit.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        equipmentFrame=Frame(parent)
        equipmentFrame.grid(row=4, column=0, columnspan=3)
        i=0
        for elem in self.slots:
            if elem:
                frame = Frame(equipmentFrame)
                elem.showCombatScreen(frame, 0)
                r=i//4
                c=i%4
                frame.grid(row=r, column=c, padx=5, pady=25)
                i+=1

        return

    def delete(self):
        try:
            podatci.PLAYER_PILOTS.remove(self)
        except ValueError:
            print("Couldn't remove requested entity.")
        return
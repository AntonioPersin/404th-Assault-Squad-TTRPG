import copy
from tkinter.ttk import Combobox

from Module import *
from MechWeapon import *
import podatci as podatci


class PlayerMech:
    def __init__(self,ime,core,lSh,rSh,lArm,rArm,coreA,coreB,chestA,chestB,chestC,chestD,lLeg,rLeg):
        self.coverBonus=0
        self.maxHP=500
        self.ac=4
        self.ime=ime
        self.core=core
        self.lSh=lSh
        self.rSh=rSh
        self.lArm=lArm
        self.rArm=rArm
        self.coreA=coreA
        self.coreB=coreB
        self.chestA=chestA
        self.chestB=chestB
        self.chestC=chestC
        self.chestD=chestD
        self.lLeg=lLeg
        self.rLeg=rLeg
        self.slots=[
                self.core,
                self.lSh,
                self.rSh,
                self.lArm,
                self.rArm,
                self.coreA,
                self.coreB,
                self.chestA,
                self.chestB,
                self.chestC,
                self.chestD,
                self.lLeg,
                self.rLeg
            ]
        self.newTmpSlots = [None] * 13
        self.setDerivedStats()
        return

    def setDerivedStats(self):
        self.evalCore()
        self.evalHP()
        self.currHP = self.maxHP
        self.acTotal = self.ac
        self.evalAC()
        return

    def evalAC(self):
        for e in self.slots:
            if e=="Armor":
                self.ac+=1
        if self.slots[1]==self.slots[2]=="Armor":
            self.ac+=1
        if self.slots[11]==self.slots[12]=="Armor":
            self.ac+=1
        if self.slots[7]==self.slots[8]==self.slots[9]==self.slots[10]=="Armor":
            self.ac+=2

        if self.ac>16: self.ac=16
        if self.ac<4: self.ac=4

        self.acTotal=self.ac+self.coverBonus
        return

    def evalHP(self):
        if self.coreA:
            if self.coreA.ime=="Reinforced core casing":
                self.maxHP=650
            elif self.coreA.ime=="Reinforced core casing Mk.2":
                self.maxHP = 750
            elif self.coreA.ime == "Reinforced core casing Mk.3":
                self.maxHP = 850
            else:
                self.maxHP = 500

        if self.coreB:
            if self.coreB.ime=="Reinforced core casing":
                self.maxHP=650
            elif self.coreB.ime=="Reinforced core casing Mk.2":
                self.maxHP = 750
            elif self.coreB.ime == "Reinforced core casing Mk.3":
                self.maxHP = 850
            else:
                self.maxHP = 500
        return

    def evalCore(self):
        if self.coreA:
            if self.coreA.ime=="Upgraded core capacitors":
                self.core.changeMaxPower(1)
            elif self.coreA.ime=="Upgraded core capacitors Mk.2":
                self.core.changeMaxPower(2)
            else:
                self.core.changeMaxPower(0)

        if self.coreB:
            if self.coreB.ime=="Upgraded core capacitors":
                self.core.changeMaxPower(1)
            elif self.coreB.ime=="Upgraded core capacitors Mk.2":
                self.core.changeMaxPower(2)
            else:
                self.core.changeMaxPower(0)

        return

    def changeHealth(self, ammount):
        self.currHP+=ammount
        if self.currHP>self.maxHP:
            self.currHP=self.maxHP
        elif self.currHP<0:
            self.currHP=0
        return

    def opis(self, extended=False):
        tekst="Mech name: {}, Core: {}".format(self.ime, self.core.ime)
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
        hptxt = "Hit Points: {}/{}".format(self.currHP, self.maxHP)
        hp = Label(parent, text=hptxt, justify=LEFT, anchor="w", wraplength=300)
        hp.grid(row=1, column=0, padx=5, pady=5)

        actxt = "Base Armor Class (Total Armor Class): {} ({})".format(self.ac, self.acTotal)
        ac = Label(parent, text=actxt, justify=LEFT, anchor="w", wraplength=300)
        ac.grid(row=1, column=1, padx=5, pady=5)

        actionFrame = LabelFrame(parent, text="Actions per Turn")
        move = Label(actionFrame, text="Player Mechs have 1 of each of the different action types its' pilot has.", justify=LEFT, anchor="w", wraplength=300)
        move.grid(row=0, column=0)
        actionFrame.grid(row=1, column=2, padx=5, pady=5)

        throwtxt = "Mechs can fastball heavier and bigger objects with the fixed maximum range of 20"
        throw = Label(parent, text=throwtxt, justify=LEFT, anchor="w", wraplength=300)
        throw.grid(row=1, column=3, padx=5, pady=5)

        covertxt = "Current cover bonus: {}".format(self.coverBonus)
        cover = Label(parent, text=covertxt, justify=LEFT, anchor="w", wraplength=300)
        cover.grid(row=1, column=4, padx=5, pady=5)

        parent.update()
        frame = Frame(parent)
        canvas = Canvas(frame, height=700, width=1400)
        frame.grid(row=2, column=0, columnspan=5)
        canvas.grid(column=0, row=0, sticky="nw")
        scrollFrame = Frame(canvas)
        scrollbarNS = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scrollFrame.bind("<Configure>",
                         lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbarNS.set)
        scrollbarNS.grid(row=0, column=1, sticky="nes")

        preset = LabelFrame(scrollFrame, text="MECH MODULES setup")
        show = Button(preset, text="Show Mech modules' details", command=lambda: self.showLoadoutDetails(preset, parent))
        show.grid(row=0, column=0, padx=10, pady=10)
        edit = Button(preset, text="Edit Mech modules", command=lambda: self.editLoadout(preset, parent))
        edit.grid(row=0, column=1, padx=10, pady=10)
        preset.grid(row=0, column=0, padx=5, pady=5)
        return

    def showLoadoutDetails(self, parent, grandParent):
        for child in parent.winfo_children():
            child.destroy()
        coreTitle = Label(parent, text="Core:", justify=LEFT, wraplength=100)
        coreTitle.grid(row=0, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=1, column=0, sticky="ew", columnspan=5)
        lShTitle = Label(parent, text="Left Shoulder module/weapon:", justify=LEFT, wraplength=100)
        lShTitle.grid(row=2, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=3, column=0, sticky="ew", columnspan=5)
        rShTitle = Label(parent, text="Right Shoulder module/weapon:", justify=LEFT, wraplength=100)
        rShTitle.grid(row=4, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=5, column=0, sticky="ew", columnspan=5)
        lArmTitle = Label(parent, text="Left Arm weapon:", justify=LEFT, wraplength=100)
        lArmTitle.grid(row=6, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=7, column=0, sticky="ew", columnspan=5)
        rArmTitle = Label(parent, text="Right Arm weapon:", justify=LEFT, wraplength=100)
        rArmTitle.grid(row=8, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=9, column=0, sticky="ew", columnspan=5)
        coreATitle = Label(parent, text="First Core module:", justify=LEFT, wraplength=100)
        coreATitle.grid(row=10, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=11, column=0, sticky="ew", columnspan=5)
        coreBTitle = Label(parent, text="Second Core module:", justify=LEFT, wraplength=100)
        coreBTitle.grid(row=12, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=13, column=0, sticky="ew", columnspan=5)
        bodyATitle = Label(parent, text="First Chasis (Body) module:", justify=LEFT, wraplength=100)
        bodyATitle.grid(row=14, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=15, column=0, sticky="ew", columnspan=5)
        bodyBTitle = Label(parent, text="Second Chasis (Body) module:", justify=LEFT, wraplength=100)
        bodyBTitle.grid(row=16, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=17, column=0, sticky="ew", columnspan=5)
        bodyCTitle = Label(parent, text="Third Chasis (Body) module:", justify=LEFT, wraplength=100)
        bodyCTitle.grid(row=18, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=19, column=0, sticky="ew", columnspan=5)
        bodyDTitle = Label(parent, text="Fourth Chasis (Body) module:", justify=LEFT, wraplength=100)
        bodyDTitle.grid(row=20, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=21, column=0, sticky="ew", columnspan=5)
        lLegTitle = Label(parent, text="Left Leg module:", justify=LEFT, wraplength=100)
        lLegTitle.grid(row=22, column=0, padx=5, pady=5)
        sep = Separator(parent, orient='horizontal')
        sep.grid(row=23, column=0, sticky="ew", columnspan=5)
        rLegTitle = Label(parent, text="Right Leg module:", justify=LEFT, wraplength=100)
        rLegTitle.grid(row=24, column=0, padx=5, pady=5)
        for i in range(len(self.slots)):
            frame = Frame(parent)
            if self.slots[i] and isinstance(self.slots[i], (Module, Core, MechWeapon)):
                self.slots[i].showDetails(frame)
            elif self.slots[i] and isinstance(self.slots[i], str):
                label = Label(frame, text=self.slots[i])
                label.grid(row=0, column=0)
            else:
                label = Label(frame, text="There is no module on this slot.")
                label.grid(row=0, column=0)
            frame.grid(row=i * 2, column=1, columnspan=4)
        hide = Button(parent, text="Hide mech modules' details", command=lambda: self.showDetails(grandParent))
        hide.grid(row=25, column=0, padx=10, pady=10)
        edit = Button(parent, text="Edit mech modules", command=lambda: self.editLoadout(parent, grandParent))
        edit.grid(row=25, column=1, padx=10, pady=10)
        return

    def editLoadout(self, parent, grandParent):
        for child in parent.winfo_children():
            child.destroy()

        armList = [x for x in podatci.MECH_WEAPONS if "arm weapon" in x.slot]
        shoulderList = [x for x in podatci.MECH_WEAPONS if "shoulder" in x.slot]
        shoulderList.extend([x for x in podatci.MODULES if "shoulder" in x.slot])
        bodyList = [x for x in podatci.MODULES if "body" in x.slot]
        coreModList = [x for x in podatci.MODULES if "core" in x.slot]
        coreList = podatci.CORES
        legList = [x for x in podatci.MODULES if "leg" in x.slot]

        rHaTxt = Label(parent, text="Right Hand slot:", width=25, height=3)
        rHaTxt.grid(row=5, column=0, padx=10, pady=10)
        rHaPH = StringVar(parent, self.rArm.ime if self.rArm else None)
        rHa = Combobox(parent, textvariable=rHaPH, state="readonly", width=25)
        tmpVals = [x.ime for x in armList] + [""]
        rHa['values'] = tmpVals
        rHa.grid(row=6, column=0, padx=10, pady=10)
        rHa.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rHaPH, armList, "rHa"))

        lHaTxt = Label(parent, text="Left Hand slot:", width=25, height=3)
        lHaTxt.grid(row=5, column=4, padx=10, pady=10)
        lHaPH = StringVar(parent, self.lArm.ime if self.lArm else None)
        lHa = Combobox(parent, textvariable=lHaPH, state="readonly", width=25)
        lHa['values'] = tmpVals
        lHa.grid(row=6, column=4, padx=10, pady=10)
        lHa.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lHaPH, armList, "lHa"))

        rShTxt = Label(parent, text="Right Shoulder slot:", width=25, height=3)
        rShTxt.grid(row=2, column=0, padx=10, pady=10)
        rShPH = StringVar(parent,
                          self.rSh.ime if isinstance(self.rSh, (MechWeapon, Module)) else self.rSh if isinstance(
                              self.rSh, str) else None)
        rSh = Combobox(parent, textvariable=rShPH, state="readonly", width=25)
        tmpVals = [x.ime for x in shoulderList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        rSh['values'] = tmpVals
        rSh.grid(row=3, column=0, padx=10, pady=10)
        rSh.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rShPH, shoulderList, "rSh"))

        lShTxt = Label(parent, text="Left Shoulder slot:", width=25, height=3)
        lShTxt.grid(row=2, column=4, padx=10, pady=10)
        lShPH = StringVar(parent,
                          self.lSh.ime if isinstance(self.lSh, (MechWeapon, Module)) else self.lSh if isinstance(
                              self.lSh, str) else None)
        lSh = Combobox(parent, textvariable=lShPH, state="readonly", width=25)
        lSh['values'] = tmpVals
        lSh.grid(row=3, column=4, padx=10, pady=10)
        lSh.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lShPH, shoulderList, "lSh"))

        body1Txt = Label(parent, text="First Chasis slot:", width=25, height=3)
        body1Txt.grid(row=3, column=1, padx=10, pady=10)
        body1PH = StringVar(parent, self.chestA.ime if isinstance(self.chestA,
                                                                  (MechWeapon, Module)) else self.chestA if isinstance(
            self.chestA, str) else None)
        body1 = Combobox(parent, textvariable=body1PH, state="readonly", width=25)
        tmpVals = [x.ime for x in bodyList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        body1['values'] = tmpVals
        body1.grid(row=4, column=1, padx=10, pady=10)
        body1.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body1PH, bodyList, "body1"))

        body2Txt = Label(parent, text="Second Chasis slot:", width=25, height=3)
        body2Txt.grid(row=3, column=3, padx=10, pady=10)
        body2PH = StringVar(parent, self.chestB.ime if isinstance(self.chestB,
                                                                  (MechWeapon, Module)) else self.chestB if isinstance(
            self.chestB, str) else None)
        body2 = Combobox(parent, textvariable=body2PH, state="readonly", width=25)
        body2['values'] = tmpVals
        body2.grid(row=4, column=3, padx=10, pady=10)
        body2.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body2PH, bodyList, "body2"))

        body3Txt = Label(parent, text="Third Chasis slot:", width=25, height=3)
        body3Txt.grid(row=7, column=1, padx=10, pady=10)
        body3PH = StringVar(parent, self.chestC.ime if isinstance(self.chestC,
                                                                  (MechWeapon, Module)) else self.chestC if isinstance(
            self.chestC, str) else None)
        body3 = Combobox(parent, textvariable=body3PH, state="readonly", width=25)
        body3['values'] = tmpVals
        body3.grid(row=8, column=1, padx=10, pady=10)
        body3.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body3PH, bodyList, "body3"))

        body4Txt = Label(parent, text="Fourth Chasis slot:", width=25, height=3)
        body4Txt.grid(row=7, column=3, padx=10, pady=10)
        body4PH = StringVar(parent, self.chestD.ime if isinstance(self.chestD,
                                                                  (MechWeapon, Module)) else self.chestD if isinstance(
            self.chestD, str) else None)
        body4 = Combobox(parent, textvariable=body4PH, state="readonly", width=25)
        body4['values'] = tmpVals
        body4.grid(row=8, column=3, padx=10, pady=10)
        body4.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(body4PH, bodyList, "body4"))

        core1Txt = Label(parent, text="First Core slot:", width=25, height=3)
        core1Txt.grid(row=5, column=1, padx=10, pady=10)
        core1PH = StringVar(parent, self.coreA.ime if self.coreA else None)
        core1 = Combobox(parent, textvariable=core1PH, state="readonly", width=25)
        tmpVals = [x.ime for x in coreModList] + [""]
        core1['values'] = tmpVals
        core1.grid(row=6, column=1, padx=10, pady=10)
        core1.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(core1PH, coreModList, "core1"))

        core2Txt = Label(parent, text="Second Core slot:", width=25, height=3)
        core2Txt.grid(row=5, column=3, padx=10, pady=10)
        core2PH = StringVar(parent, self.coreB.ime if self.coreB else None)
        core2 = Combobox(parent, textvariable=core2PH, state="readonly", width=25)
        core2['values'] = tmpVals
        core2.grid(row=6, column=3, padx=10, pady=10)
        core2.bind("<<ComboboxSelected>>",
                   lambda e: self.comboBoxReturnObject(core2PH, coreModList, "core2"))

        rLegTxt = Label(parent, text="Right Leg slot:", width=25, height=3)
        rLegTxt.grid(row=9, column=1, padx=10, pady=10)
        rLegPH = StringVar(parent,
                           self.rLeg.ime if isinstance(self.rLeg, (MechWeapon, Module)) else self.rLeg if isinstance(
                               self.rLeg, str) else None)
        rLeg = Combobox(parent, textvariable=rLegPH, state="readonly", width=25)
        tmpVals = [x.ime for x in legList]
        tmpVals.extend(["Armor", "Ammo Rack", ""])
        rLeg['values'] = tmpVals
        rLeg.grid(row=10, column=1, padx=10, pady=10)
        rLeg.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(rLegPH, legList, "rLeg"))

        lLegTxt = Label(parent, text="Left Leg slot:", width=25, height=3)
        lLegTxt.grid(row=9, column=3, padx=10, pady=10)
        lLegPH = StringVar(parent,
                           self.lLeg.ime if isinstance(self.lLeg, (MechWeapon, Module)) else self.lLeg if isinstance(
                               self.lLeg, str) else None)
        lLeg = Combobox(parent, textvariable=lLegPH, state="readonly", width=25)
        lLeg['values'] = tmpVals
        lLeg.grid(row=10, column=3, padx=10, pady=10)
        lLeg.bind("<<ComboboxSelected>>", lambda e: self.comboBoxReturnObject(lLegPH, legList, "lLeg"))

        coreTxt = Label(parent, text="Core:", width=25, height=3)
        coreTxt.grid(row=5, column=2, padx=10, pady=10)
        coreTypePH = StringVar(parent, self.core.ime if self.core else None)
        core = Combobox(parent, textvariable=coreTypePH, state="readonly", width=25)
        tmpVals = [x.ime for x in coreList]
        core['values'] = tmpVals
        core.grid(row=6, column=2, padx=10, pady=10)
        core.bind("<<ComboboxSelected>>",
                  lambda e: self.comboBoxReturnObject(coreTypePH, coreList, "core"))

        def btn_func():
            self.comboBoxReturnObject(rHaPH, armList, "rHa")
            self.comboBoxReturnObject(lHaPH, armList, "lHa")
            self.comboBoxReturnObject(rShPH, shoulderList, "rSh")
            self.comboBoxReturnObject(lShPH, shoulderList, "lSh")
            self.comboBoxReturnObject(body1PH, bodyList, "body1")
            self.comboBoxReturnObject(body2PH, bodyList, "body2")
            self.comboBoxReturnObject(body3PH, bodyList, "body3")
            self.comboBoxReturnObject(body4PH, bodyList, "body4")
            self.comboBoxReturnObject(core1PH, coreModList, "core1")
            self.comboBoxReturnObject(core2PH, coreModList, "core2")
            self.comboBoxReturnObject(rLegPH, legList, "rLeg")
            self.comboBoxReturnObject(lLegPH, legList, "lLeg")
            self.comboBoxReturnObject(coreTypePH, coreList, "core")
            self.saveEdit(parent, grandParent)

        save=Button(parent, text="Save preset", command=btn_func)
        save.grid(row=11, column=0, padx=5, pady=5)
        saveWarning=Label(parent, text="Warning! This will overwrite your current setup!", wraplength=150, font=("Arial",10,"bold"))
        saveWarning.grid(row=12, column=0, padx=5, pady=5)
        cancel = Button(parent, text="cancel editing", command=lambda: self.showDetails(grandParent))
        cancel.grid(row=11, column=1, padx=5, pady=5)
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

        if flag == "rHa":
            self.newTmpSlots[4] = spremam
        elif flag == "lHa":
            self.newTmpSlots[3] = spremam
        elif flag == "rSh":
            self.newTmpSlots[2] = spremam
        elif flag == "lSh":
            self.newTmpSlots[1] = spremam
        elif flag == "body1":
            self.newTmpSlots[7] = spremam
        elif flag == "body2":
            self.newTmpSlots[8] = spremam
        elif flag == "body3":
            self.newTmpSlots[9] = spremam
        elif flag == "body4":
            self.newTmpSlots[10] = spremam
        elif flag == "core1":
            self.newTmpSlots[5] = spremam
        elif flag == "core2":
            self.newTmpSlots[6] = spremam
        elif flag == "lLeg":
            self.newTmpSlots[11] = spremam
        elif flag == "rLeg":
            self.newTmpSlots[12] = spremam
        elif flag == "core":
            self.newTmpSlots[0] = spremam

        return

    def saveEdit(self, parent, grandParent):
        self.core=self.newTmpSlots[0]
        self.lSh=self.newTmpSlots[1]
        self.rSh=self.newTmpSlots[2]
        self.lArm=self.newTmpSlots[3]
        self.rArm=self.newTmpSlots[4]
        self.coreA=self.newTmpSlots[5]
        self.coreB=self.newTmpSlots[6]
        self.chestA=self.newTmpSlots[7]
        self.chestB=self.newTmpSlots[8]
        self.chestC=self.newTmpSlots[9]
        self.chestD=self.newTmpSlots[10]
        self.lLeg=self.newTmpSlots[11]
        self.rLeg=self.newTmpSlots[12]
        for i in range(len(self.slots)):
             self.slots[i]=self.newTmpSlots[i]
        self.setDerivedStats()
        self.showLoadoutDetails(parent, grandParent)
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

        breakReduction = 0
        for mod in self.slots:
            if isinstance(mod, Module):
                if mod.ime=="auto repair protocols":
                    breakReduction=2
                    break
                elif mod.ime=="auto repair protocols Mk.2":
                    breakReduction = 4
                    break

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
        repair = Button(healthFrame, text="Repair", command=lambda: hp_f(int(changeEntry.get()), 1, hp))
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

        modstit=Label(parent, text="Modules, Weapons and Cores", font=("Arial",13,"bold"))
        modstit.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        equipmentFrame = Frame(parent)
        equipmentFrame.grid(row=4, column=0, columnspan=3)
        i=0
        for elem in self.slots:
            if isinstance(elem, (MechWeapon, Module, Core)):
                frame = Frame(equipmentFrame)
                elem.showCombatScreen(frame, breakReduction)
                r=i//4
                c=i%4
                frame.grid(row=r, column=c, padx=5, pady=25)
                i+=1

        return

    def delete(self):
        try:
            podatci.PLAYER_MECHS.remove(self)
        except ValueError:
            print("Couldn't remove requested entity.")
        return
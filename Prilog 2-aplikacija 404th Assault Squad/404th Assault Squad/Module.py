from tkinter import *

import podatci as podatci


class Module:
    cdCmbtStatus = ["Ready", "Ready in 1 encounter", "Ready in 2 encounters"]
    cmbtCooldown = [""]

    def __init__(self, ime, tier, tip, slot, mount, requirement, effect, cooldown, duration, uses, upgrades):
        self.ime = ime
        self.tier = int(tier)
        self.tip = tip
        self.slot = slot
        self.mount = mount
        self.requirement = requirement
        self.effect = effect
        self.cooldown = None if not cooldown.isdigit() else int(cooldown)
        self.duration = None if not duration.isdigit() else int(duration)
        # -1 use for inf uses (CD only modules)
        self.uses = -1 if not uses.isdigit() else int(uses)
        self.upgrades = upgrades
        self.startCD = False
        self.reset()
        return

    def reset(self):
        self.usesRemaining = self.uses
        self.cdRemaining = 0
        self.cdCmbtRemaining = 0
        self.durRemaining = 0
        return

    def activate(self):
        if (self.cdRemaining == 0 or self.cdCmbtRemaining == 0) and self.usesRemaining != 0:
            if self.cooldown is not None:
                self.cdRemaining = self.cooldown
                self.cdCmbtRemaining = self.cooldown
            if self.duration is not None:
                self.durRemaining = self.duration
            elif self.cooldown:
                self.startCD=True
            if self.usesRemaining > 0:
                self.usesRemaining -= 1
        return

    def startCooldown(self):
        if self.duration: self.durRemaining=0
        if self.cooldown: self.cdRemaining=self.cooldown
        self.startCD=True
        return

    def breakF(self, label, info, reduction=0):
        print("breaking {}".format(self.ime))
        self.durRemaining=0
        turnsToFix=(2*self.cooldown)-reduction if self.cooldown is not None else 7-reduction if self.mount=="mech" else 5
        if turnsToFix<1:
            turnsToFix=1
        self.cdRemaining=turnsToFix
        self.startCD=True
        info[0].set(self.durRemaining)
        info[1].set(turnsToFix)
        info[2].set(self.usesRemaining if self.uses>0 else "unlimited")
        label['text']="Duration remaining(turns): {}\nCooldown remaining (turns/encounters): {}\nUses remaining: {}".format(info[0].get(), info[1].get(), info[2].get())
        return

    def endTurn(self):
        if self.durRemaining > 0:
            self.durRemaining -= 1
            if self.durRemaining == 0:
                self.startCD = True
        elif self.cdRemaining>0 and self.startCD is True:
            self.cdRemaining -= 1
        else:
            self.cdRemaining=0
            self.durRemaining=0
        return

    def endCombat(self):
        if self.durRemaining > 0:
            self.durRemaining = 0
        if self.ime in self.cmbtCooldown and self.cdCmbtRemaining > 0 and self.startCD is True:
            self.cdCmbtRemaining -= 1
        else:
            self.cdRemaining = 0
        return

    def showDetails(self, parent):
        name_list = [x.ime for x in podatci.MODULES]
        try:
            mod_id = 1 + name_list.index(self.ime)
        except ValueError:
            mod_id = -1

        tiertxt = "Tier {} {} {} module: [{}] {}".format(self.tier, self.tip, self.mount, mod_id, self.ime)
        tier = Label(parent, text=tiertxt, justify=LEFT, anchor="w", wraplength=600)
        tier.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        reqtxt = "Requirement to equip: {}".format(self.requirement)
        req = Label(parent, text=reqtxt, justify=LEFT, anchor="w", wraplength=300)
        req.grid(row=0, column=2, padx=5, pady=5)

        effecttxt = "Effect: {}".format(self.effect)
        effect = Label(parent, text=effecttxt, justify=LEFT, anchor="w", wraplength=700)
        effect.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

        usagetxt = ""
        if self.duration:
            usagetxt += "Duration: {} (turns)\n".format(self.duration)
        else:
            usagetxt += "Infinite (toggle) duration or instant activation.\n"
        if self.cooldown:
            usagetxt += "Cooldown: {} (turns)\n".format(self.cooldown)
        else:
            usagetxt += "No cooldown.\n"
        if self.uses > 0:
            usagetxt += "Uses: {} (ammount per Mech deployment)\n".format(self.uses)
        else:
            usagetxt += "Infinite uses.\n"
        usage = Label(parent, text=usagetxt, justify=LEFT, anchor="w", wraplength=300)
        usage.grid(row=0, column=3, padx=5, pady=5, rowspan=2)
        return

    def showCombatScreen(self, parent, reduction):
        def change_f(label, flag):
            if flag=="act":
                self.activate()
            elif flag=="cd":
                self.startCooldown()
            elif flag=="add":
                self.usesRemaining+=1

            durVal.set(self.durRemaining)
            cdVal.set(self.cdRemaining if self.cooldown is not None or self.cdRemaining!=0 else self.cdCmbtRemaining if self.ime in self.cmbtCooldown else "no cooldown")
            useVal.set(self.usesRemaining if self.uses>0 else "unlimited")
            label['text']="Duration remaining(turns): {}\nCooldown remaining (turns/encounters): {}\nUses remaining: {}".format(durVal.get(), cdVal.get(), useVal.get())

        ime = Label(parent, text=self.ime, wraplength=500, justify=LEFT)
        ime.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        durVal=StringVar(parent, self.durRemaining)
        cdVal = StringVar(parent, self.cdRemaining if self.cooldown is not None or self.cdRemaining!=0 else self.cdCmbtRemaining if self.ime in self.cmbtCooldown else "no cooldown")
        useVal = StringVar(parent, self.usesRemaining if self.uses>0 else "unlimited")
        durationtxt="Duration remaining(turns): {}\nCooldown remaining (turns/encounters): {}\nUses remaining: {}".format(durVal.get(), cdVal.get(), useVal.get())
        duration=Label(parent, text=durationtxt, wraplength=200, justify=LEFT)
        duration.grid(row=1, column=0, padx=5, pady=5, rowspan=2)
        activate=Button(parent, text="Activate", command=lambda: change_f(duration, "act"))
        activate.grid(row=1, column=1, padx=5, pady=5)
        cooldown=Button(parent, text="Start Cooldown", command=lambda: change_f(duration, "cd"))
        cooldown.grid(row=2, column=1, padx=5, pady=5)
        adduse = Button(parent, text="Add 1 use", state="disabled" if self.uses == -1 else "normal",
                           command=lambda: change_f(duration, "add"))
        adduse.grid(row=3, column=1, padx=5, pady=5)
        breakBtn = Button(parent, text="Jam", width=20, command=lambda : self.breakF(duration, [durVal,cdVal,useVal], reduction))
        breakBtn.grid(row=4, column=0, pady=5)
        return


################ CORE class ###########################################################################################

class Core:
    def __init__(self, ime):
        self.ime = ime
        self.powerMax = 4 if self.ime == "standard" else -1
        self.reset()
        return

    def reset(self):
        self.powerCurr = self.powerMax
        self.percent=int(self.powerCurr / self.powerMax * 100)
        return

    def changeMaxPower(self,ammount=0):
        if self.ime=="standard":
            self.powerMax=4+ammount
            self.reset()
        return

    def endCombat(self):
        if self.powerMax > 0:
            self.powerCurr -= 1
            self.percent = int(self.powerCurr / self.powerMax * 100)
        if self.powerCurr == 0:
            print("Mech has lost power.")

    def showDetails(self, parent):
        imetxt = "Type: {}".format(self.ime)
        tier = Label(parent, text=imetxt, justify=LEFT, anchor="w")
        tier.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        powertxt = "Current core power: {}%".format(self.percent) if self.ime == "standard" else "Nuclear cores provide unlimited " \
                                                                                 "ammount of power to the mech. "
        power = Label(parent, text=powertxt, justify=LEFT, anchor="w")
        power.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        effecttxt = "Some modules can only be powered by specific cores. While standard issue cores provide limited " \
                    "power, they are less dangerous to the pilot and nearby soldiers.\nOn the other side nuclear " \
                    "cores provide unlimited ammounts of power and offer a unique way to use a Mech as a weapon. "
        effect = Label(parent, text=effecttxt, justify=LEFT, anchor="w")
        effect.grid(row=1, column=0, padx=5, pady=5, columnspan=3)
        return

    def showCombatScreen(self, parent, reduction):
        def percent_f(label):
            chargetxt = "Power remaining: "
            if self.ime == "nuclear":
                chargetxt += "unlimited"
            else:
                chargetxt += "{}%".format(self.percent)
            label['text']=chargetxt

        def add_f(label):
            self.powerCurr+=1
            self.percent = int(self.powerCurr / self.powerMax * 100)
            percent_f(label)

        imetxt="Core type: {}".format(self.ime)
        ime=Label(parent, text=imetxt)
        ime.grid(row=0, column=0, padx=5, pady=5)
        charge=Label(parent)
        percent_f(charge)
        charge.grid(row=1, column=0, padx=5, pady=5)
        addCharge=Button(parent, text="Add 1 charge", state="disabled" if self.ime=="nuclear" else "normal", command=lambda: add_f(charge))
        addCharge.grid(row=1, column=1, padx=5, pady=5)
        return

from tkinter import *
from tkinter.ttk import Separator

import podatci as podatci


class PilotWeapon:
    reloadStatus = ["Ready", "Need to reload"]

    def __init__(self, ime, tier, weaponClass, damage, range, ammoType, reserves, magazine, shotsPerAtt, targetsPerAtt,
                 reload, upgrade):
        self.ime = ime
        self.tier = tier
        self.weaponClass = weaponClass
        self.damage = damage
        self.range = range
        self.ammoType = ammoType
        self.reserves = None if not reserves.isdigit() else int(reserves)
        self.magazine = None if not magazine.isdigit() else int(magazine)
        self.shotsPerAtt = None if not shotsPerAtt.isdigit() else int(shotsPerAtt)
        self.targetsPerAtt = None if not targetsPerAtt.isdigit() else int(targetsPerAtt)
        self.reload = None if not reload.isdigit() else int(reload)
        self.upgrade = upgrade
        self.broken = False
        self.setDerivedStats()
        return

    def setDerivedStats(self):
        self.reloadProgress = 0
        try:
            self.magazineRemaining = self.magazine
            self.shotsPerMag = int(self.magazine / self.shotsPerAtt)
            self.shotsPerMagRemaining = self.shotsPerMag
        except (TypeError, AttributeError):
            pass
        return

    def fire(self):
        if not self.broken:
            try:
                if self.reloadProgress != 0:
                    print(self.reloadStatus[self.reloadProgress])
                    return
                elif self.magazineRemaining == 0:
                    print("guns dry")
                    return
                else:
                    self.magazineRemaining -= self.shotsPerAtt
                    self.shotsPerMagRemaining -= 1
                    if self.magazineRemaining==0:
                        self.reloadProgress=1
                    return
            except TypeError:
                pass
        return

    def reloadFunc(self):
        print("ayo {}".format(self.reloadProgress))
        if not self.broken:
            try:
                if self.reloadProgress != 1:
                    print(self.reloadStatus[self.reloadProgress])
                elif self.magazineRemaining != 0:
                    print("you would loose the rest of the ammo")
                else:
                    self.reserves -= 1
                    self.magazineRemaining = self.magazine
                    self.shotsPerMagRemaining = self.shotsPerMag
                    self.reloadProgress=0
            except TypeError:
                pass
        return

    def breakF(self, label, reduction=0):
        self.broken=True
        label['text']=self.ime+" - JAMMED"
        return

    def fixF(self, label):
        self.broken=False
        label['text'] = self.ime
        return

    def showDetails(self, parent):
        name_list=[x.ime for x in podatci.PILOT_WEAPONS ]
        try:
            weap_id=1+name_list.index(self.ime)
        except ValueError:
            weap_id=-1
        idtxt = "[{}] {}".format(weap_id, self.ime)
        idl = Label(parent, text=idtxt, justify=LEFT, anchor="w", wraplength=300)
        idl.grid(row=0, column=0, padx=5, pady=5)

        tiertxt = "Weapon tier: {}".format(self.tier)
        tier = Label(parent, text=tiertxt, justify=LEFT, anchor="w", wraplength=300)
        tier.grid(row=0, column=1, padx=5, pady=5)

        classtxt = "Weapon class: {}".format(self.weaponClass)
        class_ = Label(parent, text=classtxt, justify=LEFT, anchor="w", wraplength=300)
        class_.grid(row=0, column=2, padx=5, pady=5)

        dmgrangetxt = "Damage: {}\n\nMaximum range: {}".format(self.damage, self.range)
        dmg = Label(parent, text=dmgrangetxt, justify=LEFT, anchor="w", wraplength=300)
        dmg.grid(row=0, column=3, padx=5, pady=5)

        ammotxt = "Ammo type: {}\n\nMagazine : {}/{}\n\nBase magazine reserves size: {}\n\nReload status: {}".format(
            self.ammoType, self.magazineRemaining, self.magazine, self.reserves, self.reloadStatus[self.reloadProgress])
        ammo = Label(parent, text=ammotxt, justify=LEFT, anchor="w", wraplength=300)
        ammo.grid(row=0, column=4, rowspan=2, padx=5, pady=5)

        if self.shotsPerAtt:
            attacktxt = "Weapon fires {} shot(s) out of its' magazine per attack and can hit {} target(s) in that " \
                        "attack. That means the weapon can fire {} time(s) from a full magazine without " \
                        "reloading.".format(self.shotsPerAtt, self.targetsPerAtt, self.shotsPerMag)
            attack = Label(parent, text=attacktxt, justify=LEFT, anchor="w", wraplength=600)
            attack.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        upgrade = LabelFrame(parent, text="Upgrades")
        lista = self.upgrade.split(" ")
        d = len(lista)
        if d >= 2:
            for i in range(0, d, 2):
                sep = Separator(upgrade, orient='horizontal')
                sep.grid(row=i+1, column=0, sticky="ew", columnspan=5)
                id_ = int(lista[i])
                cost = lista[i + 1][1:2]
                weapUpgradetxt = "{} at the cost of {} TECH points".format(name_list[id_-1], cost)
                weapUpgrade = Label(upgrade, text=weapUpgradetxt)
                weapUpgrade.grid(row=i, column=0, padx=5, pady=5)
        upgrade.grid(row=0, column=5, rowspan=2, padx=5, pady=5)
        return

    def showCombatScreen(self, parent, reduction):
        def reserve_f(flag, label):
            if flag == "d":
                self.reserves -= 1
            elif flag == "i":
                self.reserves += 1
            label['text'] = "Magazines in reserves: {}".format(self.reserves)
            print("reserves {}".format(self.reserves))

        def mag_f(flag, magLabel, reserveLabel, infoLabel):
            if flag == "f":
                self.fire()
                magLabel['text'] = "Magazine: {}/{} chambered {}\nAttacks left: {}/{}".format(self.magazineRemaining,
                                                                                               self.magazine,
                                                                                               self.ammoType,
                                                                                               self.shotsPerMagRemaining,
                                                                                               self.shotsPerMag)
                infoLabel['text'] = self.reloadStatus[self.reloadProgress]
                print("mag: {}/{}".format(self.magazineRemaining, self.magazine))
            elif flag == "r":
                self.reloadFunc()
                magLabel['text'] = "Magazine: {}/{} chambered {}\nAttacks left: {}/{}".format(self.magazineRemaining,
                                                                                                self.magazine,
                                                                                                self.ammoType,
                                                                                                self.shotsPerMagRemaining,
                                                                                                self.shotsPerMag)
                reserveLabel['text'] = "Magazines in reserves: {}".format(self.reserves)
                infoLabel['text'] = self.reloadStatus[self.reloadProgress]
                print("mag: {}/{}".format(self.magazineRemaining, self.magazine))

        ime = Label(parent, text=self.ime, wraplength=600, justify=LEFT)
        ime.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        dmgtxt = "Damage: {}, Range: {}".format(self.damage, self.range)
        damage = Label(parent, text=dmgtxt, wraplength=200, justify=LEFT)
        damage.grid(row=1, column=0, padx=5, pady=5)
        fire = Button(parent, text="Fire Weapon", command=lambda: mag_f("f", mag, reserves, reloadStatus))
        fire.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        magtxt = "Magazine: {}/{} chambered {}\nAttacks left: {}/{}".format(self.magazineRemaining, self.magazine,
                                                                              self.ammoType, self.shotsPerMagRemaining,
                                                                              self.shotsPerMag)
        mag = Label(parent, text=magtxt, wraplength=500, justify=LEFT)
        mag.grid(row=2, column=0, padx=5, pady=5)
        reload = Button(parent, text="Reload", width=10, command=lambda: mag_f("r", mag, reserves, reloadStatus))
        reload.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        reloadVar = StringVar(parent, self.reloadStatus[self.reloadProgress])
        reloadStatus = Label(parent, text=reloadVar.get())
        reloadStatus.grid(row=2, column=3, padx=5, pady=5)
        reserveVal = IntVar(parent, self.reserves)
        reservetxt = "Magazines in reserves: {}".format(reserveVal.get())
        reserves = Label(parent, text=reservetxt)
        reserves.grid(row=3, column=0, padx=5, pady=5)
        decReserves = Button(parent, text="-", width=3, command=lambda: reserve_f("d", reserves))
        decReserves.grid(row=3, column=1, padx=5, pady=5)
        incReserves = Button(parent, text="+", width=3, command=lambda: reserve_f("i", reserves))
        incReserves.grid(row=3, column=2, padx=5, pady=5)
        breakBtn = Button(parent, text="Jam", width=20,
                          command=lambda: self.breakF(ime, reduction))
        breakBtn.grid(row=4, column=0, pady=5)
        fixBtn = Button(parent, text="Unjam", width=15, command=lambda :self.fixF(ime))
        fixBtn.grid(row=4, column=1, columnspan=3, pady=5)
        return

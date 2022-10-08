from EnemyPilot import *
from EnemyMech import *
from PlayerPilot import *
from PlayerMech import *
from Module import *
from PilotWeapon import *
from MechWeapon import *

file = open("C:\\Users\\AntonioPC\\Desktop\\Tabletop\\404th Assault Squad\\export_mech_weapons.txt", "r")
fileOut=open("C:\\Users\\AntonioPC\\Desktop\\Tabletop\\404th Assault Squad\\code_output_mech_weapons.txt","w")

lista=[]
while True:
    line = file.readline()

    if not line:
        break

    tmp = line.rstrip("\n").split("\t")
    #print(tmp)
    #print(line)

    # ########### FOR EXPORTING MODULES
    # #                     ime,           tier,             tip,              slot,          mount,        requirement,     effect,      cooldown,  duration,    uses,        upgrades
    # lineToWrite="Module(\""+tmp[1]+"\", \""+tmp[11]+"\", \""+tmp[2]+"\", \""+tmp[3]+"\", \""+tmp[4]+"\", \""+tmp[5]+"\", \""+tmp[6]+"\", \""+tmp[7]+"\", \""+tmp[8]+"\", \""+tmp[9]+"\", \""+tmp[10]+"\"),\n"

    ########### FOR EXPORTING PILOT WEAPONS
    #                            ime,             tier,        weaponClass,      damage,          range,          ammoType,     reserves,      magazine,      shotsPerAtt,   targetsPerAtt,      reload,           upgrade
    #lineToWrite="PilotWeapon(\""+tmp[1]+"\", \""+tmp[12]+"\", \""+tmp[2]+"\", \""+tmp[3]+"\", \""+tmp[4]+"\", \""+tmp[5]+"\", \""+tmp[6]+"\", \""+tmp[7]+"\", \""+tmp[8]+"\", \""+tmp[9]+"\", \""+tmp[10]+"\", \""+tmp[11]+"\"),\n"

    ########### FOR EXPORTING MECH WEAPONS
    #                           ime,            tier,             slot,          damage,  weightClassPenalty,    range,        ammoType,       reserves,        magazine,    shotsPerAtt,    targetsPerAtt,     reloadTrns,        upgrade
    lineToWrite="MechWeapon(\""+tmp[1]+"\", \""+tmp[13]+"\", \""+tmp[2]+"\", \""+tmp[3]+"\", \""+tmp[4]+"\", \""+tmp[5]+"\", \""+tmp[6]+"\", \""+tmp[7]+"\", \""+tmp[8]+"\", \""+tmp[9]+"\", \""+tmp[10]+"\", \""+tmp[11]+"\", \""+tmp[12]+"\"),\n"

    fileOut.write(lineToWrite)

    lista.append(MechWeapon(tmp[1],tmp[13],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],tmp[9],tmp[10],tmp[11],tmp[12]))


print (lista[33].ime)
lista[33].endTurn()
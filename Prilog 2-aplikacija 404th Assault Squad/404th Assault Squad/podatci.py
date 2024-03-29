from Entitet import Entitet
from Environment import Environment
from MechWeapon import MechWeapon
from Module import Module, Core
from PilotWeapon import PilotWeapon

MODULES=[
    Module("night vision overlay", "1", "utility", "helmet", "suit", "available slot, 2 PER, 2 INT", "toggleable night vision(free action)", "-", "-", "-", "2 [1], 3 [2]"),
    Module("heat vision overlay", "1", "utility", "helmet", "suit", "available slot, 4 PER, 4 INT", "toggleable heat sensors(free action) that can detect heat signature of camouflaged units", "-", "-", "-", "1 [1], 3 [2]"),
    Module("electro-magnetic vision overlay", "2", "utility", "helmet", "suit", "available slot, 6 PER, 4 INT", "toggleable electro-magnetic sensors(free action) that can detect heat signature of camouflaged units", "-", "-", "-", "-"),
    Module("heat vision protocols", "2", "utility", "body", "mech", "available slot", "toggleable heat sensors(free action) that can detect heat signature of camouflaged units", "-", "-", "-", "5 [2]"),
    Module("electro-magnetic vision protocols", "2", "utility", "body", "mech", "available slot", "toggleable electro-magnetic sensors(free action) that can detect signature of camouflaged units", "-", "-", "-", "-"),
    Module("sabilizers", "1", "utility", "both legs", "mech", "available slots", "+1 turn before artilery can be fired the first time,  afterwards negates recoil wait time, harder to get knocked back while holding a shield", "-", "until retracted", "-", "11 [4]"),
    Module("mine detection protocols", "1", "utility", "leg", "mech", "available slots", "detects metal mines in a range of 3", "3", "instant", "-", "-"),
    Module("anti-pest protocols", "1", "utility", "body", "mech", "available slots", "sends a shock pulse through the rig immidiately dropping all creatures that are holding onto the mech or are manning the external weaponry and stunning them (not the pilot in control)", "3", "1", "-", "9 [2]"),
    Module("extended anti-pest protocols", "2", "utility", "body", "mech", "available slots", "sends a shock pulse through the rig immidiately dropping all creatures that are holding onto the mech or are manning the external weaponry and stunning them, also stuns everything within 1 range (not the pilot in control, excluding other mechs)", "5", "1", "-", "-"),
    Module("auto repair protocols", "1", "utility", "body", "mech", "available slots", "-2 turns to repairing broken modules", "-", "-", "-", "40 [2]"),
    Module("fast stabilizers", "2", "utility", "both legs", "mech", "available slots", "first artilery shot takes normal ammount of turns to fire, afterwards negates recoil wait time, harder to get knocked back while holding a shield", "-", "until retrackted", "-", "-"),
    Module("anti-intruder protocols", "1", "utility", "body", "mech", "available slots", "prevents mech hijack by binding mech's controls to the pilot's suit", "-", "-", "-", "-"),
    Module("self-distruct protocols", "1", "core", "core", "mech", "available slot, nuclear core", "pilot can initiate self distruct", "-", "-", "-", "14 [2], 15 [5]"),
    Module("remote self-destruct protocols", "2", "core", "core", "mech", "available slot, nuclear core", "pilot can initiate self distruct remotely through omni-tool", "-", "-", "-", "15 [3]"),
    Module("self-distruct payload protocols", "3", "core", "core", "mech", "available slot, nuclear core", "pilot can launch a mech in a desired direction before self-distruction before the pilot ejects", "-", "-", "-", "-"),
    Module("reinforced core hatch", "1", "utility", "body", "mech", "available slots", "makes it harder to reach the core from the outside of the mech", "-", "-", "-", "-"),
    Module("survival instinct", "1", "utility", "chest", "suit", "available slot, 5 END, 3 INT, 3 STR", "when HP drops below 10 suit knocks out the pilot to possibly prevent fatal damage", "-", "-", "-", "18 [3]"),
    Module("survival instinct Mk.2", "2", "utility", "chest", "suit", "available slot, 7 END, 3 INT, 5 STR", "when HP drops below a set ammount of HP (player setting) suit knocks out the pilot to possibly prevent fatal damage, pilot can trigger the effect preemptively", "-", "-", "-", "-"),
    Module("jet pack", "1", "utility", "back", "suit", "available slot, 3 AGI", "it's a jet pack… movement has +1 range", "-", "-", "3", "-"),
    Module("parachute", "1", "utility", "back", "suit", "available slot", "it's a parachute…", "6", "-", "-", "-"),
    Module("stabilizer jets", "1", "utility", "legs", "suit", "available slot, 2 AGI", "prevents fall damage", "-", "-", "-", "-"),
    Module("jet propulsion", "1", "utility", "both shoulders", "mech", "available slot, standard core", "it's a jet pack… for mechs… movement has +1 range", "-", "-", "2", "-"),
    Module("targeting overlay", "1", "utility", "helmet", "suit", "available slot, 6 PER", "+1 to hit-chance rolls, toggleable", "-", "-", "-", "24 [2]"),
    Module("adv. targeting overlay", "2", "utility", "helmet", "suit", "available slot, 9 PER", "+2 to hit-chance rolls, toggleable", "-", "-", "-", "-"),
    Module("helmet camera", "1", "utility", "helmet", "suit", "available slot", "allows HQ to have a visual feed and provide tactical help", "-", "-", "-", "-"),
    Module("mine sweeper", "1", "utility", "omni-tool", "suit", "available slot, 3 AGI", "detects mine in the range of 1", "1", "-", "-", "-"),
    Module("hacking module", "1", "utility", "omni-tool", "suit", "available slot, 4 INT", "hacks minor locks", "3", "-", "-", "28 [2], 29 [5]"),
    Module("adv. hacking module", "2", "utility", "omni-tool", "suit", "available slot, 7 INT", "hacks advanced locks, hacks adjecent module, INT roll", "4", "-", "-", "29 [3]"),
    Module("expert hacking module", "3", "utility", "omni-tool", "suit", "available slot, 9 INT", "hacks almost any lock, hack adjecent mechs and modules, no roll required", "5", "-", "-", "-"),
    Module("remote hacking module upgrade", "4", "utility", "omni-tool", "suit", "+1 INT to base requirements", "add a range of 2 to equipped hacking module, can hack mechanical equipment", "+1 to base cooldown", "2", "-", "upgrades existing one for [2]"),
    Module("active camo", "1", "utility", "chest", "suit", "available slot, 2 INT, 6 AGI", "visually masks the pilot, attacking or otherwise revealing yourself ends the effect", "3", "2", "-", "33 [2]"),
    Module("active camo protocols", "1", "utility", "body", "mech", "available slot", "visually masks the mech, attacking or otherwise revealing yourself ends the effect", "5", "2", "-", "34 [2]"),
    Module("extended active camo", "2", "utility", "chest", "suit", "available slot, 2 INT, 6 AGI", "visually masks the pilot for an extended period, attacking or otherwise revealing yourself ends the effect", "3", "3", "-", "-"),
    Module("extended active camo protocols", "2", "utility", "body", "mech", "available slot", "visually masks the mech for an extended period, attacking or otherwise revealing yourself ends the effect", "5", "3", "-", "-"),
    Module("heat emission reduction", "1", "utility", "back", "suit", "available slot", "coolants in the suit adjust the temperature emmissions to match the external temperature", "3", "2", "-", "36 [2]"),
    Module("extended heat emission reduction", "2", "utility", "back", "suit", "available slot", "coolants in the suit adjust the temperature emmissions to match the external temperature, extended duration", "3", "3", "-", "-"),
    Module("heat emission reduction protocols", "1", "utility", "body", "mech", "available slot", "coolants in the mech's core adjust the temperature emmissions to match the external temperature", "5", "2", "-", "38 [2]"),
    Module("extended heat emission reduction protocols", "2", "utility", "body", "mech", "available slot", "coolants in the mech's core adjust the temperature emmissions to match the external temperature, extended duration", "5", "3", "-", "-"),
    Module("upgraded firewall", "1", "utility", "body", "mech", "available slot", "prevents a mech from being disabled through hacking", "-", "-", "-", ""),
    Module("auto repair protocols Mk.2", "2", "utility", "body", "mech", "available slot", "-4 turns for repairing, up to minimum of 1 turn", "-", "-", "-", "-"),
    Module("Guardian angels", "1", "utility", "shoulder", "mech", "available slot", "launches 1 small drone that orbits the mech, drone intercepts incoming rockets and grenades", "3", "until destroyed", "-", "42 [2], 43 [3]"),
    Module("Guardian angels Mk.2", "2", "utility", "shoulder", "mech", "available slot", "launches 3 small drones that orbits the mech, drones intercepts incoming rockets and grenades", "4", "until destroyed", "-", "43 [1]"),
    Module("Guardian angels Mk.3", "3", "utility", "shoulder", "mech", "available slot, nuclear core", "launches 5 small drones that orbits the mech, drones intercepts incoming rockets and grenades", "5", "until destroyed", "-", "-"),
    Module("R.A.T. drone", "1", "utility", "shoulder and body", "mech", "available slots", "deployes a Recon Assault and Tactical drone, drone has customizeable 2 utility/drone slots", "-", "until destroyed or recalled", "1", "-"),
    Module("R.A.T. explosive payload", "1", "drone", "drone", "drone", "available slot", "drone carries an explosive payload that can be remotely detonated from inside the mech", "-", "-", "-", "-"),
    Module("R.A.T. medical dispenser", "1", "drone", "drone", "drone", "available slot", "drone can inject a stim into the target", "2", "instant", "2", "-"),
    Module("R.A.T. tazer", "1", "drone", "drone", "drone", "available slot", "drone can stun a target", "4", "instant", "2", "-"),
    Module("smoke grenade launcer", "1", "utility", "shoulder/leg", "mech", "available slot", "can launch a smoke grenade in a range of 3", "4", "3", "2", "49 [1]"),
    Module("smoke grenade launcer Mk.2", "2", "utility", "shoulder/leg", "mech", "available slot", "can launch 2 smoke grenades at once in a range of 3", "6", "3", "2", "-"),
    Module("Beacon launcher", "1", "utility", "shoulder/leg", "mech", "available slot", "launches 1 beacon that calls in a supply crate after 2 turns", "-", "-", "1", "51 [1]"),
    Module("Beacon launcher Mk.2", "2", "utility", "shoulder/leg", "mech", "available slot", "launches 1 beacon that calls in a supply crate after 2 turns", "2 combats", "-", "-", "-"),
    Module("Hook launcher", "1", "utility", "omni-tool", "suit", "available slot, 7 AGI, 4 PER", "launch a 2 range hook on a steel chord, can be reeled in at will (enemies can unhook themselves in 1 action)", "3", "-", "-", "53 [2]"),
    Module("Shock Hook launcher", "2", "utility", "omni-tool", "suit", "available slot, 7 AGI, 4 PER,       3 INT", "launch a 2 range hook on a steel chord that shocks organics on hit, stunning them for 1 turn (does not affect mechs), can be reeled in at will (enemies can unhook themselves in 1 action once the recover from stun)", "5", "1", "-", "-"),
    Module("Upgraded core capacitors", "1", "core", "core", "mech", "available slot, standard core", "core lasts for 5 combat encounters", "-", "5 combats", "-", "55 [4]"),
    Module("Upgraded core capacitors Mk.2", "2", "core", "core", "mech", "available slot, standard core", "core lasts for 6 combat encounters", "-", "6 combats", "-", "-"),
    Module("Reinforced core casing", "1", "core", "core", "mech", "available slot", "increases mech HP by 150, cannot have 2 core casings equipped in the same time", "-", "-", "-", "56 [5], 57 [10]"),
    Module("Reinforced core casing Mk.2", "2", "core", "core", "mech", "available slot", "increases mech HP by 250, cannot have 2 core casings equipped in the same time", "-", "-", "-", "57 [5]"),
    Module("Reinforced core casing Mk.3", "3", "core", "core", "mech", "available slot", "increases mech HP by 350, cannot have 2 core casings equipped in the same time", "-", "-", "-", "-"),
    Module("Overdrive", "1", "core", "core", "mech", "available slot, standard core", "+25% dmg, take 25% more damage, core overheats at the end of the duration, disabling the mech for 3 turns", "3", "3", "1", "-"),
    Module("Target analyzer", "1", "utility", "helmet", "suit", "available slot, 4 INT, 4 PER", "displays target's modules and weapons, requires visual of the target", "1", "-", "-", "61 [1]"),
    Module("Advanced Target analyzer", "2", "utility", "helmet", "suit", "available slot, 6 INT, 4 PER", "displays target's modules and their cooldowns as well as weapons and magazine contents, requires visual of the target", "1", "-", "-", "-"),
    Module("Turret conversion ", "1", "core", "core", "mech", "available slot", "converts a chosen shoulder weapon (except artilery) into a mannable turret, weapon cannot be fired by the mech (it needs a gunner), weapon shots use gunner's action and hit chance modifiers, gunners can be stunned by anti-pest protocols, turret can be hijacked, one module can convert 1 turret, 2 modules can be installed", "-", "-", "-", "-"),
    Module("Grenade rig", "1", "utility", "chest", "suit", "available slot, 2 STR", "provides 3 extra grenade slots", "-", "-", "-", "-"),
    Module("Grenade holders", "1", "utility", "legs", "suit", "available slot, 1 STR, 1 AGL", "provides 2 extra grenade slots", "-", "-", "-", "-"),
    Module("Extended ammo rig", "1", "utility", "chest", "suit", "available slot, 2 STR", "provides 5 extra magazine slots", "-", "-", "-", "-"),
    Module("Ammo rig", "1", "utility", "legs", "suit", "available slot, 1 STR, 1 AGL", "provides 2 extra magazine slots", "-", "-", "-", "-"),
    Module("Equipment Launcher", "1", "utility", "back", "suit", "available slot, 4 STR, 3 AGL", "launches grenades with +1 range and +3 PER ", "2", "-", "-", "-")
]

CORES=[
    Core("standard"),
    Core("nuclear")
]

PILOT_WEAPONS=[
    PilotWeapon("Handgun", "1", "handgun", "12", "3", "9mm", "4", "4", "1", "1", "1", "2 [1], 3 [2], 4 [1]"),
    PilotWeapon("Silenced handgun", "1", "handgun", "15", "3", "9mm", "4", "4", "1", "1", "1", "3 [1], 4 [1]"),
    PilotWeapon("Handgun Mk.2", "2", "handgun", "20", "3", "9mm", "4", "4", "1", "1", "1", "-"),
    PilotWeapon("Handgun ext. Mags", "1", "handgun", "12", "3", "9mm", "4", "6", "1", "1", "1", "3 [1], 2 [1]"),
    PilotWeapon("Revolver", "1", "handcannon", "17", "4", ".44 magnum", "3", "3", "1", "1", "1", "6 [2]"),
    PilotWeapon("Revolver Mk.2", "2", "handcannon", "25", "4", ".44 magnum", "3", "3", "1", "1", "1", "-"),
    PilotWeapon("Cheap shot (revolver)", "2", "handcannon", "12", "3", ".44 magnum", "3", "3", "1", "1", "1", "-"),
    PilotWeapon("Omni-Blade", "1", "omni-melee", "15", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "9 [1]"),
    PilotWeapon("Omni-Blade Mk.2", "2", "omni-melee", "30", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "-"),
    PilotWeapon("Hidden Blade", "1", "cybernetic-melee", "20", "1", "-", "-", "-", "-", "1", "-", "-"),
    PilotWeapon("Combart Knife", "1", "melee", "15", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "-"),
    PilotWeapon("Reinforced glove", "1", "melee", "10", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "-"),
    PilotWeapon("Power fist", "2", "melee", "20", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "14 [2]"),
    PilotWeapon("Power Fist Mk.2", "3", "melee", "40", "2", "-", "-", "-", "-", "flexible, always same dmg", "-", "-"),
    PilotWeapon("Parazon", "1", "cybernetic-melee", "20", "2", "-", "-", "-", "-", "1", "-", "-"),
    PilotWeapon("Katana", "1", "melee", "30", "1", "-", "-", "-", "-", "1", "-", "-"),
    PilotWeapon("SMG", "1", "SMG", "20", "4", "9mm", "3", "30", "10", "1", "1", "18 [1], 34 [2]"),
    PilotWeapon("SMG ext. Mags", "1", "SMG", "20", "4", "9mm", "2", "60", "10", "1", "1", "34 [1]"),
    PilotWeapon("Assault rifle", "1", "AR", "25", "4", "5.56", "2", "30", "10", "1", "1", "20 [2], 21 [1], 22 [2]"),
    PilotWeapon("Assault rifle Mk.2", "2", "AR", "40", "4", "5.56", "2", "30", "10", "1", "1", "-"),
    PilotWeapon("Semi Assault Rifle", "1", "AR", "18", "5", "5.56", "2", "7", "1", "1", "1", "22 [1]"),
    PilotWeapon("Scoped Assault Rifle", "2", "AR", "25", "6", "5.56", "2", "5", "1", "1", "1", "-"),
    PilotWeapon("Sniper rifle", "1", "sniper", "35", "6", "7.62", "2", "3", "1", "1", "1", "24 [3]"),
    PilotWeapon("Sniper rifle Mk.2", "2", "sniper", "50", "7", "7.62", "2", "3", "1", "1", "1", "-"),
    PilotWeapon("Anti-material Rifle", "3", "sniper", "70", "8", ".50", "3", "2", "1", "1", "2", "-"),
    PilotWeapon("Laser sniper", "3", "sniper", "40", "8", "MFC", "5", "1", "1", "1", "1", "-"),
    PilotWeapon("Shotgun", "1", "shotgun", "20", "3", "12 ga.", "4", "3", "1", "1", "1", "28 [2]"),
    PilotWeapon("Shotgun Mk.2", "2", "shotgun", "30", "3", "12 ga.", "4", "3", "1", "1", "1", "-"),
    PilotWeapon("Automatic shotgun", "2", "shotgun", "30", "3", "12 ga.", "2", "15", "5", "1", "1", "-"),
    PilotWeapon("Shell Shock (shotgun)", "2", "shotgun", "20", "3", "12 ga.", "3", "3", "1", "1", "1", "-"),
    PilotWeapon("Revolver shotgun", "2", "handcannon", "15", "3", "12 ga.", "3", "3", "1", "1", "1", "-"),
    PilotWeapon("Sawed-off", "1", "sawed-off", "26", "2", "12 ga.", "6", "2", "2", "1", "1", "-"),
    PilotWeapon("BOSG (ACOG)", "1", "shotgun", "35", "5", "12 ga. (slug)", "9", "1", "1", "1", "1", "-"),
    PilotWeapon("SMG Mk.2", "2", "SMG", "35", "4", "9mm", "3", "30", "10", "1", "1", "-"),
    PilotWeapon("Tracer rifle", "2", "AR", "30", "4", "5.56", "2", "30", "10", "1", "1", "-")
]

MECH_WEAPONS=[
    MechWeapon("Minigun", "1", "arm weapon/shoulder", "50", "50% dmg", "4", "5mm", "3", "99", "33", "1", "1 action", "14 [1], 15 [1], 16 [2]"),
    MechWeapon("Grenade launcher", "1", "arm weapon/shoulder", "100", "50% dmg, +4 AC", "4", "40mm grenades", "6", "1", "1", "1", "automatically reloads every turn (can be fired only once per turn)", "17 [2]"),
    MechWeapon("Projectable shield", "1", "arm weapon", "200", "-", "-", "shield core", "1", "-", "-", "-", "1 end of combat", "13 [2], 36 [1]"),
    MechWeapon("Automatic shotgun", "1", "arm weapon", "70", "50% dmg, +2 AC", "3", "20 ga.", "3", "20", "5", "1", "1 action", "18 [2], 19 [1]"),
    MechWeapon("Rocket launcher", "1", "shoulder", "120", "75% dmg, +1 AC", "6", "HE rocket", "4", "1", "1", "1", "1 action", "20 [1], 21 [3], 22 [4]"),
    MechWeapon("Cannon", "1", "shoulder", "150", "66% dmg, +3 AC", "6", "65mm shell", "5", "1", "1", "1", "2 actions", "23 [3]"),
    MechWeapon("Artilery cannon", "1", "both shoulder", "600", "-", "30", "120mm shell", "3", "1", "1", "1", "2", "-"),
    MechWeapon("Mech omni-blade", "1", "arm weapon", "50", "+5 AC", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "24 [1], 25 [2]"),
    MechWeapon("Flamer", "1", "arm weapon", "30", "200% dmg", "3", "flamer fuel", "5", "50", "25", "1", "1 action", "26 [2], 27 [1]"),
    MechWeapon("Laser cannon", "1", "arm weapon", "120", "25% dmg, +2 AC", "4", "micro fusion cell", "5", "1", "1", "1", "2 actions", "28 [2], 29 [2], 30 [4], 31 [4]"),
    MechWeapon("Artilery missle pod", "1", "both shoulder", "350", "-", "20", "hellfire missile", "0", "8", "8", "1", "5", "-"),
    MechWeapon("Micro missiles", "1", "shoulder", "30", "+3 AC", "5", "micro missile", "6", "3", "3", "1", "automatically reloads every turn (can be fired only once per turn)", "32 [2], 33 [4], 34 [1], 35 [3]"),
    MechWeapon("Projectable shield Mk.2", "2", "arm weapon", "300", "-", "-", "shield core", "1", "-", "-", "-", "1 end of combat", "-"),
    MechWeapon("Eco fire minigun", "1", "arm weapon/shoulder", "30", "50% dmg", "4", "5mm", "3", "100", "20", "1", "1 action", "15 [1], 16 [1]"),
    MechWeapon("Buy-out fire minigun", "1", "arm weapon/shoulder", "75", "50% dmg", "4", "5mm", "3", "100", "50", "1", "1 action", "14 [1], 16 [1]"),
    MechWeapon("Minigun Mk.2", "2", "arm weapon/shoulder", "75", "66% dmg", "4", "5mm", "3", "99", "33", "1", "1 action", "-"),
    MechWeapon("Grenade launcher Mk.2", "2", "arm weapon/shoulder", "160", "50% dmg, +4 AC", "5", "40mm grenades", "6", "1", "1", "1", "automatically reloads every turn (can be fired only once per turn)", "-"),
    MechWeapon("Automatic shotgun Mk.2", "2", "arm weapon", "100", "50% dmg, +2 AC", "3", "20 ga.", "3", "20", "5", "1", "1 action", "-"),
    MechWeapon("Automatic shotgun range upgrade", "1", "arm weapon", "70", "50% dmg, +2 AC", "4", "20 ga.", "3", "20", "5", "1", "1 action", "18 [1]"),
    MechWeapon("Rocket launcher AP adjustment", "1", "shoulder", "200", "20% dmg, +3 AC", "6", "AP rocket", "4", "1", "1", "1", "1 action", "5 [1], 21 [4], 22 [3]"),
    MechWeapon("Rocket launcher Mk.2", "2", "shoulder", "200", "75% dmg, +1 AC", "6", "HE rocket", "4", "1", "1", "1", "1 action", "-"),
    MechWeapon("Rocket launcher AP Mk.2", "2", "shoulder", "350", "20% dmg, +3 AC", "6", "AP rocket", "4", "1", "1", "1", "1 action", "-"),
    MechWeapon("Cannon Mk.2", "2", "shoulder", "250", "60% dmg, +3 AC", "6", "65mm shell", "5", "1", "1", "1", "2 actions", "-"),
    MechWeapon("Mech omni-blade Mk.2", "2", "arm weapon", "75", "+5 AC", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "25 [1]"),
    MechWeapon("Mech omni-blade Mk.3", "3", "arm weapon", "100", "+5 AC", "1", "-", "-", "-", "-", "flexible, always same dmg", "-", "-"),
    MechWeapon("Flamer Mk.2", "2", "arm weapon", "40", "200% dmg", "3", "flamer fuel", "5", "50", "25", "1", "1 action", "-"),
    MechWeapon("Flamer expanded tanks", "1", "arm weapon", "30", "200% dmg", "3", "flamer fuel", "5", "75", "25", "1", "1 action", "26 [1]"),
    MechWeapon("Laser sniper", "1", "arm weapon", "100", "50% dmg, penetrates all small targets in a line", "6", "micro fusion cell", "4", "1", "1", "1", "2 actions", "30 [2], 29 [1], 31 [3]"),
    MechWeapon("Laser beam", "1", "arm weapon", "50", "50% dmg", "3", "small energy cell", "2", "30", "10", "2", "1 action", "28 [1], 30 [3], 31 [2]"),
    MechWeapon("Laser sniper Mk.2", "2", "arm weapon", "200", "50% dmg, penetrates all small targets in a line", "8", "micro fusion cell", "4", "1", "1", "1", "1 turn", "-"),
    MechWeapon("Laser beam Mk.2", "2", "arm weapon", "75", "50% dmg", "3", "small energy cell", "2", "30", "10", "3", "2 actions", "-"),
    MechWeapon("Micro missiles Mk.2", "2", "shoulder", "40", "+3 AC", "5", "micro missile", "3", "6", "6", "1", "automatically reloads every turn (can be fired only once per turn)", "33 [2], 35 [1]"),
    MechWeapon("Micro missiles Mk.3", "3", "shoulder", "50", "+3 AC", "5", "micro missile", "2", "9", "9", "1", "automatically reloads every turn (can be fired only once per turn)", "-"),
    MechWeapon("Seeking micro missiles", "2", "shoulder", "30", "-", "4", "micro missile", "6", "3", "3", "1", "automatically reloads every turn (can be fired only once per turn)", "35 [2]"),
    MechWeapon("Seeking micro missiles Mk.2", "3", "shoulder", "40", "-", "4", "micro missile", "3", "6", "6", "1", "automatically reloads every turn (can be fired only once per turn)", "-"),
    MechWeapon("Grounded projectable shield", "1", "arm weapon", "200", "-", "-", "shield core", "1", "-", "-", "-", "1 end of combat", "13 [1]")
]

ENEMY_MECHS=[]

ENEMY_PILOTS=[]

PLAYER_PILOTS=[]

PLAYER_MECHS=[]

DEPLOYED=[]

ENVIRONMENT=[
    Entitet(Environment("Tree", 2, False), r'res/postTree.png'),
    Entitet(Environment("metal Post", 2, False), r'res/postMetal.png'),
    Entitet(Environment("stone Wall", 2, False), r'res/wallStone.png'),
    Entitet(Environment("stone Wall Window", 1, False), r'res/windowStoneTB.png'),
    Entitet(Environment("stone Wall Window", 1, False), r'res/windowStoneLR.png'),
    Entitet(Environment("brick Wall", 2, False), r'res/wallBrick.png'),
    Entitet(Environment("brick Wall Window", 1, False), r'res/windowBrickLR.png'),
    Entitet(Environment("brick Wall Window", 1, False), r'res/windowBrickTB.png'),
    Entitet(Environment("left end of a turned over Table", 1, True), r'res/turnedtableWoodT.png'),
    Entitet(Environment("right end of a turned over Table", 1, True), r'res/turnedtableWoodB.png'),
    Entitet(Environment("right end of a turned over Table", 1, True), r'res/turnedtableWoodL.png'),
    Entitet(Environment("left end of a turned over Table", 1, True), r'res/turnedtableWoodR.png'),
    Entitet(Environment("bottom edge of a square Table", 0, True), r'res/squareTableWoodB.png'),
    Entitet(Environment("bottom-left corner of a square Table", 0, True), r'res/squareTableWoodBL.png'),
    Entitet(Environment("bottom-right corner of a square Table", 0, True), r'res/squareTableWoodBR.png'),
    Entitet(Environment("square Table", 0, True), r'res/squareTableWoodC.png'),
    Entitet(Environment("left edge of a square Table", 0, True), r'res/squareTableWoodL.png'),
    Entitet(Environment("right edge of a square Table", 0, True), r'res/squareTableWoodR.png'),
    Entitet(Environment("top edge of a square Table", 0, True), r'res/squareTableWoodT.png'),
    Entitet(Environment("top-left corner of a square Table", 0, True), r'res/squareTableWoodTL.png'),
    Entitet(Environment("top-right corner of a square Table", 0, True), r'res/squareTableWoodTR.png'),
    Entitet(Environment("small wooden Table", 0, True), r'res/smallTableWood.png'),
    Entitet(Environment("destroyed Mech", 1, False), r'res/mechDestroyed.png'),
    Entitet(Environment("wooden Half-Wall", 1, False), r'res/halfWallWoodLR.png'),
    Entitet(Environment("wooden Half-Wall", 1, False), r'res/halfWallWoodTB.png'),
    Entitet(Environment("bottom corner of a wooden Half-Wall", 1, False), r'res/halfWallEndWoodB.png'),
    Entitet(Environment("left corner of a wooden Half-Wall", 1, False), r'res/halfWallEndWoodL.png'),
    Entitet(Environment("right corner of a wooden Half-Wall", 1, False), r'res/halfWallEndWoodR.png'),
    Entitet(Environment("top corner of a wooden Half-Wall", 1, False), r'res/halfWallEndWoodT.png'),
    Entitet(Environment("metal Half-Wall", 1, False), r'res/halfWallMetalLR.png'),
    Entitet(Environment("metal Half-Wall", 1, False), r'res/halfWallMetalTB.png'),
    Entitet(Environment("top corner of a metal Half-Wall", 1, False), r'res/halfWallEndMetalT.png'),
    Entitet(Environment("left corner of a metal Half-Wall", 1, False), r'res/halfWallEndMetalL.png'),
    Entitet(Environment("right corner of a metal Half-Wall", 1, False), r'res/halfWallEndMetalR.png'),
    Entitet(Environment("bottom corner of a metal Half-Wall", 1, False), r'res/halfWallEndMetalB.png'),
    Entitet(Environment("Chair", 0, True), r'res/chairB.png'),
    Entitet(Environment("Chair", 0, True), r'res/chairL.png'),
    Entitet(Environment("Chair", 0, True), r'res/chairR.png'),
    Entitet(Environment("Chair", 0, True), r'res/chairT.png'),
    Entitet(Environment("top side of a Bed", 0, False), r'res/bedT1.png'),
    Entitet(Environment("top side of a Bed", 0, False), r'res/bedT2.png'),
    Entitet(Environment("bottom side of a Bed", 0, False), r'res/bedB1.png'),
    Entitet(Environment("bottom side of a Bed", 0, False), r'res/bedB2.png'),
    Entitet(Environment("red  Barrel", 1, False), r'res/barrelRed.png'),
    Entitet(Environment("green Barrel", 1, False), r'res/barrelGreen.png'),
]


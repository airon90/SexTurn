#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import csv
import os


class Player():
    def __init__(self, id, name, sex, orient, partners, skips, stats):
        self.id = id
        self.name = name
        self.sex = sex
        self.orient = orient
        self.partners = partners
        self.skips = skips
        self.stats = stats

    def __str__(self):
        if self.sex == 0:
            s = "male"
        else:
            s = "female"
        if self.orient == 0:
            o = "hetero"
        elif self.orient == 1:
            o = "bisex"
        elif self.orient == 2:
            o = "gay"
        return self.name + " (" + s + ")" if self.orient == -1 else self.name + " (" + s + ", " + o + ")"

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sex(self):
        return self.sex

    def get_orient(self):
        return self.orient

    def get_partners(self):
        return self.partners

    def get_skips(self):
        return self.skips

    def get_stats(self):
        return self.stats

    def set_partners(self, partners):
        self.partners = partners

    def set_skips(self, skips):
        self.skips = skips

    def set_stats(self, stats):
        self.stats = stats


class Place():
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex

    def get_sex(self):
        return self.sex

    def get_name(self):
        return self.name


ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + \
    "/" if os.path.dirname(os.path.abspath(__file__)) else ""

nSkips = 3

loop = True
while(loop):
    nPlayers = 1
    while (int(nPlayers) < 2 or nPlayers.isdigit() == False):
        try:
            nPlayers = input("Players: ")
        except IOError:
            raise(IOError)

    nPlayers = int(nPlayers)
    players = []
    partners = []
    names = []
    stats = [0]*nPlayers

    considerOrient = -1
    while (int(considerOrient) < 0 or
            int(considerOrient) > 1 or
            considerOrient.isdigit() == False):
        try:
            considerOrient = input("Consider sexual orientation? (0, 1): ")
        except IOError:
            raise(IOError)
    considerOrient = int(considerOrient)
    totSex = 0
    for n in range(nPlayers):
        try:
            namePlayer = input("Name player " + str(n + 1) + ": ")
        except IOError:
            raise(IOError)

        if (namePlayer not in names):
            names.append(namePlayer)
        else:
            while (namePlayer in names):
                print(namePlayer + " is already chosen")
                try:
                    namePlayer = input("Name player " + str(n + 1) + ": ")
                except IOError:
                    raise(IOError)
            names.append(namePlayer)

        sexPlayer = -1
        while (int(sexPlayer) < 0 or
               int(sexPlayer) > 1 or
               sexPlayer.isdigit() == False):
            print("Sex of player", str(n + 1), "(m=0, f=1): ", end="")
            sexPlayer = input("")
        sexPlayer = int(sexPlayer)

        orPlayer = -1
        if (considerOrient == 1):
            while (int(orPlayer) < 0 or
                   int(orPlayer) > 2 or
                   orPlayer.isdigit() == False):
                print("Sexual orientation of player ", str(n + 1))
                print("(h=0, b=1, g=2): ", end="")
                orPlayer = input("")
        totSex = totSex + sexPlayer
        players.append(Player(n, namePlayer, sexPlayer,
                              orPlayer, partners, nSkips, stats))

    for partner in players:
        if (considerOrient == 1):
            partners = []
            sex = int(partner.get_sex())
            orient = int(partner.get_orient())
            name = partner.get_name()

            for partner2 in players:
                name2 = partner2.get_name()
                if (name != name2):
                    orient2 = int(partner2.get_orient())
                    sex2 = int(partner2.get_sex())
                    name2 = partner2.get_name()
                    if (sex == 0 and orient == 0 and sex2 == 1 and orient2 != 2) or (sex == 1 and orient == 0 and sex2 == 0 and orient2 != 2):
                        partners.append(partner2)
                    if (sex == 0 and orient == 1 and not (sex2 == 1 and orient2 == 2) and not (sex2 == 0 and orient2 == 0)) or (sex == 1 and orient == 1 and not (sex2 == 0 and orient2 == 2) and not (sex2 == 1 and orient2 == 0)):
                        partners.append(partner2)
                    if (sex == 0 and orient == 2 and sex2 == 0 and orient2 != 0) or (sex == 1 and orient == 2 and sex2 == 1 and orient2 != 0):
                        partners.append(partner2)
            if partners == []:
                print(name, "doesn't have any partner! Aborting")
                loop = False
            partner.set_partners(partners)
        else:
            partners = []
            name = partner.get_name()

            for partner2 in players:
                name2 = partner2.get_name()
                if (name != name2):
                    partners.append(partner2)
            partner.set_partners(partners)
    confirm = -1
    for pl in range(len(players)):
        print(str(pl + 1) + ".", players[pl])
    while (int(confirm) < 0 or int(confirm) > 1 or confirm.isdigit() == False):
        try:
            confirm = input("Are data correct? (0, 1): ")
        except IOError:
            raise(IOError)
    if (confirm == "1"):
        loop = False

loop = True
if loop == True:
    print("Include sexual actions? (0 (no), 1 (also), 2 (only)): ")
    level = -1

    while level < 0 or level > 2:
        level = int(input("Choice: "))

actions = []
places = []
levelMax = 1
for i in range(levelMax + 1):
    places.append(list())
    actions.append(list())

with open(ABS_PATH + 'labels.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["type"] == "A":
            actions[int(row["level"])].append(row["label"])
        elif row["type"] == "P":
            if (totSex == 0 or totSex == nPlayers):
                if (totSex == 0 and row["sex"] != "1"):
                    places[int(row["level"])].append(
                        Place(row["label"], row["sex"]))
                if (totSex == nPlayers and row["sex"] != "0"):
                    places[int(row["level"])].append(
                        Place(row["label"], row["sex"]))
            else:
                places[int(row["level"])].append(
                    Place(row["label"], row["sex"]))
        else:
            print("Error in CSV file")
            loop = False
            break

if (level == 0):
    del actions[1]
    del places[1]

if (level == 2):
    del places[0]

turn = 0

while loop:
    playr = players[turn % nPlayers]
    print("It's " + playr.name + "'s turn")

    skip = playr.get_skips()
    opt = "z"
    if skip == 0:
        while opt not in ["d", "q", "c", ""]:
            print("C = continue, D = statistics, Q = quit")
            opt = input("Choice: ").lower()
            if opt == "+":
                playr.set_skips(skip + 1)
                print("Skip added to " + playr.get_name())
    else:
        while opt not in ["d", "q", "s", "c", ""]:
            print("C = continue, D = statistics, S = skip, Q = quit")
            opt = input("Choice: ").lower()
    if opt == "d":
        stats = playr.get_stats()
        print("Total matches with other players:")
        for n in range(len(players)):
            if playr.get_name() != players[n].get_name():
                print("* " + players[n].get_name() + ": " + str(stats[n]))
            else:
                totalPlay = stats[n]
        print("Total turns: " + str(totalPlay))

    elif opt == "q":
        print("Thank you for playing!")
        loop = False

    elif opt == "s":
        playr.set_skips(skip - 1)
        print(playr.get_name(), "skipped the match")

    elif opt == "c" or opt == "":
        partner = playr.get_partners()
        player2 = partner[random.randint(0, len(partner) - 1)]
        sex = player2.get_sex()
        randomAction = random.randint(0, len(actions) - 1)
        action = actions[randomAction][random.randint(
            0, len(actions[randomAction]) - 1)]
        randomPlace = random.randint(0, len(places) - 1)
        place = places[randomPlace][random.randint(
            0, len(places[randomPlace]) - 1)]
        sexplace = place.get_sex()
        while ((sex == 0 and sexplace == 1) or (sex == 1 and sexplace == 0)):
            randomPlace = random.randint(0, len(places) - 1)
            place = places[randomPlace][random.randint(
                0, len(places[randomPlace]) - 1)]
            sexplace = place.get_sex()

        print(playr.get_name(), "must", action.lower(),
              player2.get_name() + "'s", place.get_name())
        goOn = input("")
        stats = playr.get_stats()
        stats[player2.get_id()] = stats[player2.get_id()] + 1
        stats[playr.get_id()] = stats[playr.get_id()] + 1
        playr.set_stats(stats)
        stats = player2.get_stats()
        stats[playr.get_id()] = stats[playr.get_id()] + 1
        stats[player2.get_id()] = stats[player2.get_id()] + 1
        player2.set_stats(stats)
    else:
        print("Option not valid")

    turn = turn + 1

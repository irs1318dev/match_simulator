import random
from random_word import RandomWords
import league

class season:
    def __init__(self, year):
        self.year = year;
        self.leagues=[];
        for i in range (0,3):
            print("Creating league %d"%(i))
            self.leagues.append(league.league(i, random.randint(20,30)))

        #create matches
        #create pairings for match


    def __str__(self):
        return "Season: %s" %(self.year)



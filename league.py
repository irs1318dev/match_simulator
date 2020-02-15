import random
import team

class league:
    def __init__(self, league_id, num_teams):
        name = "League_%d"%(league_id)
        self.name=name
        self.num_teams = num_teams
        self.team=[]
        print ("Creating League %d (%s) with %d teams" %(league_id, self.name, num_teams))
        for i in range (0, num_teams):
            name = "%s_%d"%(self.name,i)
            print("Creating team %d %s" %(i,name))
            self.team.append(team.team(name, league_id))

    def __str__(self):
        return "Name: %s" %(self.name)



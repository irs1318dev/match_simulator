import random

class match:
    def __init__(self, field):
        self.time_remaining = [(15*1000),(135*1000)] # auton and telop time in ms
        self.tick_time = 250 # 250ms per calculation tick
        self.current_time=0;

    def __str__(self):
        return "Name: %s %d %d (%.2f %.2f %.2f)" %(self.name, self.team_id, self.league, self.shoot_skill, self.defense_skill, self.climb_skill)

    def do_tick(self):
        self.current_time += self.tick_time
        self.recalculate()
        if (self.current_time > self.time_remaining[0]+self.time_remaining[1]):
            # end of game
            print ("Game End at %d " %(self.current_time))
            return 0
        elif (self.current_time > self.time_remaining[0]):
            # in teleop
            print ("Teleop at %d " %(self.current_time))
            return 1
        else:
            # in auton
            print ("Auton at %d " %(self.current_time))
            return 2

    def recalculate(self):
        return 0

    def simulate_auton(self):
        return 0

    def simulate_teleop(self):
        return 0

    def simulate_endgame(self):
        return 0



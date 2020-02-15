import random
from random_word import RandomWords

class team:
    def __init__(self, team_name, league_id):
        self.name=team_name
        self.team_id=random.randint(1000,9000)
        self.league=league_id

        # variables controlling auton
        self.auton_shoot_skill=1.0
        self.auton_pickup_skill=1.0
        self.auton_move_from_line=1.0

        # variables controlling teleop
        self.shoot_skill=1.0
        self.defense_skill=1.0
        self.climb_skill=1.0

        # variables tracking meet to meet
        self.robot_improve=0

        # variables tracking match to match
        self.driver_improve=1

        # intrinsic variables about the robot
        self.can_climb=1
        self.can_balance=1
        self.can_shoot=1
        self.control_panel=1
        self.rotation_sensor=1
        self.color_sensor=1
        self.ground_pickup=1
        self.hopper_pickup=1

        # robot speed in ft/min
        self.robot_speed=200
        self.robot_turn_radius=1.0
        self.robot_turn_rate=1.0
        self.init_stats()

    def __str__(self):
        return "Name: %s %d %d (%.2f %.2f %.2f)" %(self.name, self.team_id, self.league, self.shoot_skill, self.defense_skill, self.climb_skill)

    def init_stats(self):
        adjust = random.uniform(.80,1.20)
        self.shoot_skill *= adjust 
        adjust = random.uniform(.80,1.20)
        self.defense_skill *= adjust 
        adjust = random.uniform(.80,1.20)
        self.climb_skill *= adjust 

    def set_shoot_skill(self, newval):
        self.shoot_skill = newval

    def set_defense_skill(self, newval):
        self.defense_skill = newval

    def set_climb_skill(self, newval):
        self.climb_skill = newval



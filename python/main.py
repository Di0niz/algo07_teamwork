import sys
import math
import random

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

debug = False

class Vec2:
    """Определение вектора для решения задачи по поиску"""
    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y

    def perpendicular_component(self, v):
        return self.sub(self.parallel_component(v))

    def dot(self, v):
        return self.x*v.x + self.y*v.y

    def sub(self, v):
        return Vec2(self.x - v.x, self.y - v.y)

    def minus(self):
        return Vec2(-self.x, -self.y)

    def add(self, v):
        return Vec2(self.x + v.x, self.y + v.y)

    def div(self, scalar):
        return Vec2(self.x*1.0/scalar, self.y*1.0/scalar)

    def mult(self, scalar):
        return Vec2(self.x*scalar, self.y*scalar)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        length = self.length()
        if length > 0:
            return self.div(length)
        return self

    def cross(self):
        return Vec2(self.y, -self.x)

    def distance(self, v):
        return math.hypot(self.x-v.x, self.y-v.y)

    def parallel_component(self, unit_basis):
        projection = self.dot(unit_basis)
        return unit_basis.mult(projection)

    def truncate(self, max_length):
        length = self.length()
        if length > math.fabs(max_length):
            return self.mult(max_length * 1.0 / length)
        return self

    def set_y_zero(self):
        return Vec2(self.x, 0)


    def rotate(self, alpha):
        s = math.sin(alpha)
        c = math.cos(alpha)

        return Vec2(self.x*c-self.y*s, self.x*s+self.y*c)

    def angle_to(self, v):
        dot = self.normalize().dot(v.normalize())
        return math.acos(dot)


    def distance_from_line(self, point, line_origin, line_unit_tangent):
        offset = point.sub(line_origin)
        perp = offset.perpendicular_component(line_unit_tangent)

        return perp.length()

    # Определяем вхождение точки в указанный круг
    def intersects_circle(self, center, radius):
        return self.distance(center) < radius

    def abs(self):
        return Vec2(self.x if self.x > 0 else -self.x, self.y if self.y > 0 else -self.y)

    def __repr__(self):
        return "(%d,%d)" % (self.x, self.y)

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)

    def __cmp__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return cmp(int(self.x), int(other.x)) and cmp(int(self.y, other.y))


    @staticmethod
    def zero():
        return Vec2(0, 0)

    @staticmethod
    def forward():
        return Vec2(0, 1)

class Entity:
    """Описание класса игрока"""

    def __init__(self, entity_id, entity_type, x, y, speed_x, speed_y, state, radius=100.0, max_speed=150.0, mass=1.0, friction=1.0):
        self.entity_id = int(entity_id)
        self.entity_type = entity_type
        self.position = Vec2(int(x), int(y))
        self.velocity = Vec2(int(speed_x), int(speed_y))
        self.state = int(state)
        self.mass = mass
        self.radius = radius
        self.max_speed = max_speed
        self.friction = friction

        self.avoidance = Vec2.zero()
        self.steer     = Vec2.zero()
        self.desired_velocity = self.velocity

        self.thrust    = 150

        self.target    = None

    def get_distance_to_unit(self, unit):
        return self.position.distance(unit.position)

    def __str__(self):
        return "Entity('%d','%s','%d','%d','%d','%d','%d',%d,%d,%f,%f)" % (
            self.entity_id, self.entity_type,
            self.position.x, self.position.y,
            self.velocity.x, self.velocity.y,
            self.state, self.radius, self.max_speed, self.mass, self.friction
            )
    def __repr__(self):
        return "Entity('%d','%s','%d','%d','%d','%d','%d',%d,%d,%f,%f)" % (
            self.entity_id, self.entity_type,
            self.position.x, self.position.y,
            self.velocity.x, self.velocity.y,
            self.state, self.radius, self.max_speed, self.mass, self.friction
            )

    def __cmp__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return cmp(self.entity_id, other.entity_id)

    def forward(self, velocity = None, t = 1.0):
        if velocity is None:
            velocity = self.velocity

        velocity = velocity.add(self.steer).mult(t)
        position = self.position.add(velocity)

        return Entity(
            self.entity_id,
            self.entity_type,
            position.x, position.y,
            velocity.x, velocity.y,
            self.state,
            self.radius,
            self.max_speed,
            self.mass,
            self.friction
        )

    def future_position(self, with_steering = None):
        if with_steering == None:
            return self.position.add(self.velocity.mult(1.0))
        else: 
            return 0 
#                    dv = self.velocity.\
#        sub(for_wizard.position.sub(steer_direction).normalize().mult(150*for_wizard.friction))


    def future_velocity(self, with_steering):
        if with_steering == None:
            return self.velocity.mult(self.friction)
        else: 
            return 0 

    def set_target_unit(self, target, trust = 150):
        #self.target = target
        self.set_target(target.future_position(), trust)


    def set_target(self, future_t, trust = 150):

        self.desired_velocity = self.get_desired_velocity(future_t)
        self.steer = self.desired_velocity.sub(self.velocity).normalize().mult(trust * self.friction)

    def get_direction(self):
        return self.position.add(self.velocity).add(self.steer).add(self.avoidance)

    def get_force(self, trust = 150):
        steering = Vec2.zero()
        steering = steering.add(self.steer)
        steering = steering.add(self.avoidance)

        #steering = steering.truncate(trust)
        #steering = steering.div(self.mass)

        return self.position.add(steering)

    def get_desired_velocity(self, t, position = None):
        """ Ищем направление движения объекта"""
        max_velocity = 800

        return t.sub(self.position).normalize().mult(max_velocity + 1)

    def steer_to(self, t, vt=None, avoidance=None):
        if vt is None:
            vt = Vec2.zero()

        if avoidance is None:
            avoidance = Vec2.zero()

        if self.velocity.x == 0 and self.velocity.y == 0:
            return t


        future_t = t.add(vt.mult(2.0))

        desired_velocity = self.get_desired_velocity(future_t)

        steering = desired_velocity.sub(self.velocity).normalize()
        steering = steering.mult(800)
        steering = steering.sub(avoidance)

        return self.position.add(steering)

    def steer_to_unit(self, target, avoidance=None):
        return self.steer_to(target.position, target.velocity, avoidance)


class World:
    def __init__(self, my_team_raw):
        self.my_team_id = int(my_team_raw)
        self.spell = 0
        self.wizards = []
        self.snaffles = []
        self.opponents = []
        self.bludgers = []
        self.current_spell = []

    def add_spell(self):
        self.spell = self.spell + 1
        new_current_spell = []
        for cur in self.current_spell:
            spell = cur[0], cur[1], cur[2] - 1
            if (spell[2] > 0):
                new_current_spell.append(spell) 
        # удаляем заклинания, которые не используются
        self.current_spell = new_current_spell

    def spell_cost(self, spell):
        spells = {
            # Strategy.CAST_ACCIO: (20, 6),
            # Strategy.CAST_FLIPENDO: (20, 3),
            # Strategy.CAST_OBLIVIATE: (5, 1),
            # Strategy.CAST_PETRIFICUS: (10, 3)
        }
        return spells[spell]

    def make_spell(self, wizard, spell, target):
        """Делаем заклинание"""

        cost, time = self.spell_cost(spell)
        self.spell = self.spell - cost

        self.current_spell.append((spell, wizard.entity_id, target.entity_id, time))
    

    def __str__(self):
        s = "w = World(%d)" % self.my_team_id
        for el in self.wizards:
            s = s + "\nw.wizards.append(%s)" % el
        for el in self.snaffles:
            s = s + "\nw.snaffles.append(%s)" % el
        for el in self.opponents:
            s = s + "\nw.opponents.append(%s)" % el
        for el in self.bludgers:
            s = s + "\nw.bludgers.append(%s)" % el
        return s

    def read_raw_input(self):
        self.wizards = []
        self.snaffles = []
        self.opponents = []
        self.bludgers = []

        count_entities = int(input())

        for i in range(count_entities):
            self.add_raw_input(input())

 #       if debug:
 #           print >> sys.stderr, self

    def add_raw_input(self, raw):
#        if debug:
#            print >> sys.stderr, raw
        entity_id, entity_type, x, y, vx, vy, state = raw.split()
        if entity_type == "WIZARD":
            self.wizards.append(
                Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 300, 1.0, 0.75)
                )

        elif entity_type == "OPPONENT_WIZARD":
            self.opponents.append(
                Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 300, 1.0, 0.75)
                )

        elif entity_type == "SNAFFLE":
            self.snaffles.append(
                Entity(entity_id, entity_type, x, y, vx, vy, state, 150, 800, 0.5, 0.9)
                )

        elif entity_type == "BLUDGER":
            self.bludgers.append(
                Entity(entity_id, entity_type, x, y, vx, vy, state, 200, 600, 8.0, 0.75)
                )


    def center(self):
        """ определяем центр игры"""
        return Vec2(8000, 3750)  # Entity("0 CENTER 8000 3750 0 0 0")

    def opponent_gate(self, wizard=None):
        """ определяем центр игры"""

        center = 3750
        if wizard != None:
            if wizard.velocity.y < 30:
                center = center - 600
            elif wizard.velocity.y > -30:
                center = center + 600
            else:
                center = min(max(wizard.position.y, center - 600), 3750 + 600)

        return Vec2(16000 if self.my_team_id == 0 else 0, center)

    def gate(self, wizard=None):
        """ определяем центр игры"""

        center = 3750
        if wizard != None:
            center = min(max(wizard.position.y, center - 800), 3750 + 800)

        return Vec2(16000 if self.my_team_id == 1 else 0, center)

    def find_snaffle(self, for_wizard, cur_snaffle=None):
        """ ищем ближайший мяч для волшебника """
        near_snaffle = None
        min_dist = 100000

        for snaffle in self.snaffles:

            if snaffle == cur_snaffle:
                continue

            # если мяч двигается слишком быстро, тогда игнорируем его
            if snaffle.velocity.length() > 1000:
                continue    

            dist = for_wizard.get_distance_to_unit(snaffle)
            steer_direction = for_wizard.steer_to_unit(snaffle)
            dv = for_wizard.velocity.\
                sub(for_wizard.position.sub(steer_direction).normalize().mult(150))

            new_min = dist /dv.length()

            if new_min < min_dist:
                near_snaffle = snaffle
                min_dist = new_min

        return near_snaffle if near_snaffle else cur_snaffle


if __name__ == '__main__':
    debug = True

    w = World(input())

    # game loop
    while True:
        my_score, my_magic = [int(i) for i in input().split()]
        opponent_score, opponent_magic = [int(i) for i in input().split()]

        w.read_raw_input()

        near_snaffle = None
        for wizard in w.wizards:
            near_snaffle = w.find_snaffle(wizard, near_snaffle)

            print(f"MOVE {near_snaffle.position.x} {near_snaffle.position.y} 150")

